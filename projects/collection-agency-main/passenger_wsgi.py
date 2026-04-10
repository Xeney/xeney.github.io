#!/usr/bin/env python3
"""
Passenger WSGI entry point for deployment on shared hosting (reg.ru)
"""
import sys
import os

# Путь к интерпретатору Python из виртуального окружения (опционально)
INTERP = os.path.join(os.environ.get('HOME', ''), 'collection-agency', 'venv', 'bin', 'python3')

# Перезапуск с правильным интерпретатором если нужно
if os.path.exists(INTERP) and sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Добавить путь к проекту
project_path = os.path.join(os.environ.get('HOME', ''), 'collection-agency')
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Импортировать приложение
from app import create_app

# create_app не принимает аргументы в текущей реализации
application = create_app()