from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request, flash
from wtforms import PasswordField, SelectField, TextAreaField
from wtforms.validators import Optional
from app import db
from app.models import User, Profile, Path, Stage, Step, Test, Question, Answer, XPLog, SavedPath, UserAnswer
from app.admin_forms import TestForm, QuestionForm, PathForm, StageForm, StepForm

class AdminHomeView(AdminIndexView):
    """Главная страница админки с дашбордом"""
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin():
            return redirect(url_for('auth.login'))
        
        stats = {
            'users': User.query.count(),
            'paths': Path.query.count(),
            'stages': Stage.query.count(),
            'steps': Step.query.count(),
            'tests': Test.query.count(),
            'questions': Question.query.count(),
            'xp_logs': XPLog.query.count()
        }
        
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        recent_xp = XPLog.query.order_by(XPLog.timestamp.desc()).limit(5).all()
        
        return self.render('admin/dashboard.html', 
                          stats=stats, 
                          recent_users=recent_users,
                          recent_xp=recent_xp)

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))
    
    # Настройки отображения
    can_view_details = True
    can_export = True
    export_types = ['csv', 'xls']
    page_size = 20
    
    # Bootstrap классы для форм
    form_widget_args = {
        'description': {'rows': 3},
        'content': {'rows': 10},
        'bio': {'rows': 3},
    }

class UserView(SecureModelView):
    """Управление пользователями"""
    can_create = False
    can_delete = False
    
    column_labels = {
        'email': 'Email',
        'role': 'Роль',
        'created_at': 'Дата регистрации',
        'profile.username': 'Имя пользователя',
        'profile.xp': 'Опыт',
        'profile.level': 'Уровень'
    }
    
    column_list = ['email', 'profile.username', 'role', 'profile.level', 'profile.xp', 'created_at']
    column_searchable_list = ['email', 'profile.username']
    column_filters = ['role', 'created_at']
    column_default_sort = ('created_at', True)
    
    form_extra_fields = {
        'password': PasswordField('Новый пароль')
    }
    form_columns = ['role', 'password']
    
    # Кастомные колонки
    column_formatters = {
        'profile.level': lambda v, c, m, p: f'🎯 {m.profile.level}' if m.profile else '-',
        'profile.xp': lambda v, c, m, p: f'⚡ {m.profile.xp}' if m.profile else '-',
        'role': lambda v, c, m, p: f'👑 {m.role}' if m.role == 'admin' else f'👤 {m.role}'
    }
    
    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.set_password(form.password.data)

class ProfileView(SecureModelView):
    """Управление профилями"""
    endpoint = 'admin_profiles'
    
    column_labels = {
        'username': 'Имя пользователя',
        'xp': 'Опыт',
        'level': 'Уровень',
        'is_public': 'Публичный',
        'bio': 'О себе',
        'user.email': 'Email',
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'country': 'Страна',
        'city': 'Город'
    }
    
    column_list = ['username', 'user.email', 'first_name', 'last_name', 'level', 'xp', 'is_public']
    column_searchable_list = ['username', 'user.email', 'first_name', 'last_name']
    column_filters = ['is_public', 'country', 'city']
    
    form_columns = ['first_name', 'last_name', 'bio', 'country', 'city', 'phone', 'is_public']
    
    column_formatters = {
        'level': lambda v, c, m, p: f'<span class="badge bg-primary">Level {m.level}</span>',
        'xp': lambda v, c, m, p: f'<span class="badge bg-success">{m.xp} XP</span>',
        'is_public': lambda v, c, m, p: '✅ Да' if m.is_public else '❌ Нет'
    }

class PathView(SecureModelView):
    """Управление путями обучения"""
    endpoint = 'admin_paths'
    
    column_labels = {
        'title': 'Название',
        'difficulty': 'Сложность',
        'stages': 'Этапов',
        'created_at': 'Дата создания'
    }
    
    column_list = ['title', 'difficulty', 'stages', 'created_at']
    column_searchable_list = ['title', 'description']
    column_filters = ['difficulty']
    
    form = PathForm
    
    column_formatters = {
        'difficulty': lambda v, c, m, p: {
            'beginner': '<span class="badge bg-success">🌱 Начинающий</span>',
            'intermediate': '<span class="badge bg-warning text-dark">📊 Средний</span>',
            'advanced': '<span class="badge bg-danger">🚀 Продвинутый</span>'
        }.get(m.difficulty, m.difficulty),
        'stages': lambda v, c, m, p: f'<span class="badge bg-info">{len(m.stages)}</span>'
    }

