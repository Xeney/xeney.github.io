from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User
from app.admin.forms import LoginForm

bp = Blueprint('auth', __name__)

def create_admin_user():
    """Create admin user if doesn't exist"""
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Admin user created: admin / admin123')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        # Проверяем, что пользователь активен
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Ваш аккаунт деактивирован. Обратитесь к администратору.', 'danger')
                return render_template('admin/login.html', form=form)
            
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash(f'Добро пожаловать, {user.username}!', 'success')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash('Неверный логин или пароль', 'danger')
    
    return render_template('admin/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('public.index'))