from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Profile

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный email или пароль', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        # Перенаправляем на запрошенную страницу или на главную
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
        
        flash(f'Добро пожаловать, {user.profile.username}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Вход', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, role='student')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()  # Чтобы получить user.id

        profile = Profile(user_id=user.id, username=form.username.data)
        db.session.add(profile)
        db.session.commit()

        flash('Поздравляем, вы зарегистрированы! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Регистрация', form=form)