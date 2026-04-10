from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, DateField, DecimalField, SelectField, TextAreaField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, EqualTo
from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, DateField, DecimalField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, EqualTo

class DocumentUploadForm(FlaskForm):
    """
    Форма для загрузки документов к должнику.
    Поле называется `file` — шаблоны ожидают form.file
    """
    file = FileField('Файл', validators=[
        FileRequired(message='Выберите файл для загрузки'),
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'xls', 'xlsx', 'txt'], 'Недопустимый формат файла')
    ])
    description = TextAreaField('Описание', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Загрузить')

# Остальные формы без изменений, но убедитесь, что имена полей соответствуют шаблонам
class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class DebtorForm(FlaskForm):
    full_name = StringField('ФИО', validators=[DataRequired(), Length(max=255)])
    birth_date = DateField('Дата рождения', format='%Y-%m-%d', validators=[Optional()])
    passport_data = StringField('Паспорт', validators=[Optional(), Length(max=300)])
    contract_number = StringField('Номер договора', validators=[DataRequired(), Length(max=128)])
    debt_amount = DecimalField('Сумма долга', validators=[DataRequired()])
    bank_name = StringField('Банк', validators=[DataRequired(), Length(max=255)])
    status = SelectField('Статус', choices=[('active', 'Активный'), ('archived', 'Архив'), ('paid', 'Погашен')], default='active')
    submit = SubmitField('Сохранить')

class InteractionForm(FlaskForm):
    interaction_type = SelectField('Тип взаимодействия', choices=[('call', 'Звонок'), ('sms', 'SMS'), ('email', 'Email'), ('meeting', 'Встреча')], validators=[DataRequired()])
    date = StringField('Дата', validators=[DataRequired()], description='Формат: ДД.MM.YYYY')
    time = StringField('Время', validators=[DataRequired()], description='Формат: ЧЧ:ММ')
    result = StringField('Результат', validators=[DataRequired(), Length(max=200)])
    comment = TextAreaField('Комментарий', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Добавить')

class ImportForm(FlaskForm):
    file = FileField('Excel файл', validators=[
        FileRequired('Выберите файл для загрузки'),
        FileAllowed(['xlsx', 'xls'], 'Только Excel файлы (.xlsx, .xls)')
    ])
    submit = SubmitField('Импортировать')

class UserForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Роль', choices=[('admin','Администратор'),('manager','Менеджер'),('operator','Оператор')], validators=[DataRequired()])
    submit = SubmitField('Создать пользователя')

class EditUserForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=3, max=64)])
    role = SelectField('Роль', choices=[('admin','Администратор'),('manager','Менеджер'),('operator','Оператор')], validators=[DataRequired()])
    submit = SubmitField('Обновить пользователя')

class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('Новый пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('new_password', message='Пароли должны совпадать')])
    submit = SubmitField('Сменить пароль')

class DocumentUploadForm(FlaskForm):
    """
    Форма для загрузки документов к должнику.
    Поле называется `file` — это ожидает шаблон debtor_detail.html.
    """
    file = FileField(
        'Файл',
        validators=[
            FileRequired(message='Выберите файл для загрузки'),
            FileAllowed(
                ['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'xls', 'xlsx', 'txt'],
                'Недопустимый формат файла'
            )
        ]
    )
    description = TextAreaField('Описание', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Загрузить')