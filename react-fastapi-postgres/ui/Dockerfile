# Build stage — Node 20 compiles the React/Vite app
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci --prefer-offline

COPY . .
RUN npm run build

# Serve stage — Rusha base image provides nginx with SPA config pre-baked
FROM ghcr.io/rusha-corp/base-image-react:latest
COPY --from=build /app/dist /usr/share/nginx/html
