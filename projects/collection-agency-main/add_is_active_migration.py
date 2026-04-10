import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

def add_is_active_column():
    """Добавляет колонку is_active в таблицу пользователей"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Добавление поля is_active в таблицу user...")
        
        try:
            # Используем правильный метод для выполнения SQL
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE user ADD COLUMN is_active BOOLEAN DEFAULT TRUE'))
                conn.commit()
            
            print("✅ Поле is_active успешно добавлено!")
            
            # Проверяем
            from app.models import User
            users = User.query.all()
            for user in users:
                print(f"👤 {user.username}: is_active = {getattr(user, 'is_active', 'NOT SET')}")
                
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("ℹ️ Возможно, поле уже существует")

if __name__ == '__main__':
    add_is_active_column()