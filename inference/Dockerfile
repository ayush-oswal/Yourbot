FROM python:3.11-slim
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/
WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m prisma generate

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]