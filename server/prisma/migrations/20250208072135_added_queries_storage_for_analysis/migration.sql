-- CreateTable
CREATE TABLE "queries" (
    "id" TEXT NOT NULL,
    "query" TEXT NOT NULL,
    "chatbotId" TEXT NOT NULL,

    CONSTRAINT "queries_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "queries" ADD CONSTRAINT "queries_chatbotId_fkey" FOREIGN KEY ("chatbotId") REFERENCES "Chatbot"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
