/*
  Warnings:

  - You are about to drop the column `apikey` on the `User` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[apiKey]` on the table `User` will be added. If there are existing duplicate values, this will fail.
  - The required column `apiKey` was added to the `User` table with a prisma-level default value. This is not possible if the table is not empty. Please add this column as optional, then populate it before making it required.

*/
-- DropIndex
DROP INDEX "User_apikey_key";

-- AlterTable
ALTER TABLE "User" DROP COLUMN "apikey",
ADD COLUMN     "apiKey" TEXT NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "User_apiKey_key" ON "User"("apiKey");
