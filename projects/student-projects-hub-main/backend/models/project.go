package models

import (
	"time"
)

// Project структура соответствует спецификации из ТЗ
type Project struct {
	ID          int       `json:"id"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	Author      string    `json:"author"`
	CreatedAt   time.Time `json:"created_at"`
}

// CreateProjectRequest структура для запроса создания проекта
type CreateProjectRequest struct {
	Title       string `json:"title" binding:"required"`
	Description string `json:"description" binding:"required"`
	Author      string `json:"author" binding:"required"`
}

// Validate проверяет базовую валидацию полей
func (r *CreateProjectRequest) Validate() error {
	if r.Title == "" {
		return &ValidationError{Field: "title", Message: "Название проекта обязательно"}
	}
	if r.Description == "" {
		return &ValidationError{Field: "description", Message: "Описание проекта обязательно"}
	}
	if r.Author == "" {
		return &ValidationError{Field: "author", Message: "Автор проекта обязателен"}
	}
	return nil
}

// ValidationError ошибка валидации
type ValidationError struct {
	Field   string `json:"field"`
	Message string `json:"message"`
}

func (e *ValidationError) Error() string {
	return e.Message
}
