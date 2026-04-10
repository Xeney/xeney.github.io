import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import inspect

def add_debtor_status_and_documents_fixed():
    """Добавляет статус должникам и создает таблицу документов для существующей таблицы debtor"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Начало миграции для таблицы debtor...")
        
        inspector = inspect(db.engine)
        
        try:
            with db.engine.connect() as conn:
                # 1. Добавляем колонку status в таблицу debtor
                print("📝 Добавляем поле status в таблицу debtor...")
                
                # Проверяем, существует ли уже колонка status
                columns = [col['name'] for col in inspector.get_columns('debtor')]
                if 'status' not in columns:
                    conn.execute(db.text('ALTER TABLE debtor ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT "active"'))
                    print("✅ Поле status добавлено в таблицу debtor")
                else:
                    print("ℹ️ Поле status уже существует в таблице debtor")
                
                # 2. Создаем таблицу documents
                print("📄 Создаем таблицу documents...")
                
                if 'documents' not in inspector.get_table_names():
                    conn.execute(db.text("""
                        CREATE TABLE documents (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            debtor_id INTEGER NOT NULL,
                            filename_original TEXT NOT NULL,
                            filename_disk TEXT NOT NULL,
                            content_type TEXT,
                            size INTEGER,
                            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                            uploaded_by INTEGER,
                            FOREIGN KEY (debtor_id) REFERENCES debtor(id) ON DELETE CASCADE,
                            FOREIGN KEY (uploaded_by) REFERENCES user(id)
                        )
                    """))
                    print("✅ Таблица documents создана")
                else:
                    print("ℹ️ Таблица documents уже существует")
                
                # 3. Создаем индекс для оптимизации запросов
                print("⚡ Создаем индекс для documents...")
                
                # Проверяем существование индекса
                indexes = inspector.get_indexes('documents')
                index_names = [idx['name'] for idx in indexes] if indexes else []
                
                if 'ix_documents_debtor_id' not in index_names:
                    conn.execute(db.text('CREATE INDEX ix_documents_debtor_id ON documents(debtor_id)'))
                    print("✅ Индекс ix_documents_debtor_id создан")
                else:
                    print("ℹ️ Индекс ix_documents_debtor_id уже существует")
                
                conn.commit()
            
            print("✅ Миграция успешно выполнена!")
            
            # Проверяем результат
            print("🔍 Проверяем результаты миграции...")
            
            # Проверяем debtor
            from app.models import Debtor
            debtors = Debtor.query.limit(3).all()
            print(f"📊 Проверка первых 3 должников:")
            for debtor in debtors:
                status = getattr(debtor, 'status', 'NOT SET')
                print(f"   👤 {debtor.full_name}: status = {status}")
            
            # Проверяем создание таблицы documents
            with db.engine.connect() as conn:
                result = conn.execute(db.text("SELECT name FROM sqlite_master WHERE type='table' AND name='documents'"))
                table_exists = result.fetchone() is not None
                print(f"📋 Таблица documents создана: {'✅' if table_exists else '❌'}")
                
                if table_exists:
                    result = conn.execute(db.text("PRAGMA table_info(documents)"))
                    columns_count = len(result.fetchall())
                    print(f"   📊 Колонок в таблице: {columns_count}")
                
                # Проверяем индекс
                result = conn.execute(db.text("SELECT name FROM sqlite_master WHERE type='index' AND name='ix_documents_debtor_id'"))
                index_exists = result.fetchone() is not None
                print(f"🔗 Индекс ix_documents_debtor_id создан: {'✅' if index_exists else '❌'}")
                
        except Exception as e:
            print(f"❌ Ошибка при выполнении миграции: {e}")
            print("ℹ️ Возможно, некоторые объекты уже существуют")

if __name__ == '__main__':
    add_debtor_status_and_documents_fixed()