class StageView(SecureModelView):
    """Управление этапами"""
    endpoint = 'admin_stages'
    
    column_labels = {
        'title': 'Название',
        'path': 'Путь',
        'order_index': 'Порядок',
        'steps': 'Шагов'
    }
    
    column_list = ['title', 'path', 'order_index', 'steps']
    column_filters = ['path']
    
    form = StageForm
    
    def create_form(self):
        form = super().create_form()
        form.path_id.choices = [(p.id, p.title) for p in Path.query.all()]
        return form
    
    column_formatters = {
        'steps': lambda v, c, m, p: f'<span class="badge bg-info">{len(m.steps)}</span>'
    }

class StepView(SecureModelView):
    """Управление шагами"""
    endpoint = 'admin_steps'
    
    column_labels = {
        'title': 'Название',
        'stage': 'Этап',
        'type': 'Тип',
        'xp_reward': 'XP',
        'order_index': 'Порядок'
    }
    
    column_list = ['title', 'stage', 'type', 'xp_reward', 'order_index']
    column_filters = ['type', 'stage']
    
    form = StepForm
    
    def create_form(self):
        form = super().create_form()
        form.stage_id.choices = [(s.id, f"{s.path.title} - {s.title}") for s in Stage.query.all()]
        return form
    
    column_formatters = {
        'type': lambda v, c, m, p: {
            'theory': '<span class="badge bg-info">📖 Теория</span>',
            'test': '<span class="badge bg-warning text-dark">✅ Тест</span>'
        }.get(m.type, m.type),
        'xp_reward': lambda v, c, m, p: f'<span class="badge bg-success">+{m.xp_reward} XP</span>'
    }

class TestView(SecureModelView):
    """Управление тестами"""
    endpoint = 'admin_tests'
    
    column_labels = {
        'step': 'Шаг',
        'passing_score': 'Проходной балл',
        'questions': 'Вопросов'
    }
    
    column_list = ['step', 'passing_score', 'questions']
    
    create_template = 'admin/test_create.html'
    edit_template = 'admin/test_create.html'
    
    form = TestForm
    
    def create_form(self):
        form = super().create_form()
        form.step_id.choices = [(s.id, f"{s.stage.path.title} - {s.stage.title} - {s.title}") 
                               for s in Step.query.filter_by(type='test').all()]
        return form
    
    column_formatters = {
        'passing_score': lambda v, c, m, p: f'<span class="badge bg-warning text-dark">{m.passing_score}%</span>',
        'questions': lambda v, c, m, p: f'<span class="badge bg-info">{len(m.questions)}</span>'
    }

class QuestionView(SecureModelView):
    """Управление вопросами"""
    endpoint = 'admin_questions'
    
    column_labels = {
        'text': 'Вопрос',
        'test': 'Тест',
        'answers': 'Ответов'
    }
    
    column_list = ['text', 'test', 'answers']
    column_searchable_list = ['text']
    
    create_template = 'admin/question_create.html'
    edit_template = 'admin/question_create.html'
    
    form = QuestionForm
    
    def create_form(self):
        form = super().create_form()
        form.test_id.choices = [(t.id, f"{t.step.stage.path.title} - {t.step.title}") 
                               for t in Test.query.all()]
        return form
    
    column_formatters = {
        'answers': lambda v, c, m, p: f'<span class="badge bg-info">{len(m.answers)}</span>'
    }

class AnswerView(SecureModelView):
    """Управление ответами"""
    endpoint = 'admin_answers'
    
    column_labels = {
        'text': 'Ответ',
        'question': 'Вопрос',
        'is_correct': 'Правильный'
    }
    
    column_list = ['text', 'question', 'is_correct']
    column_filters = ['is_correct']
    
    column_formatters = {
        'is_correct': lambda v, c, m, p: '✅ Да' if m.is_correct else '❌ Нет'
    }

