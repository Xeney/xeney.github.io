package handlers

import (
	"net/http"
	"strconv"
	"time"

	"github.com/Xeney/student-projects-hub/backend/models"
	"github.com/gin-gonic/gin"
)

// Временное хранилище в памяти
var projects = []models.Project{
	{
		ID:          1,
		Title:       "Tetris на C#",
		Description: "Консольная версия игры",
		Author:      "Дима",
		CreatedAt:   time.Date(2026, 1, 15, 0, 0, 0, 0, time.UTC),
	},
	{
		ID:          2,
		Title:       "Веб-приложение для заметок",
		Description: "SPA приложение на React с бэкендом на Go",
		Author:      "Дамир",
		CreatedAt:   time.Date(2026, 1, 20, 0, 0, 0, 0, time.UTC),
	},
	{
		ID:          3,
		Title:       "API для системы блогов",
		Description: "REST API с JWT аутентификацией",
		Author:      "Дима",
		CreatedAt:   time.Date(2026, 1, 25, 0, 0, 0, 0, time.UTC),
	},
}

// Вспомогательная функция для поиска проекта по ID
func findProjectByID(id int) (*models.Project, int) {
	for i, project := range projects {
		if project.ID == id {
			return &projects[i], i
		}
	}
	return nil, -1
}

// GetProjects возвращает список всех проектов
// GET /api/projects
func GetProjects(c *gin.Context) {
	// Возвращаем JSON массив проектов со статусом 200 OK
	c.JSON(http.StatusOK, gin.H{
		"status":   "success",
		"data":     projects,
		"count":    len(projects),
		"endpoint": "GET /api/projects",
	})
}

// GetProjectByID возвращает проект по ID
// GET /api/projects/:id
func GetProjectByID(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"status":  "error",
			"message": "Неверный формат ID",
			"error":   "ID должен быть числом",
		})
		return
	}

	project, _ := findProjectByID(id)
	if project == nil {
		c.JSON(http.StatusNotFound, gin.H{
			"status":  "error",
			"message": "Проект не найден",
			"error":   "Проект с ID " + idStr + " не существует",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status": "success",
		"data":   project,
	})
}

// CreateProject создает новый проект
// POST /api/projects
func CreateProject(c *gin.Context) {
	var request models.CreateProjectRequest

	// Привязываем JSON к структуре
	if err := c.ShouldBindJSON(&request); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"status":  "error",
			"message": "Неверный формат запроса",
			"error":   err.Error(),
		})
		return
	}

	// Базовая валидация
	if err := request.Validate(); err != nil {
		if validationErr, ok := err.(*models.ValidationError); ok {
			c.JSON(http.StatusBadRequest, gin.H{
				"status":  "error",
				"message": "Ошибка валидации",
				"error":   validationErr.Message,
				"field":   validationErr.Field,
			})
		} else {
			c.JSON(http.StatusBadRequest, gin.H{
				"status":  "error",
				"message": "Ошибка валидации",
				"error":   err.Error(),
			})
		}
		return
	}

	// Генерируем новый ID
	newID := 1
	if len(projects) > 0 {
		maxID := 0
		for _, project := range projects {
			if project.ID > maxID {
				maxID = project.ID
			}
		}
		newID = maxID + 1
	}

	// Создаем новый проект
	newProject := models.Project{
		ID:          newID,
		Title:       request.Title,
		Description: request.Description,
		Author:      request.Author,
		CreatedAt:   time.Now().UTC(),
	}

	// Добавляем в хранилище
	projects = append(projects, newProject)

	// Возвращаем созданный проект со статусом 201 Created
	c.JSON(http.StatusCreated, gin.H{
		"status":  "success",
		"message": "Проект успешно создан",
		"data":    newProject,
	})
}

// UpdateProject обновляет существующий проект
// PUT /api/projects/:id
func UpdateProject(c *gin.Context) {
	// Получаем ID из URL
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"status":  "error",
			"message": "Неверный формат ID",
			"error":   "ID должен быть числом",
		})
		return
	}

	// Ищем проект
	project, index := findProjectByID(id)
	if project == nil {
		c.JSON(http.StatusNotFound, gin.H{
			"status":  "error",
			"message": "Проект не найден",
			"error":   "Проект с ID " + idStr + " не существует",
		})
		return
	}

	// Привязываем JSON к структуре
	var request models.CreateProjectRequest
	if err := c.ShouldBindJSON(&request); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"status":  "error",
			"message": "Неверный формат запроса",
			"error":   err.Error(),
		})
		return
	}

	// Базовая валидация
	if err := request.Validate(); err != nil {
		if validationErr, ok := err.(*models.ValidationError); ok {
			c.JSON(http.StatusBadRequest, gin.H{
				"status":  "error",
				"message": "Ошибка валидации",
				"error":   validationErr.Message,
				"field":   validationErr.Field,
			})
		} else {
			c.JSON(http.StatusBadRequest, gin.H{
				"status":  "error",
				"message": "Ошибка валидации",
				"error":   err.Error(),
			})
		}
		return
	}

	// Обновляем проект (сохраняем ID и created_at)
	projects[index] = models.Project{
		ID:          project.ID,          // Сохраняем оригинальный ID
		Title:       request.Title,       // Новое название
		Description: request.Description, // Новое описание
		Author:      request.Author,      // Новый автор
		CreatedAt:   project.CreatedAt,   // Сохраняем оригинальную дату создания
	}

	// Возвращаем обновленный проект
	c.JSON(http.StatusOK, gin.H{
		"status":  "success",
		"message": "Проект успешно обновлен",
		"data":    projects[index],
	})
}

// DeleteProject удаляет проект
// DELETE /api/projects/:id
func DeleteProject(c *gin.Context) {
	// Получаем ID из URL
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"status":  "error",
			"message": "Неверный формат ID",
			"error":   "ID должен быть числом",
		})
		return
	}

	// Ищем проект
	project, index := findProjectByID(id)
	if project == nil {
		c.JSON(http.StatusNotFound, gin.H{
			"status":  "error",
			"message": "Проект не найден",
			"error":   "Проект с ID " + idStr + " не существует",
		})
		return
	}

	// Удаляем проект из слайса
	projects = append(projects[:index], projects[index+1:]...)

	// Возвращаем статус 204 No Content
	c.Status(http.StatusNoContent)
}
