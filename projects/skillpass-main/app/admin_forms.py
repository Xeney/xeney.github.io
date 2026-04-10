from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class AnswerForm(FlaskForm):
    """Форма для ответа"""
    text = StringField('Текст ответа', validators=[DataRequired(), Length(max=200)])
    is_correct = BooleanField('Правильный ответ')

class QuestionForm(FlaskForm):
    """Форма для вопроса с ответами"""
    test_id = SelectField('Тест', coerce=int, validators=[DataRequired()])
    text = TextAreaField('Текст вопроса', validators=[DataRequired()])
    
    # Ответы
    answer_1 = StringField('Ответ 1', validators=[DataRequired(), Length(max=200)])
    answer_2 = StringField('Ответ 2', validators=[DataRequired(), Length(max=200)])
    answer_3 = StringField('Ответ 3', validators=[DataRequired(), Length(max=200)])
    answer_4 = StringField('Ответ 4', validators=[DataRequired(), Length(max=200)])
    
    correct_1 = BooleanField('Правильный 1')
    correct_2 = BooleanField('Правильный 2')
    correct_3 = BooleanField('Правильный 3')
    correct_4 = BooleanField('Правильный 4')
    
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        
        # Проверяем, что хотя бы один ответ правильный
        has_correct = any([
            self.correct_1.data,
            self.correct_2.data,
            self.correct_3.data,
            self.correct_4.data
        ])
        
        if not has_correct:
            self.correct_1.errors.append('Должен быть хотя бы один правильный ответ')
            return False
        
        return True

class TestForm(FlaskForm):
    """Форма для теста"""
    step_id = SelectField('Шаг', coerce=int, validators=[DataRequired()])
    title = StringField('Название теста', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание', validators=[Optional()])
    passing_score = IntegerField('Проходной балл (%)', 
                               validators=[DataRequired(), NumberRange(min=1, max=100)],
                               default=80)
    xp_reward = IntegerField('Награда XP', 
                            validators=[DataRequired(), NumberRange(min=0)],
                            default=50)
    
    def validate_title(self, field):
        if not field.data:
            raise ValidationError('Название теста обязательно')

class PathForm(FlaskForm):
    """Форма для пути обучения"""
    title = StringField('Название пути', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    difficulty = SelectField('Сложность', 
                           choices=[
                               ('beginner', '🌱 Начинающий'),
                               ('intermediate', '📊 Средний'),
                               ('advanced', '🚀 Продвинутый')
                           ],
                           validators=[DataRequired()])

class StageForm(FlaskForm):
    """Форма для этапа"""
    path_id = SelectField('Путь', coerce=int, validators=[DataRequired()])
    title = StringField('Название этапа', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание', validators=[Optional()])
    order_index = IntegerField('Порядковый номер', 
                              validators=[DataRequired(), NumberRange(min=0)],
                              default=0)

class StepForm(FlaskForm):
    """Форма для шага"""
    stage_id = SelectField('Этап', coerce=int, validators=[DataRequired()])
    title = StringField('Название шага', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    type = SelectField('Тип шага',
                      choices=[
                          ('theory', '📖 Теория'),
                          ('test', '✅ Тест')
                      ],
                      validators=[DataRequired()])
    xp_reward = IntegerField('Награда XP',
                            validators=[DataRequired(), NumberRange(min=0)],
                            default=10)
    order_index = IntegerField('Порядковый номер',
                              validators=[DataRequired(), NumberRange(min=0)],
                              default=0)