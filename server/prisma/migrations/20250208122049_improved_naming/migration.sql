/*
  Warnings:

  - You are about to drop the `queries` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "queries" DROP CONSTRAINT "queries_chatbotId_fkey";

-- DropTable
DROP TABLE "queries";

-- CreateTable
CREATE TABLE "Queries" (
    "id" TEXT NOT NULL,
    "query" TEXT NOT NULL,
    "chatbotId" TEXT NOT NULL,

    CONSTRAINT "Queries_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Queries" ADD CONSTRAINT "Queries_chatbotId_fkey" FOREIGN KEY ("chatbotId") REFERENCES "Chatbot"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
