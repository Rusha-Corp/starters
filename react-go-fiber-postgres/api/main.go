package main

import (
	"log"
	"os"

	"github.com/gofiber/cors"
	"github.com/gofiber/fiber/v2"
)

func main() {
	app := fiber.New(fiber.Config{
		AppName: "Rusha API",
	})

	app.Use(cors.New(cors.Config{
		AllowOrigins: "*",
		AllowMethods: "GET,POST,PUT,DELETE,OPTIONS",
		AllowHeaders: "Origin,Content-Type,Accept,Authorization",
	}))

	app.Get("/health", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{
			"status": "ok",
		})
	})

	app.Get("/api/status", func(c *fiber.Ctx) error {
		dbURL := os.Getenv("DATABASE_URL")
		dbStatus := "not_configured"
		if dbURL != "" {
			dbStatus = "configured"
		}

		return c.JSON(fiber.Map{
			"status":   "ok",
			"database": dbStatus,
			"port":     os.Getenv("PORT"),
		})
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Starting server on :%s", port)
	if err := app.Listen(":" + port); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
