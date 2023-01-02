FROM node:latest

RUN npm i -g pnpm @nestjs/cli

WORKDIR /code
COPY package.json pnpm-lock.yaml ./
RUN pnpm install

COPY . .
