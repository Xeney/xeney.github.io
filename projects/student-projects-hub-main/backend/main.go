package main

import (
	"log"

	"github.com/Xeney/student-projects-hub/backend/handlers"
	"github.com/gin-gonic/gin"
)

func main() {
	// Инициализируем Gin router
	router := gin.Default()

	// Настраиваем CORS middleware
	router.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization, Accept")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	})

	// Регистрируем маршруты
	router.GET("/api/projects", handlers.GetProjects)
	router.GET("/api/projects/:id", handlers.GetProjectByID)
	router.POST("/api/projects", handlers.CreateProject)
	router.PUT("/api/projects/:id", handlers.UpdateProject)
	router.DELETE("/api/projects/:id", handlers.DeleteProject)

	// Запускаем сервер
	log.Println("Сервер запущен на http://localhost:8080")
	log.Println("Доступные эндпоинты:")
	log.Println("  GET    /api/projects      - получить список проектов")
	log.Println("  GET    /api/projects/:id  - получить проект по ID")
	log.Println("  POST   /api/projects      - создать новый проект")
	log.Println("  PUT    /api/projects/:id  - обновить проект")
	log.Println("  DELETE /api/projects/:id  - удалить проект")

	if err := router.Run(":8080"); err != nil {
		log.Fatal("Ошибка запуска сервера:", err)
	}
}
