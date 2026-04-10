from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, SelectField, DateField, FieldList, FormField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, URL
from app.models import User, Profile
from datetime import date

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    accept_tos = BooleanField('Я согласен на обработку персональных данных (152-ФЗ)', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.join(User.profile).filter(Profile.username == username.data).first()
        if user is not None:
            raise ValidationError('Это имя пользователя уже занято.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот email уже зарегистрирован.')

class SocialLinkForm(FlaskForm):
    """Форма для одной соцсети"""
    platform = SelectField('Платформа', choices=[
        ('', '-- Выберите --'),
        ('vk', 'VK'),
        ('telegram', 'Telegram'),
        ('github', 'GitHub'),
        ('gitlab', 'GitLab'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('discord', 'Discord'),
        ('twitch', 'Twitch'),
        ('tiktok', 'TikTok'),
        ('website', 'Личный сайт')
    ], validators=[Optional()])
    url = StringField('Ссылка', validators=[Optional(), URL()])
    username = StringField('Имя пользователя', validators=[Optional(), Length(max=100)])

class ProfileEditForm(FlaskForm):
    # Личная информация
    first_name = StringField('Имя', validators=[Optional(), Length(max=100)])
    last_name = StringField('Фамилия', validators=[Optional(), Length(max=100)])
    gender = SelectField('Пол', choices=[
        ('', '-- Не указан --'),
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('other', 'Другой')
    ], validators=[Optional()])
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[Optional()])
    
    # Контактная информация
    phone = StringField('Номер телефона', validators=[Optional(), Length(max=20)])
    country = StringField('Страна', validators=[Optional(), Length(max=100)])
    city = StringField('Город', validators=[Optional(), Length(max=100)])
    
    # О себе
    bio = TextAreaField('О себе', validators=[Optional(), Length(max=500)])
    
    # Соцсети - теперь 5 отдельных полей
    social_1_platform = SelectField('Соцсеть 1', choices=[
        ('', '-- Выберите --'),
        ('vk', 'VK'),
        ('telegram', 'Telegram'),
        ('github', 'GitHub'),
        ('gitlab', 'GitLab'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('discord', 'Discord'),
        ('twitch', 'Twitch'),
        ('tiktok', 'TikTok'),
        ('website', 'Личный сайт')
    ], validators=[Optional()])
    social_1_url = StringField('Ссылка 1', validators=[Optional(), URL()])
    social_1_username = StringField('Имя пользователя 1', validators=[Optional(), Length(max=100)])
    
    social_2_platform = SelectField('Соцсеть 2', choices=[
        ('', '-- Выберите --'),
        ('vk', 'VK'),
        ('telegram', 'Telegram'),
        ('github', 'GitHub'),
        ('gitlab', 'GitLab'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('discord', 'Discord'),
        ('twitch', 'Twitch'),
        ('tiktok', 'TikTok'),
        ('website', 'Личный сайт')
    ], validators=[Optional()])
    social_2_url = StringField('Ссылка 2', validators=[Optional(), URL()])
    social_2_username = StringField('Имя пользователя 2', validators=[Optional(), Length(max=100)])
    
    social_3_platform = SelectField('Соцсеть 3', choices=[
        ('', '-- Выберите --'),
        ('vk', 'VK'),
        ('telegram', 'Telegram'),
        ('github', 'GitHub'),
        ('gitlab', 'GitLab'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('discord', 'Discord'),
        ('twitch', 'Twitch'),
        ('tiktok', 'TikTok'),
        ('website', 'Личный сайт')
    ], validators=[Optional()])
    social_3_url = StringField('Ссылка 3', validators=[Optional(), URL()])
    social_3_username = StringField('Имя пользователя 3', validators=[Optional(), Length(max=100)])
    
    social_4_platform = SelectField('Соцсеть 4', choices=[
        ('', '-- Выберите --'),
        ('vk', 'VK'),
        ('telegram', 'Telegram'),
        ('github', 'GitHub'),
        ('gitlab', 'GitLab'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('discord', 'Discord'),
        ('twitch', 'Twitch'),
        ('tiktok', 'TikTok'),
        ('website', 'Личный сайт')
    ], validators=[Optional()])
    social_4_url = StringField('Ссылка 4', validators=[Optional(), URL()])
    social_4_username = StringField('Имя пользователя 4', validators=[Optional(), Length(max=100)])
    
    social_5_platform = SelectField('Соцсеть 5', choices=[
        ('', '-- Выберите --'),
        ('vk', 'VK'),
        ('telegram', 'Telegram'),
        ('github', 'GitHub'),
        ('gitlab', 'GitLab'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('discord', 'Discord'),
        ('twitch', 'Twitch'),
        ('tiktok', 'TikTok'),
        ('website', 'Личный сайт')
    ], validators=[Optional()])
    social_5_url = StringField('Ссылка 5', validators=[Optional(), URL()])
    social_5_username = StringField('Имя пользователя 5', validators=[Optional(), Length(max=100)])
    
    # Настройки приватности
    is_public = BooleanField('Публичный профиль')
    
    # Аватар
    avatar = FileField('Аватар', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Только изображения!')
    ])
    
    submit = SubmitField('Сохранить изменения')

class SearchForm(FlaskForm):
    """Форма поиска пользователей"""
    query = StringField('Поиск', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Найти')