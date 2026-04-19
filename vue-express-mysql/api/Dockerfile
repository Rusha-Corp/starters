# Production-optimised Node.js image for Express
FROM node:20-alpine AS production
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app
ENV NODE_ENV=production

COPY package*.json ./
RUN npm ci --only=production --prefer-offline

COPY . .
RUN chown -R appuser:appgroup /app

USER appuser
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost:3000/health || exit 1

STOPSIGNAL SIGTERM
CMD ["node", "src/index.js"]
