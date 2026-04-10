// edit.js

// Получаем ID из URL
function getProjectId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Загрузка данных проекта для редактирования
async function loadProjectData() {
    const projectId = getProjectId();
    
    // Если нет ID - это создание нового проекта
    if (!projectId) {
        document.getElementById('form-title').textContent = 'Создание нового проекта';
        return;
    }
    
    try {
        const response = await fetch(`http://localhost:8080/api/projects/${projectId}`);
        const result = await response.json();
        
        if (result.status === 'success') {
            const project = result.data;
            
            // Заполняем форму
            document.getElementById('title').value = project.title;
            document.getElementById('author').value = project.author;
            document.getElementById('description').value = project.description;
        } else {
            alert('Проект не найден');
            goBack();
        }
    } catch (error) {
        console.error('Ошибка загрузки:', error);
        alert('Не удалось загрузить данные проекта');
    }
}

// Сохранение проекта
async function saveProject(event) {
    event.preventDefault(); // Предотвращаем обычную отправку формы
    
    const projectId = getProjectId();
    const formData = {
        title: document.getElementById('title').value.trim(),
        author: document.getElementById('author').value.trim(),
        description: document.getElementById('description').value.trim()
    };
    
    // Валидация
    if (!formData.title || !formData.author || !formData.description) {
        alert('Пожалуйста, заполните все поля');
        return;
    }
    
    try {
        let response;
        
        if (projectId) {
            // Редактирование существующего проекта (PUT)
            response = await fetch(`http://localhost:8080/api/projects/${projectId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
        } else {
            // Создание нового проекта (POST)
            response = await fetch('http://localhost:8080/api/projects', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
        }
        
        const result = await response.json();
        
        if (result.status === 'success') {
            alert(projectId ? 'Проект обновлён!' : 'Проект создан!');
            window.location.href = 'projects.html';
        } else {
            alert('Ошибка: ' + result.message);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось сохранить проект');
    }
}

// Возврат назад
function goBack() {
    window.history.back();
}

// Инициализация
document.addEventListener('DOMContentLoaded', function() {
    loadProjectData();
    document.getElementById('project-form').addEventListener('submit', saveProject);
});