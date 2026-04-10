import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import inspect

def check_database():
    """Проверяем структуру базы данных"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Проверяем структуру базы данных...")
        
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"📊 Таблицы в базе данных ({len(tables)}):")
        for table in tables:
            print(f"   📋 {table}")
            columns = inspector.get_columns(table)
            for column in columns:
                print(f"      └─ {column['name']} ({column['type']})")
        
        # Проверяем существующие модели
        print("\n🔎 Проверяем модели Flask-SQLAlchemy...")
        try:
            from app.models import User, Debtor
            print("✅ Модели импортированы успешно")
        except Exception as e:
            print(f"❌ Ошибка импорта моделей: {e}")

if __name__ == '__main__':
    check_database()