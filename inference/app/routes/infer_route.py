from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.prisma.prisma_client import get_prisma
from pydantic import BaseModel
from app.core.jina_ai import JinaAI
from app.core.pinecone import get_matches
from app.core.groq import client
from app.constants.prompts import INFER_PROMPT
import google.generativeai as genai
import os
import asyncio

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class InferRequest(BaseModel):
    query: str
    chatbot_id: str
    previous_messages: list[Message]

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


@router.post("/infer")
async def infer(request: InferRequest):
    # get embedding of query, search pinecone index for similar docs top k, use chunk_id in metadata to obtain chunk text, then use groq to generate response

    Prisma = await get_prisma();

    await Prisma.queries.create(
        data = {
            "query": request.query,
            "chatbotId": request.chatbot_id
        }
    )


    jina_ai = JinaAI()
    embedding = jina_ai.fetch_embeddings(request.query)
    matches = await get_matches(embedding, request.chatbot_id)
    # get the chunks from postgres based on the chunk_ids in the matches

    Prisma = await get_prisma();

    chunks = await Prisma.chunk.find_many(
        where={
            "id": {
                "in": [match["metadata"]["chunk_id"] for match in matches]
            }
        }
    )


    # pass the matches to groq to generate response


    stringified_messages = []
    for i, message in enumerate(request.previous_messages):
        if i % 2 == 0:
            stringified_messages.append(f"User: {message.content}")
        else:
            stringified_messages.append(f"Assistant: {message.content}")

    print(stringified_messages)

    context = "\n".join([chunk.chunkText for chunk in chunks])

    chatbot = await Prisma.chatbot.find_unique(
        where={
            "id": request.chatbot_id
        }
    )

    description = chatbot.description


    messages = [
        {
            "role": "system",
            "content": INFER_PROMPT.format(description=description, context=context, previous_messages=stringified_messages)
        }
    ]

    messages.append({"role": "user", "content": request.query})

    async def generate_response():
        # stream = client.chat.completions.create(
        #     messages=messages,
        #     model="mixtral-8x7b-32768",
        #     temperature=0.5,
        #     max_tokens=4096,
        #     stream=True
        # )

        # response = ""

        # for chunk in stream:
        #     if chunk.choices[0].delta.content is not None:
        #         content = chunk.choices[0].delta.content
        #         response += content
        #         yield f"{content}"

        # print(response)

        model = genai.GenerativeModel(model_name="gemini-2.0-flash",system_instruction=INFER_PROMPT.format(description=description, context=context, previous_messages=stringified_messages))

        response = model.generate_content(request.query)
        full_response = response.text
        print(full_response)
        chunk_size = 10 
        for i in range(0, len(full_response), chunk_size):
            chunk = full_response[i:i+chunk_size]
            yield f"{chunk}"
            await asyncio.sleep(0.05)


    return StreamingResponse(generate_response(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "Content-Type": "text/event-stream"})
