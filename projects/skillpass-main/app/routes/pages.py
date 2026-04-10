from flask import Blueprint, render_template

bp = Blueprint('pages', __name__)

@bp.route('/about')
def about():
    """Страница 'О проекте'"""
    return render_template('pages/about.html', title='О проекте')

@bp.route('/how-it-works')
def how_it_works():
    """Страница 'Как это работает'"""
    return render_template('pages/how_it_works.html', title='Как это работает')

@bp.route('/help')
def help():
    """Страница 'Помощь'"""
    return render_template('pages/help.html', title='Помощь')

@bp.route('/contacts')
def contacts():
    """Страница 'Контакты'"""
    return render_template('pages/contacts.html', title='Контакты')

@bp.route('/terms')
def terms():
    """Страница 'Пользовательское соглашение'"""
    return render_template('pages/terms.html', title='Пользовательское соглашение')

@bp.route('/privacy')
def privacy():
    """Страница 'Политика конфиденциальности'"""
    return render_template('pages/privacy.html', title='Политика конфиденциальности')