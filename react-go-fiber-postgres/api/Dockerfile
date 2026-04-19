# Multi-stage build: go-builder → distroless
# ─── Build Stage ─────────────────────────────────────────────────────────────
FROM golang:1.22-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o server .

# ─── Production Stage ────────────────────────────────────────────────────────
FROM gcr.io/distroless/static-debian12:nonroot

WORKDIR /app
COPY --from=builder /app/server .

USER nonroot:nonroot
EXPOSE 8080

STOPSIGNAL SIGTERM
CMD ["/app/server"]
