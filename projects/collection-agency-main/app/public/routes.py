from flask import Blueprint, render_template, current_app

bp = Blueprint('public', __name__)

@bp.route('/')
def index():
    """
    Публичная главная страница.
    Шаблон templates/public/index.html ожидает переменную `agency`.
    Значения берутся из current_app.config с безопасными дефолтами.
    """
    agency_info = {
        'name': 'ООО "Коллекторское Агентство Финансовых Решений"',
        'inn': '1234567890',
        'ogrn': '1234567890123',
        'legal_address': 'г. Москва, ул. Примерная, д. 123',
        'phone': '+7 (495) 123-45-67',
        'email': 'info@example.com',
        'fedresurs_link': 'https://fedresurs.ru/',
        'working_hours': 'Пн-Пт: 9:00-18:00'
    }
    return render_template('public/index.html', agency=agency_info)