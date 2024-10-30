/*
  Warnings:

  - Added the required column `description` to the `Chatbot` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Chatbot" ADD COLUMN     "description" TEXT NOT NULL;
