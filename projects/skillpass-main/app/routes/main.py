from flask import Blueprint, render_template
from app.models import Path, User, Step, XPLog
from sqlalchemy import func
from app import db
from app.models import Profile

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    paths = Path.query.all()
    
    # Статистика платформы
    stats = {
        'users': User.query.count(),
        'paths': Path.query.count(),
        'steps': Step.query.count(),
        'xp_count': db.session.query(func.sum(XPLog.amount)).scalar() or 0
    }
    
    # Популярные пути (с сортировкой по количеству студентов)
    popular_paths = Path.query.limit(3).all()
    
    # Топ пользователей
    top_users = User.query.join(User.profile).order_by(Profile.xp.desc()).limit(5).all()
    
    return render_template('index.html', 
                         paths=paths, 
                         stats=stats,
                         popular_paths=popular_paths,
                         top_users=top_users)