async function loadProjects() {
    try {
        // 1. Запрашиваем данные
        const response = await fetch('http://localhost:8080/api/projects');
        const result = await response.json();
        
        console.log('Получено от сервера:', result);
        
        // 2. Берём массив проектов из поля "data"
        const projects = result.data;
        
        // 3. Показываем проекты
        showProjects(projects);
        
    } catch (error) {
        console.log('Ошибка загрузки:', error);
        document.querySelector('.cards-container').innerHTML = `
            <div style="text-align: center; padding: 40px; color: red;">
                <h3>Ошибка загрузки проектов</h3>
                <p>${error.message}</p>
            </div>
        `;
    }
}

function showProjects(projects) {
    const container = document.querySelector('.cards-container');
    container.innerHTML = '';
    
    if (!Array.isArray(projects)) {
        console.error('projects не массив:', projects);
        container.innerHTML = '<p>Ошибка формата данных</p>';
        return;
    }
    
    if (projects.length === 0) {
        container.innerHTML = '<p>Пока нет проектов</p>';
        return;
    }
    
    projects.forEach(project => {
        const card = document.createElement('div');
        card.className = 'Card__Content';
        card.dataset.projectId = project.id; // ← ДОБАВЬ ЭТУ СТРОКУ!
        
        const githubUrl = project.githubUrl || '#';
        
        card.innerHTML = `
            <div class="Card__menu">
                <button class="Card__menu-button">⋯</button>
                <div class="Card__dropdown">
                    <div class="Card__dropdown-item">Редактировать</div>
                    <div class="Card__dropdown-item delete">Удалить</div>
                </div>
            </div>
            
            <div class="Card__Text">
                <div class="Card__Name">${project.title || 'Без названия'}</div>
                <div class="Card__Author">${project.author || 'Автор не указан'}</div>
                <div class="Card__Description">${project.description || 'Нет описания'}</div>
            </div>
            
            <div class="Card__Actions">
                <a href="project.html?id=${project.id}">
                    <button class="card__action-button card__action-button--open">
                        Открыть
                    </button>
                </a>
                <a href="${githubUrl}" target="_blank">
                    <button class="card__action-button card__action-button--github">
                        <img src="all__projects/github.png" alt="GitHub" class="Git__img">
                    </button>
                </a>
            </div>
        `;
        
        container.appendChild(card);
    });
    
    initCardMenus();
}

// Функция для меню карточек
function initCardMenus() {
    document.querySelectorAll('.Card__menu-button').forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const dropdown = this.nextElementSibling;
            dropdown.classList.toggle('show');
        });
    });
    
    document.addEventListener('click', function() {
        document.querySelectorAll('.Card__dropdown').forEach(dropdown => {
            dropdown.classList.remove('show');
        });
    });
    
    // Обработчик для редактирования
    document.querySelectorAll('.Card__dropdown-item:not(.delete)').forEach(item => {
        item.addEventListener('click', function() {
            const card = this.closest('.Card__Content');
            const projectId = card.dataset.projectId; // Получаем ID из data-атрибута
            window.location.href = `edit.html?id=${projectId}`;
        });
    });
    
    // Обработчик для удаления
    document.querySelectorAll('.Card__dropdown-item.delete').forEach(item => {
        item.addEventListener('click', function() {
            const card = this.closest('.Card__Content');
            const projectId = card.dataset.projectId;
            deleteProject(projectId);
        });
    });
}

// Функция удаления проекта
async function deleteProject(projectId) {
    if (!confirm('Вы уверены, что хотите удалить этот проект?')) {
        return;
    }
    
    try {
        const response = await fetch(`http://localhost:8080/api/projects/${projectId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Проект удалён!');
            loadProjects(); // Перезагружаем список
        } else {
            alert('Ошибка при удалении проекта');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось удалить проект');
    }
}

// Запускаем когда страница загрузится
document.addEventListener('DOMContentLoaded', loadProjects);