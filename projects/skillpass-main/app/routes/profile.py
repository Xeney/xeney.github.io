from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Profile, User, UserProgress, Step, Path
from app.forms import ProfileEditForm, SearchForm
import os
from PIL import Image
import uuid
from datetime import datetime

bp = Blueprint('profile', __name__, url_prefix='/profile')

def save_avatar(form_avatar):
    """Сохраняет аватарку и возвращает имя файла"""
    random_hex = uuid.uuid4().hex
    _, f_ext = os.path.splitext(form_avatar.filename)
    avatar_filename = random_hex + f_ext
    
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
    os.makedirs(upload_path, exist_ok=True)
    
    avatar_path = os.path.join(upload_path, avatar_filename)
    
    try:
        output_size = (200, 200)
        i = Image.open(form_avatar)
        i.thumbnail(output_size)
        i.save(avatar_path, optimize=True, quality=85)
        return avatar_filename
    except Exception as e:
        print(f"Error saving avatar: {e}")
        return None

@bp.route('/<username>')
def view(username):
    """Просмотр профиля пользователя с ограничениями для неавторизованных"""
    user = User.query.join(User.profile).filter(Profile.username == username).first_or_404()
    
    # Проверка приватности
    if not user.profile.is_public and (not current_user.is_authenticated or current_user.id != user.id):
        abort(403)
    
    # Определяем, показывать ли полную информацию
    show_full_info = current_user.is_authenticated and (user.profile.is_public or current_user.id == user.id)
    
    # Базовые данные, которые видят все
    profile_data = {
        'username': user.profile.username,
        'first_name': user.profile.first_name,
        'last_name': user.profile.last_name,
        'full_name': user.full_name,
        'level': user.profile.level,
        'xp': user.profile.xp,
        'bio': user.profile.bio,
        'avatar': user.profile.avatar,
        'avatar_url': user.profile.avatar_url,
        'is_public': user.profile.is_public,
        'is_owner': current_user.is_authenticated and current_user.id == user.id,
        'is_admin': user.is_admin(),
        'created_at': user.created_at,
        'registered_date': user.created_at.strftime('%d.%m.%Y')
    }
    
    # Данные, которые видят только авторизованные (или владелец приватного профиля)
    completed_steps = []
    if show_full_info:
        completed_steps = Step.query.join(UserProgress).filter(
            UserProgress.user_id == user.id, 
            UserProgress.completed == True
        ).order_by(UserProgress.completed_at.desc()).all()
    
    return render_template('profile/view.html', 
                          profile_user=user,
                          profile_data=profile_data,
                          show_full_info=show_full_info,
                          completed_steps=completed_steps)

@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """Редактирование профиля (только для авторизованных)"""
    form = ProfileEditForm()
    
    if form.validate_on_submit():
        profile = current_user.profile
        
        # Личная информация
        profile.first_name = form.first_name.data
        profile.last_name = form.last_name.data
        profile.gender = form.gender.data
        profile.birth_date = form.birth_date.data
        
        # Контактная информация
        profile.phone = form.phone.data
        profile.country = form.country.data
        profile.city = form.city.data
        
        # О себе
        profile.bio = form.bio.data
        profile.is_public = form.is_public.data
        
        # Соцсети - собираем в список, пропуская пустые
        social_links = []
        for i in range(1, 6):
            platform = getattr(form, f'social_{i}_platform').data
            url = getattr(form, f'social_{i}_url').data
            username = getattr(form, f'social_{i}_username').data
            
            # Сохраняем только если заполнена платформа и есть хотя бы url или username
            if platform and (url or username):
                # Если нет url, но есть username, формируем url автоматически
                if not url and username:
                    url = auto_generate_url(platform, username)
                
                social_links.append({
                    'platform': platform,
                    'url': url,
                    'username': username or extract_username_from_url(platform, url)
                })
        
        profile.social_links = social_links
        
        # Обрабатываем аватарку если загружена
        if form.avatar.data:
            try:
                if profile.avatar and profile.avatar != 'default-avatar.png':
                    old_avatar_path = os.path.join(current_app.root_path, 
                                                  'static', 'uploads', 'avatars', 
                                                  profile.avatar)
                    if os.path.exists(old_avatar_path):
                        os.remove(old_avatar_path)
                
                avatar_filename = save_avatar(form.avatar.data)
                if avatar_filename:
                    profile.avatar = avatar_filename
                    flash('Аватарка успешно обновлена!', 'success')
                else:
                    flash('Ошибка при обработке изображения', 'danger')
                
            except Exception as e:
                flash('Ошибка при загрузке аватарки. Попробуйте другой файл.', 'danger')
                print(f"Error saving avatar: {e}")
        
        db.session.commit()
        flash('Профиль обновлен', 'success')
        return redirect(url_for('profile.view', username=profile.username))
    
    elif request.method == 'GET':
        profile = current_user.profile
        
        # Личная информация
        form.first_name.data = profile.first_name
        form.last_name.data = profile.last_name
        form.gender.data = profile.gender
        form.birth_date.data = profile.birth_date
        
        # Контактная информация
        form.phone.data = profile.phone
        form.country.data = profile.country
        form.city.data = profile.city
        
        # О себе
        form.bio.data = profile.bio
        form.is_public.data = profile.is_public
        
        # Соцсети
        social_links = profile.social_links or []
        for i in range(len(social_links)):
            if i < 5:
                link = social_links[i]
                getattr(form, f'social_{i+1}_platform').data = link.get('platform', '')
                getattr(form, f'social_{i+1}_url').data = link.get('url', '')
                getattr(form, f'social_{i+1}_username').data = link.get('username', '')
    
    return render_template('profile/edit.html', title='Редактирование профиля', form=form)

