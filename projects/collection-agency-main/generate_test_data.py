import os
import sys
from openpyxl import Workbook
from datetime import datetime, timedelta
import random

def generate_test_excel(filename='test_debtors.xlsx', num_records=50):
    """
    Генерирует тестовый Excel файл с данными должников
    """
    print(f"🔄 Генерация тестовых данных ({num_records} записей)...")
    
    # Создаем новую книгу Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Должники"
    
    # Заголовки столбцов
    headers = ['ФИО', 'Дата рождения', 'Паспорт', 'Номер договора', 'Сумма долга', 'Банк']
    ws.append(headers)
    
    # Тестовые данные
    surnames = ['Иванов', 'Петров', 'Сидоров', 'Кузнецов', 'Смирнов', 'Попов', 'Васильев', 'Федоров']
    names = ['Иван', 'Петр', 'Сергей', 'Алексей', 'Дмитрий', 'Андрей', 'Михаил', 'Владимир']
    patronymics = ['Иванович', 'Петрович', 'Сергеевич', 'Алексеевич', 'Дмитриевич', 'Андреевич']
    
    banks = ['Сбербанк', 'ВТБ', 'Альфа-Банк', 'Тинькофф', 'Газпромбанк', 'Открытие', 'Райффайзенбанк']
    
    # Генерируем тестовые записи
    for i in range(1, num_records + 1):
        # ФИО
        full_name = f"{random.choice(surnames)} {random.choice(names)} {random.choice(patronymics)}"
        
        # Дата рождения (от 20 до 70 лет)
        birth_year = random.randint(1955, 2003)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        birth_date = f"{birth_day:02d}.{birth_month:02d}.{birth_year}"
        
        # Паспортные данные
        passport_series = random.randint(1000, 9999)
        passport_number = random.randint(100000, 999999)
        passport_data = f"{passport_series} {passport_number}"
        
        # Номер договора
        contract_number = f"DOG-2024-{i:04d}"
        
        # Сумма долга (от 10,000 до 1,000,000 рублей)
        debt_amount = round(random.uniform(10000, 1000000), 2)
        
        # Банк
        bank_name = random.choice(banks)
        
        # Добавляем строку в Excel
        ws.append([
            full_name,
            birth_date,
            passport_data,
            contract_number,
            debt_amount,
            bank_name
        ])
    
    # Настраиваем ширину столбцов
    column_widths = [30, 15, 15, 20, 15, 20]
    for i, width in enumerate(column_widths, 1):
        ws.column_dimensions[chr(64 + i)].width = width
    
    # Сохраняем файл
    wb.save(filename)
    print(f"✅ Файл сохранен: {filename}")
    print(f"📁 Полный путь: {os.path.abspath(filename)}")
    
    # Выводим статистику
    print(f"\n📊 Статистика:")
    print(f"   • Записей создано: {num_records}")
    print(f"   • Банки: {', '.join(set(banks))}")
    print(f"   • Диапазон сумм: 10,000 - 1,000,000 руб.")
    
    return filename

def generate_small_test_file(filename='small_test.xlsx'):
    """
    Генерирует маленький тестовый файл (5 записей) для быстрой проверки
    """
    print("🔄 Генерация маленького тестового файла...")
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Должники"
    
    # Заголовки
    headers = ['ФИО', 'Дата рождения', 'Паспорт', 'Номер договора', 'Сумма долга', 'Банк']
    ws.append(headers)
    
    # Тестовые данные (5 записей)
    test_data = [
        ['Иванов Иван Иванович', '15.03.1980', '1234 567890', 'TEST-001', 150000, 'Сбербанк'],
        ['Петрова Мария Сергеевна', '22.07.1985', '5678 123456', 'TEST-002', 75500.50, 'ВТБ'],
        ['Сидоров Петр Алексеевич', '03.11.1975', '9012 345678', 'TEST-003', 200000, 'Альфа-Банк'],
        ['Кузнецова Анна Дмитриевна', '18.05.1990', '3456 789012', 'TEST-004', 50000, 'Тинькофф'],
        ['Федоров Алексей Петрович', '29.12.1982', '7890 123456', 'TEST-005', 300000, 'Газпромбанк']
    ]
    
    for row in test_data:
        ws.append(row)
    
    # Настраиваем ширину столбцов
    column_widths = [30, 15, 15, 20, 15, 20]
    for i, width in enumerate(column_widths, 1):
        ws.column_dimensions[chr(64 + i)].width = width
    
    wb.save(filename)
    print(f"✅ Маленький тестовый файл сохранен: {filename}")
    print(f"📁 Полный путь: {os.path.abspath(filename)}")
    
    return filename

def main():
    """
    Главная функция - предлагает выбор пользователю
    """
    print("🎯 Генератор тестовых данных для импорта")
    print("=" * 50)
    
    while True:
        print("\nВыберите вариант:")
        print("1. 📊 Большой файл (50 записей) - для тестирования импорта")
        print("2. 📝 Маленький файл (5 записей) - для быстрой проверки")
        print("3. 🔢 Указать количество записей")
        print("4. ❌ Выход")
        
        choice = input("\nВаш выбор (1-4): ").strip()
        
        if choice == '1':
            filename = generate_test_excel('test_debtors_50.xlsx', 50)
            break
        elif choice == '2':
            filename = generate_small_test_file('test_debtors_5.xlsx')
            break
        elif choice == '3':
            try:
                num = int(input("Введите количество записей: "))
                filename = f"test_debtors_{num}.xlsx"
                generate_test_excel(filename, num)
                break
            except ValueError:
                print("❌ Ошибка: введите число!")
        elif choice == '4':
            print("👋 Выход...")
            return
        else:
            print("❌ Неверный выбор! Попробуйте снова.")
    
    print(f"\n🎉 Файл готов к импорту!")
    print(f"📋 Для импорта:")
    print(f"   1. Войдите в систему как администратор/менеджер")
    print(f"   2. Перейдите в раздел 'Импорт'")
    print(f"   3. Загрузите файл: {filename}")
    print(f"   4. Нажмите 'Импортировать'")

if __name__ == '__main__':
    main()