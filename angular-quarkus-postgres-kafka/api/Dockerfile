# Multi-stage build: maven-builder → production (JVM mode)
# ─── Build Stage ─────────────────────────────────────────────────────────────
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /app

COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
RUN ./mvnw dependency:go-offline -q

COPY src src
RUN ./mvnw clean package -DskipTests -q

# ─── Production Stage ────────────────────────────────────────────────────────
FROM eclipse-temurin:21-jre-alpine AS production
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /app/target/quarkus-app/lib ./lib
COPY --from=builder /app/target/quarkus-app/*.jar ./
COPY --from=builder /app/target/quarkus-app/app ./app
COPY --from=builder /app/target/quarkus-app/quarkus ./quarkus

USER appuser
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD wget -qO- http://localhost:8080/q/health || exit 1

STOPSIGNAL SIGTERM
CMD ["java", "-jar", "quarkus-run.jar"]