def auto_generate_url(platform, username):
    """Автоматически генерирует URL для популярных платформ"""
    urls = {
        'vk': f'https://vk.com/{username}',
        'telegram': f'https://t.me/{username}',
        'github': f'https://github.com/{username}',
        'gitlab': f'https://gitlab.com/{username}',
        'linkedin': f'https://linkedin.com/in/{username}',
        'twitter': f'https://twitter.com/{username}',
        'instagram': f'https://instagram.com/{username}',
        'facebook': f'https://facebook.com/{username}',
        'youtube': f'https://youtube.com/@{username}',
        'discord': f'https://discord.com/users/{username}',
        'twitch': f'https://twitch.tv/{username}',
        'tiktok': f'https://tiktok.com/@{username}'
    }
    return urls.get(platform, '')

def extract_username_from_url(platform, url):
    """Извлекает username из URL"""
    if not url:
        return ''
    
    # Простое извлечение для популярных платформ
    if platform == 'vk' and 'vk.com/' in url:
        return url.split('vk.com/')[-1].split('/')[0]
    elif platform == 'telegram' and 't.me/' in url:
        return url.split('t.me/')[-1].split('/')[0]
    elif platform == 'github' and 'github.com/' in url:
        return url.split('github.com/')[-1].split('/')[0]
    elif platform == 'instagram' and 'instagram.com/' in url:
        return url.split('instagram.com/')[-1].split('/')[0]
    
    # Если не удалось извлечь, возвращаем последнюю часть URL
    return url.split('/')[-1]

@bp.route('/delete-avatar', methods=['POST'])
@login_required
def delete_avatar():
    """Удаляет аватарку и устанавливает дефолтную"""
    if current_user.profile.avatar and current_user.profile.avatar != 'default-avatar.png':
        avatar_path = os.path.join(current_app.root_path, 
                                  'static', 'uploads', 'avatars', 
                                  current_user.profile.avatar)
        if os.path.exists(avatar_path):
            os.remove(avatar_path)
    
    current_user.profile.avatar = 'default-avatar.png'
    db.session.commit()
    
    flash('Аватарка удалена', 'success')
    return redirect(url_for('profile.edit'))

@bp.route('/search')
def search():
    """Поиск пользователей (доступен всем, но видны только публичные профили)"""
    form = SearchForm()
    query = request.args.get('q', '')
    results = []
    
    if query and len(query) >= 2:
        # Ищем только по публичным профилям
        results = User.query.join(Profile).filter(
            db.or_(
                Profile.username.ilike(f'%{query}%'),
                Profile.first_name.ilike(f'%{query}%'),
                Profile.last_name.ilike(f'%{query}%')
            ),
            Profile.is_public == True  # Только публичные профили
        ).limit(20).all()
    
    return render_template('profile/search.html', form=form, results=results, query=query)

@bp.route('/by-email/<email>')
def view_by_email(email):
    """Просмотр профиля по email (только для публичных профилей)"""
    user = User.query.filter_by(email=email).first_or_404()
    
    # Если профиль приватный и пользователь не авторизован или не владелец
    if not user.profile.is_public and (not current_user.is_authenticated or current_user.id != user.id):
        abort(403)
    
    return redirect(url_for('profile.view', username=user.profile.username))

@bp.route('/by-id/<int:user_id>')
def view_by_id(user_id):
    """Просмотр профиля по ID (только для публичных профилей)"""
    user = User.query.get_or_404(user_id)
    
    # Если профиль приватный и пользователь не авторизован или не владелец
    if not user.profile.is_public and (not current_user.is_authenticated or current_user.id != user.id):
        abort(403)
    
    return redirect(url_for('profile.view', username=user.profile.username))

@bp.route('/leaderboard')
def leaderboard():
    """Таблица лидеров (топ 100 по XP) - доступна всем"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Топ пользователей по XP (только публичные профили)
    users = User.query.join(Profile).filter(
        Profile.is_public == True
    ).order_by(Profile.xp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('profile/leaderboard.html', users=users)