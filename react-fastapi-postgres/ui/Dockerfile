# Build stage — Node 20 compiles the React/Vite app
# This Dockerfile is for building static assets only.
# In development, the Vite dev server is used (via docker-compose).
# In production, Rusha serves the built assets.

FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci --prefer-offline

COPY . .
RUN npm run build

# The output is in /app/dist — Rusha picks this up for deployment