class XPLogView(SecureModelView):
    """Логи XP"""
    endpoint = 'admin_xp_logs'
    can_create = False
    can_edit = False
    can_delete = False
    
    column_labels = {
        'user.email': 'Пользователь',
        'amount': 'XP',
        'reason': 'Причина',
        'timestamp': 'Дата'
    }
    
    column_list = ['user.email', 'amount', 'reason', 'timestamp']
    column_filters = ['timestamp']
    column_default_sort = ('timestamp', True)
    
    column_formatters = {
        'amount': lambda v, c, m, p: f'<span class="badge bg-success">+{m.amount}</span>',
        'timestamp': lambda v, c, m, p: m.timestamp.strftime('%d.%m.%Y %H:%M') if m.timestamp else '-'
    }

class SavedPathView(SecureModelView):
    """Сохранённые пути"""
    endpoint = 'admin_saved_paths'
    can_create = False
    can_edit = False
    
    column_labels = {
        'user.email': 'Пользователь',
        'path.title': 'Путь',
        'saved_at': 'Дата сохранения'
    }
    
    column_list = ['user.email', 'path.title', 'saved_at']
    column_filters = ['saved_at']
    
    column_formatters = {
        'saved_at': lambda v, c, m, p: m.saved_at.strftime('%d.%m.%Y %H:%M') if m.saved_at else '-'
    }

class UserAnswerView(SecureModelView):
    """Ответы пользователей"""
    endpoint = 'admin_user_answers'
    can_create = False
    can_edit = False
    can_delete = False
    
    column_labels = {
        'user.email': 'Пользователь',
        'question.text': 'Вопрос',
        'answer.text': 'Ответ',
        'is_correct': 'Правильно',
        'created_at': 'Дата'
    }
    
    column_list = ['user.email', 'question.text', 'answer.text', 'is_correct', 'created_at']
    column_filters = ['is_correct', 'created_at']
    
    column_formatters = {
        'is_correct': lambda v, c, m, p: '✅ Да' if m.is_correct else '❌ Нет',
        'created_at': lambda v, c, m, p: m.created_at.strftime('%d.%m.%Y %H:%M') if m.created_at else '-'
    }

def init_admin(app):
    admin = Admin(app, 
                  name='SkillPass Администрирование', 
                  template_mode='bootstrap4',
                  index_view=AdminHomeView(name='Главная'),
                  base_template='admin/master.html')
    
    # Добавляем представления
    admin.add_view(UserView(User, db.session, name='👤 Пользователи', category='Управление', endpoint='admin_users'))
    admin.add_view(ProfileView(Profile, db.session, name='📋 Профили', category='Управление', endpoint='admin_profiles'))
    
    admin.add_view(PathView(Path, db.session, name='🗺️ Пути', category='Обучение', endpoint='admin_paths'))
    admin.add_view(StageView(Stage, db.session, name='📦 Этапы', category='Обучение', endpoint='admin_stages'))
    admin.add_view(StepView(Step, db.session, name='📚 Шаги', category='Обучение', endpoint='admin_steps'))
    
    admin.add_view(TestView(Test, db.session, name='📝 Тесты', category='Тестирование', endpoint='admin_tests'))
    admin.add_view(QuestionView(Question, db.session, name='❓ Вопросы', category='Тестирование', endpoint='admin_questions'))
    admin.add_view(AnswerView(Answer, db.session, name='💡 Ответы', category='Тестирование', endpoint='admin_answers'))
    
    admin.add_view(XPLogView(XPLog, db.session, name='📊 Логи XP', category='Статистика', endpoint='admin_xp_logs'))
    admin.add_view(SavedPathView(SavedPath, db.session, name='🔖 Сохранения', category='Статистика', endpoint='admin_saved_paths'))
    admin.add_view(UserAnswerView(UserAnswer, db.session, name='📝 Ответы пользователей', category='Статистика', endpoint='admin_user_answers'))