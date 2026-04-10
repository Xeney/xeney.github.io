from app import create_app, db
from app.models import User, Profile

def init_db():
    app = create_app()
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        
        # Проверяем, есть ли уже администратор
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            # Создаем админа
            admin = User(email='admin@example.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.flush()
            
            profile = Profile(user_id=admin.id, username='admin')
            db.session.add(profile)
            db.session.commit()
            
            print('✓ Администратор создан:')
            print('  Email: admin@example.com')
            print('  Пароль: admin123')
        else:
            print('✓ Администратор уже существует')
        
        print('✓ База данных инициализирована')

if __name__ == '__main__':
    init_db()