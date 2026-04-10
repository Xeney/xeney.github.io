from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import url_for
import math

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    profile = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')
    xp_logs = db.relationship('XPLog', backref='user', lazy='dynamic')
    progress = db.relationship('UserProgress', backref='user', lazy='dynamic')
    saved_paths = db.relationship('SavedPath', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def full_name(self):
        if self.profile.first_name or self.profile.last_name:
            return f"{self.profile.first_name} {self.profile.last_name}".strip()
        return self.profile.username

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    
    # Основная информация
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(100), default='')
    last_name = db.Column(db.String(100), default='')
    gender = db.Column(db.String(10), default='')  # male, female, other
    birth_date = db.Column(db.Date, nullable=True)
    
    # Контактная информация
    phone = db.Column(db.String(20), default='')
    country = db.Column(db.String(100), default='')
    city = db.Column(db.String(100), default='')
    
    # Соцсети (храним как JSON)
    social_links = db.Column(db.JSON, default=list)
    
    # Системная информация
    xp = db.Column(db.Integer, default=0)
    bio = db.Column(db.Text, default='')
    is_public = db.Column(db.Boolean, default=True)
    avatar = db.Column(db.String(200), default='default-avatar.png')
    
    @property
    def level(self):
        return int(math.sqrt(self.xp)) + 1 if self.xp else 1
    
    @property
    def avatar_url(self):
        if self.avatar and self.avatar != 'default-avatar.png':
            return url_for('static', filename=f'uploads/avatars/{self.avatar}')
        return url_for('static', filename='img/default-avatar.png')
    
    @property
    def age(self):
        if self.birth_date:
            today = datetime.today().date()
            age = today.year - self.birth_date.year
            # Проверяем, был ли уже день рождения в этом году
            if today.month < self.birth_date.month or (today.month == self.birth_date.month and today.day < self.birth_date.day):
                age -= 1
            return age
        return None
    
    @property
    def gender_display(self):
        genders = {
            'male': 'Мужской',
            'female': 'Женский',
            'other': 'Другой'
        }
        return genders.get(self.gender, 'Не указан')
    
    @property
    def role_display(self):
        user = User.query.get(self.user_id)
        if user:
            return 'Администратор' if user.role == 'admin' else 'Студент'
        return 'Студент'

class SocialLink(db.Model):
    """Модель для соцсетей"""
    __tablename__ = 'social_links'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    platform = db.Column(db.String(50))  # vk, telegram, github, etc.
    url = db.Column(db.String(200))
    username = db.Column(db.String(100))
    
    @property
    def icon(self):
        icons = {
            'vk': 'bi-vk',
            'telegram': 'bi-telegram',
            'github': 'bi-github',
            'gitlab': 'bi-gitlab',
            'linkedin': 'bi-linkedin',
            'twitter': 'bi-twitter-x',
            'instagram': 'bi-instagram',
            'facebook': 'bi-facebook',
            'youtube': 'bi-youtube',
            'discord': 'bi-discord',
            'twitch': 'bi-twitch',
            'tiktok': 'bi-tiktok',
            'website': 'bi-globe'
        }
        return icons.get(self.platform, 'bi-link-45deg')
    
    @property
    def platform_display(self):
        names = {
            'vk': 'VK',
            'telegram': 'Telegram',
            'github': 'GitHub',
            'gitlab': 'GitLab',
            'linkedin': 'LinkedIn',
            'twitter': 'Twitter/X',
            'instagram': 'Instagram',
            'facebook': 'Facebook',
            'youtube': 'YouTube',
            'discord': 'Discord',
            'twitch': 'Twitch',
            'tiktok': 'TikTok',
            'website': 'Сайт'
        }
        return names.get(self.platform, 'Ссылка')
    
    @property
    def color(self):
        colors = {
            'vk': '#4C75A3',
            'telegram': '#0088cc',
            'github': '#333',
            'gitlab': '#FC6D26',
            'linkedin': '#0077b5',
            'twitter': '#000000',
            'instagram': '#E4405F',
            'facebook': '#1877F2',
            'youtube': '#FF0000',
            'discord': '#5865F2',
            'twitch': '#9146FF',
            'tiktok': '#000000',
            'website': '#6c757d'
        }
        return colors.get(self.platform, '#6c757d')

class Path(db.Model):
    __tablename__ = 'paths'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(20), default='beginner')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    stages = db.relationship('Stage', backref='path', lazy=True, cascade='all, delete-orphan', order_by='Stage.order_index')

class Stage(db.Model):
    __tablename__ = 'stages'
    id = db.Column(db.Integer, primary_key=True)
    path_id = db.Column(db.Integer, db.ForeignKey('paths.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order_index = db.Column(db.Integer, default=0)
    
    steps = db.relationship('Step', backref='stage', lazy=True, cascade='all, delete-orphan', order_by='Step.order_index')

class Step(db.Model):
    __tablename__ = 'steps'
    id = db.Column(db.Integer, primary_key=True)
    stage_id = db.Column(db.Integer, db.ForeignKey('stages.id'))
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    type = db.Column(db.String(20), default='theory')  # 'theory' or 'test'
    xp_reward = db.Column(db.Integer, default=10)
    order_index = db.Column(db.Integer, default=0)
    
    test = db.relationship('Test', backref='step', uselist=False, cascade='all, delete-orphan')

class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.Integer, db.ForeignKey('steps.id'), unique=True)
    passing_score = db.Column(db.Integer, default=80)  # процент правильных ответов
    
    questions = db.relationship('Question', backref='test', lazy=True, cascade='all, delete-orphan')

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
    text = db.Column(db.Text, nullable=False)
    order_index = db.Column(db.Integer, default=0)
    
    answers = db.relationship('Answer', backref='question', lazy=True, cascade='all, delete-orphan')

class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

class XPLog(db.Model):
    __tablename__ = 'xp_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount = db.Column(db.Integer)
    reason = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    step_id = db.Column(db.Integer, db.ForeignKey('steps.id'))
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'step_id', name='unique_user_step'),)
    
    step = db.relationship('Step')
    
class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'))
    is_correct = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'question_id', name='unique_user_question'),)
    
class SavedPath(db.Model):
    __tablename__ = 'saved_paths'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    path_id = db.Column(db.Integer, db.ForeignKey('paths.id'))
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'path_id', name='unique_user_path'),)
    
    path = db.relationship('Path')