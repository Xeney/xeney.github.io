from app import create_app, db
from app.models import User, Profile, Path, Stage, Step, Test, Question, Answer, UserProgress, XPLog
from datetime import datetime, timedelta, timezone

def seed_data():
    app = create_app()
    with app.app_context():
        print("🌱 Начинаем заполнение базы тестовыми данными...")
        
        # 1. Создаем тестового пользователя если его нет
        user = User.query.filter_by(email='student@example.com').first()
        if not user:
            user = User(email='student@example.com', role='student')
            user.set_password('student123')
            db.session.add(user)
            db.session.flush()
            
            profile = Profile(
                user_id=user.id,
                username='student',
                xp=150,
                bio='Я тестовый студент, учусь программировать',
                is_public=True
            )
            db.session.add(profile)
            print("  ✅ Создан тестовый пользователь")
        else:
            print("  ✅ Тестовый пользователь уже существует")
        
        # 2. Путь: Python разработчик
        python_path = Path.query.filter_by(title='Python разработчик').first()
        if not python_path:
            python_path = Path(
                title='Python разработчик',
                description='Полный путь от новичка до Junior Python разработчика',
                difficulty='beginner'
            )
            db.session.add(python_path)
            db.session.flush()
            print("  ✅ Создан путь: Python разработчик")
            
            # Этапы и шаги для Python
            stage1 = Stage(
                path_id=python_path.id,
                title='Основы Python',
                description='Изучите базовый синтаксис и структуры данных',
                order_index=1
            )
            db.session.add(stage1)
            db.session.flush()
            
            # Шаг 1 - теория
            step1 = Step(
                stage_id=stage1.id,
                title='Введение в Python',
                content='''
                <h2>Добро пожаловать в мир Python!</h2>
                <p>Python - это высокоуровневый язык программирования, который отличается простотой и читаемостью кода.</p>
                <h3>Почему Python?</h3>
                <ul>
                    <li>Простой синтаксис</li>
                    <li>Большое сообщество</li>
                    <li>Множество библиотек</li>
                    <li>Применяется в веб-разработке, анализе данных, AI</li>
                </ul>
                ''',
                type='theory',
                xp_reward=10,
                order_index=1
            )
            db.session.add(step1)
            
            # Шаг 2 - теория
            step2 = Step(
                stage_id=stage1.id,
                title='Переменные и типы данных',
                content='''
                <h2>Переменные в Python</h2>
                <p>В Python не нужно объявлять тип переменной - он определяется автоматически.</p>
                <pre><code>
name = "Анна"        # строка (str)
age = 25             # целое число (int)
height = 1.75        # число с плавающей точкой (float)
is_student = True    # булево значение (bool)
                </code></pre>
                ''',
                type='theory',
                xp_reward=10,
                order_index=2
            )
            db.session.add(step2)
            
            # Шаг 3 - тест
            step3 = Step(
                stage_id=stage1.id,
                title='Тест по основам Python',
                content='Проверьте свои знания основ Python',
                type='test',
                xp_reward=30,
                order_index=3
            )
            db.session.add(step3)
            db.session.flush()
            
            # Тест Python
            test_python = Test(
                step_id=step3.id,
                passing_score=80
            )
            db.session.add(test_python)
            db.session.flush()
            
            # Вопросы для Python теста
            q1 = Question(test_id=test_python.id, text='Какой оператор используется для вывода данных в Python?')
            db.session.add(q1)
            db.session.flush()
            db.session.add_all([
                Answer(question_id=q1.id, text='print()', is_correct=True),
                Answer(question_id=q1.id, text='input()', is_correct=False),
                Answer(question_id=q1.id, text='output()', is_correct=False),
                Answer(question_id=q1.id, text='console.log()', is_correct=False)
            ])
            
            q2 = Question(test_id=test_python.id, text='Какой тип данных используется для целых чисел?')
            db.session.add(q2)
            db.session.flush()
            db.session.add_all([
                Answer(question_id=q2.id, text='int', is_correct=True),
                Answer(question_id=q2.id, text='float', is_correct=False),
                Answer(question_id=q2.id, text='str', is_correct=False),
                Answer(question_id=q2.id, text='bool', is_correct=False)
            ])
            
            q3 = Question(test_id=test_python.id, text='Как создать комментарий в Python?')
            db.session.add(q3)
            db.session.flush()
            db.session.add_all([
                Answer(question_id=q3.id, text='# Это комментарий', is_correct=True),
                Answer(question_id=q3.id, text='// Это комментарий', is_correct=False),
                Answer(question_id=q3.id, text='/* Это комментарий */', is_correct=False),
                Answer(question_id=q3.id, text='<!-- Это комментарий -->', is_correct=False)
            ])
            
            # Прогресс для пользователя
            if user:
                progress1 = UserProgress(
                    user_id=user.id,
                    step_id=step1.id,
                    completed=True,
                    completed_at=datetime.now(timezone.utc) - timedelta(days=2)
                )
                db.session.add(progress1)
                
                progress2 = UserProgress(
                    user_id=user.id,
                    step_id=step2.id,
                    completed=True,
                    completed_at=datetime.now(timezone.utc) - timedelta(days=1)
                )
                db.session.add(progress2)
                
                xp1 = XPLog(user_id=user.id, amount=10, reason='Пройден шаг: Введение в Python')
                xp2 = XPLog(user_id=user.id, amount=10, reason='Пройден шаг: Переменные и типы данных')
                db.session.add_all([xp1, xp2])
                
                user.profile.xp = 170
        else:
            print("  ✅ Путь Python разработчик уже существует")
        
        # 3. Путь: C# разработчик
        csharp_path = Path.query.filter_by(title='C# разработчик').first()
        if not csharp_path:
            csharp_path = Path(
                title='C# разработчик',
                description='Изучите основы C# и платформы .NET для создания приложений',
                difficulty='beginner'
            )
            db.session.add(csharp_path)
            db.session.flush()
            print("  ✅ Создан путь: C# разработчик")
            
            # Этап 1: Основы C#
            stage_csharp1 = Stage(
                path_id=csharp_path.id,
                title='Основы языка C#',
                description='Изучите базовый синтаксис, типы данных и основы ООП в C#',
                order_index=1
            )
            db.session.add(stage_csharp1)
            db.session.flush()
            
            # Шаг 1 - теория: Введение в C# (РАСШИРЕННАЯ ТЕОРИЯ)
            step_csharp1 = Step(
                stage_id=stage_csharp1.id,
                title='Введение в C# и .NET',
                content='''
                <h1>Введение в C# и платформу .NET</h1>
                
                <div class="alert alert-info">
                    <strong>C#</strong> (произносится "си шарп") - современный объектно-ориентированный язык программирования, разработанный компанией Microsoft.
                </div>

                <h2>Что такое .NET?</h2>
                <p>.NET - это платформа для разработки различных типов приложений. Она включает в себя:</p>
                <ul>
                    <li><strong>Языки программирования</strong> (C#, F#, Visual Basic)</li>
                    <li><strong>Библиотеки классов</strong> для работы с файлами, сетью, базами данных</li>
                    <li><strong>Среду выполнения</strong> (CLR - Common Language Runtime)</li>
                </ul>

                <h3>Типы приложений на C#:</h3>
                <div class="row">
                    <div class="col-md-6">
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5>Десктопные приложения</h5>
                                <p>Windows Forms, WPF, MAUI</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5>Веб-приложения</h5>
                                <p>ASP.NET Core, Blazor</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5>Мобильные приложения</h5>
                                <p>Xamarin, .NET MAUI</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5>Игры</h5>
                                <p>Unity (C#)</p>
                            </div>
                        </div>
                    </div>
                </div>

                <h2>Особенности C#:</h2>
                <table class="table table-bordered">
                    <tr>
                        <th>Особенность</th>
                        <th>Описание</th>
                    </tr>
                    <tr>
                        <td>Строгая типизация</td>
                        <td>Все переменные имеют фиксированный тип</td>
                    </tr>
                    <tr>
                        <td>Объектно-ориентированный</td>
                        <td>Поддерживает классы, наследование, полиморфизм</td>
                    </tr>
                    <tr>
                        <td>Автоматическая сборка мусора</td>
                        <td>Не нужно вручную освобождать память</td>
                    </tr>
                    <tr>
                        <td>Кроссплатформенность</td>
                        <td>Работает на Windows, Linux, macOS через .NET Core</td>
                    </tr>
                </table>

                <h2>Первая программа на C#:</h2>
                <pre><code>
using System;

namespace MyFirstApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello, World!");
            Console.ReadLine();
        }
    }
}
                </code></pre>

                <h3>Разбор кода:</h3>
                <ul>
                    <li><code>using System;</code> - подключает пространство имен System</li>
                    <li><code>namespace</code> - объявляет пространство имен</li>
                    <li><code>class Program</code> - объявляет класс</li>
                    <li><code>static void Main()</code> - точка входа в программу</li>
                    <li><code>Console.WriteLine()</code> - вывод в консоль</li>
                </ul>
                ''',
                type='theory',
                xp_reward=20,
                order_index=1
            )
            db.session.add(step_csharp1)
            
            # Шаг 2 - теория: Типы данных и переменные (РАСШИРЕННАЯ ТЕОРИЯ)
            step_csharp2 = Step(
                stage_id=stage_csharp1.id,
                title='Типы данных и переменные в C#',
                content='''
                <h1>Типы данных и переменные в C#</h1>
                
                <div class="alert alert-warning">
                    <strong>Важно!</strong> C# является строго типизированным языком, что означает необходимость указывать тип переменной при её объявлении.
                </div>

                <h2>Простые типы данных:</h2>
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Тип</th>
                            <th>Описание</th>
                            <th>Диапазон</th>
                            <th>Пример</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>int</code></td>
                            <td>Целые числа</td>
                            <td>-2,147,483,648 до 2,147,483,647</td>
                            <td><code>int age = 25;</code></td>
                        </tr>
                        <tr>
                            <td><code>long</code></td>
                            <td>Длинные целые числа</td>
                            <td>-9 квинтильонов до 9 квинтильонов</td>
                            <td><code>long population = 8_000_000_000L;</code></td>
                        </tr>
                        <tr>
                            <td><code>float</code></td>
                            <td>Числа с плавающей точкой</td>
                            <td>±1.5e-45 до ±3.4e38</td>
                            <td><code>float price = 19.99f;</code></td>
                        </tr>
                        <tr>
                            <td><code>double</code></td>
                            <td>Двойная точность</td>
                            <td>±5.0e-324 до ±1.7e308</td>
                            <td><code>double pi = 3.14159;</code></td>
                        </tr>
                        <tr>
                            <td><code>decimal</code></td>
                            <td>Для финансовых расчетов</td>
                            <td>±1.0e-28 до ±7.9e28</td>
                            <td><code>decimal salary = 50000.50m;</code></td>
                        </tr>
                        <tr>
                            <td><code>string</code></td>
                            <td>Строки</td>
                            <td>до 2 млрд символов</td>
                            <td><code>string name = "Анна";</code></td>
                        </tr>
                        <tr>
                            <td><code>char</code></td>
                            <td>Одиночный символ</td>
                            <td>любой Unicode символ</td>
                            <td><code>char grade = 'A';</code></td>
                        </tr>
                        <tr>
                            <td><code>bool</code></td>
                            <td>Логический тип</td>
                            <td>true или false</td>
                            <td><code>bool isStudent = true;</code></td>
                        </tr>
                    </tbody>
                </table>

                <h2>Объявление переменных:</h2>
                <pre><code>
// Полный синтаксис с указанием типа
int number = 10;
string message = "Hello";

// Использование var (тип определяется компилятором)
var count = 42;         // int
var text = "World";     // string
var price = 19.99;      // double (по умолчанию)

// Константы (значение нельзя изменить)
const double PI = 3.14159;
const int DAYS_IN_WEEK = 7;

// Несколько переменных одной строкой
int x = 10, y = 20, z = 30;
                </code></pre>

                <h2>Nullable типы (типы, которые могут быть null):</h2>
                <pre><code>
// Обычный int не может быть null
int normalInt = null; // Ошибка!

// Nullable int может быть null
int? nullableInt = null;
int? age = 25;

// Проверка на null
if (nullableInt.HasValue)
{
    Console.WriteLine(nullableInt.Value);
}

// Оператор объединения с null
int result = nullableInt ?? 0; // если null, то 0
                </code></pre>

                <h2>Интерполяция строк:</h2>
                <pre><code>
string name = "Анна";
int age = 25;

// Старый способ (конкатенация)
string oldWay = "Привет, " + name + "! Тебе " + age + " лет.";

// Новый способ (интерполяция)
string newWay = $"Привет, {name}! Тебе {age} лет.";

// Можно использовать выражения
string calc = $"2 + 2 = {2 + 2}";
                </code></pre>

                <h2>Преобразование типов:</h2>
                <pre><code>
// Неявное преобразование (без потери данных)
int intValue = 100;
long longValue = intValue;  // int → long
double doubleValue = intValue; // int → double

// Явное преобразование (может потерять данные)
double d = 123.45;
int i = (int)d;  // 123 (дробная часть отброшена)

// Преобразование через класс Convert
string str = "123";
int num = Convert.ToInt32(str);

// Проверка на возможность преобразования
if (int.TryParse("123", out int result))
{
    Console.WriteLine($"Успешно: {result}");
}
                </code></pre>
                ''',
                type='theory',
                xp_reward=20,
                order_index=2
            )
            db.session.add(step_csharp2)
            
            # Шаг 3 - теория: Управляющие конструкции
            step_csharp3 = Step(
                stage_id=stage_csharp1.id,
                title='Управляющие конструкции в C#',
                content='''
                <h1>Управляющие конструкции в C#</h1>
                
                <h2>Условные операторы</h2>
                
                <h3>if-else</h3>
                <pre><code>
int age = 18;

if (age >= 18)
{
    Console.WriteLine("Вы совершеннолетний");
}
else
{
    Console.WriteLine("Вы несовершеннолетний");
}

// if-else if
int score = 85;

if (score >= 90)
{
    Console.WriteLine("Отлично");
}
else if (score >= 75)
{
    Console.WriteLine("Хорошо");
}
else if (score >= 60)
{
    Console.WriteLine("Удовлетворительно");
}
else
{
    Console.WriteLine("Неудовлетворительно");
}
                </code></pre>

                <h3>switch</h3>
                <pre><code>
string day = "Monday";

switch (day)
{
    case "Monday":
        Console.WriteLine("Понедельник");
        break;
    case "Tuesday":
        Console.WriteLine("Вторник");
        break;
    case "Wednesday":
        Console.WriteLine("Среда");
        break;
    default:
        Console.WriteLine("Другой день");
        break;
}

// Современный switch (C# 8.0+)
string result = day switch
{
    "Monday" => "Понедельник",
    "Tuesday" => "Вторник",
    "Wednesday" => "Среда",
    _ => "Другой день"
};
                </code></pre>

                <h2>Циклы</h2>
                
                <h3>for</h3>
                <pre><code>
for (int i = 0; i < 5; i++)
{
    Console.WriteLine($"Итерация {i}");
}

// Обратный цикл
for (int i = 5; i > 0; i--)
{
    Console.WriteLine(i);
}
                </code></pre>

                <h3>while</h3>
                <pre><code>
int i = 0;
while (i < 5)
{
    Console.WriteLine($"while: {i}");
    i++;
}

// do-while (выполнится хотя бы один раз)
int j = 0;
do
{
    Console.WriteLine($"do-while: {j}");
    j++;
} while (j < 5);
                </code></pre>

                <h3>foreach</h3>
                <pre><code>
string[] fruits = { "яблоко", "банан", "апельсин" };

foreach (string fruit in fruits)
{
    Console.WriteLine(fruit);
}

// Для коллекций
List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };
foreach (int num in numbers)
{
    Console.WriteLine(num);
}
                </code></pre>

                <h2>Ключевые слова управления циклом</h2>
                <pre><code>
// break - выход из цикла
for (int i = 0; i < 10; i++)
{
    if (i == 5) break;
    Console.WriteLine(i); // 0,1,2,3,4
}

// continue - переход к следующей итерации
for (int i = 0; i < 5; i++)
{
    if (i == 2) continue;
    Console.WriteLine(i); // 0,1,3,4
}

// return - выход из метода
int FindNumber(int[] numbers, int target)
{
    foreach (int num in numbers)
    {
        if (num == target)
            return num; // немедленный выход из метода
    }
    return -1;
}
                </code></pre>
                ''',
                type='theory',
                xp_reward=20,
                order_index=3
            )
            db.session.add(step_csharp3)
            
            # Шаг 4 - теория: Массивы и коллекции
            step_csharp4 = Step(
                stage_id=stage_csharp1.id,
                title='Массивы и коллекции',
                content='''
                <h1>Массивы и коллекции в C#</h1>
                
                <h2>Массивы</h2>
                <pre><code>
// Объявление массива
int[] numbers = new int[5]; // массив из 5 элементов
string[] names = new string[] { "Анна", "Иван", "Мария" };
int[] simple = { 1, 2, 3, 4, 5 };

// Доступ к элементам
numbers[0] = 10;
int first = numbers[0];

// Длина массива
int length = names.Length;

// Многомерные массивы
int[,] matrix = new int[3, 3];
int[,,] cube = new int[3, 3, 3];

// Инициализация многомерного массива
int[,] matrix2 = {
    { 1, 2, 3 },
    { 4, 5, 6 },
    { 7, 8, 9 }
};

// Доступ к элементам многомерного массива
int element = matrix2[1, 1]; // 5
                </code></pre>

                <h2>Коллекции</h2>
                
                <h3>List<T> - динамический список</h3>
                <pre><code>
using System.Collections.Generic;

// Создание списка
List<int> numbers = new List<int>();
List<string> names = new List<string> { "Анна", "Иван" };

// Добавление элементов
numbers.Add(10);
numbers.AddRange(new[] { 20, 30, 40 });

// Вставка
numbers.Insert(1, 15); // вставить на позицию 1

// Удаление
numbers.Remove(20); // удалить по значению
numbers.RemoveAt(0); // удалить по индексу
numbers.Clear(); // очистить все

// Поиск
bool exists = numbers.Contains(30);
int index = numbers.IndexOf(30);
                </code></pre>

                <h3>Dictionary<TKey, TValue> - словарь</h3>
                <pre><code>
// Создание словаря
Dictionary<string, int> ages = new Dictionary<string, int>();

// Добавление
ages["Анна"] = 25;
ages.Add("Иван", 30);

// Проверка наличия
if (ages.ContainsKey("Анна"))
{
    int age = ages["Анна"];
}

// Перебор
foreach (var pair in ages)
{
    Console.WriteLine($"{pair.Key}: {pair.Value}");
}

// Безопасное получение значения
if (ages.TryGetValue("Мария", out int age))
{
    Console.WriteLine(age);
}
                </code></pre>

                <h3>HashSet<T> - множество уникальных элементов</h3>
                <pre><code>
HashSet<int> numbers = new HashSet<int> { 1, 2, 3, 4, 5 };
numbers.Add(3); // не добавится, т.к. уже есть

// Операции над множествами
HashSet<int> set1 = new HashSet<int> { 1, 2, 3 };
HashSet<int> set2 = new HashSet<int> { 2, 3, 4 };

set1.UnionWith(set2); // объединение
set1.IntersectWith(set2); // пересечение
set1.ExceptWith(set2); // разность
                </code></pre>

                <h2>LINQ - Language Integrated Query</h2>
                <pre><code>
using System.Linq;

int[] numbers = { 5, 2, 8, 1, 9, 3 };

// Фильтрация
var evenNumbers = numbers.Where(n => n % 2 == 0);

// Сортировка
var sorted = numbers.OrderBy(n => n);

// Проекция
var squares = numbers.Select(n => n * n);

// Агрегация
int sum = numbers.Sum();
double avg = numbers.Average();
int max = numbers.Max();
int min = numbers.Min();

// Синтаксис запросов
var result = from n in numbers
             where n > 3
             orderby n
             select n * 2;
                </code></pre>
                ''',
                type='theory',
                xp_reward=20,
                order_index=4
            )
            db.session.add(step_csharp4)
            
            # Шаг 5 - тест: Основы C#
            step_csharp5 = Step(
                stage_id=stage_csharp1.id,
                title='Тест: Основы языка C#',
                content='Проверьте свои знания основ C#',
                type='test',
                xp_reward=70,
                order_index=5
            )
            db.session.add(step_csharp5)
            db.session.flush()
            
            # Тест C#
            test_csharp = Test(
                step_id=step_csharp5.id,
                passing_score=70
            )
            db.session.add(test_csharp)
            db.session.flush()
            
            # Вопрос 1: Вывод в консоль
            q_csharp1 = Question(test_id=test_csharp.id, text='Какой метод используется для вывода текста в консоль в C#?')
            db.session.add(q_csharp1)
            db.session.flush()
            db.session.add_all([
                Answer(question_id=q_csharp1.id, text='Console.WriteLine()', is_correct=True),
                Answer(question_id=q_csharp1.id, text='System.out.println()', is_correct=False),
                Answer(question_id=q_csharp1.id, text='print()', is_correct=False),
                Answer(question_id=q_csharp1.id, text='echo()', is_correct=False)
            ])
            
            # Вопрос 2: Точка входа
            q_csharp2 = Question(test_id=test_csharp.id, text='Как называется точка входа в программу на C#?')
            db.session.add(q_csharp2)
            db.session.flush()
            db.session.add_all([
                Answer(question_id=q_csharp2.id, text='Main()', is_correct=True),
                Answer(question_id=q_csharp2.id, text='start()', is_correct=False),
                Answer(question_id=q_csharp2.id, text='init()', is_correct=False),
                Answer(question_id=q_csharp2.id, text='program()', is_correct=False)
            ])
            
            # Вопрос 3: Тип для целых чисел
            q_csharp3 = Question(test_id=test_csharp.id, text='Какой тип данных в C# используется для целых чисел?')
            db.session.add(q_csharp3)
            db.session.flush()
            db.session.add_all([
                Answer(question_id=q_csharp3.id, text='int', is_correct=True),
                Answer(question_id=q_csharp3.id, text='float', is_correct=False),
                Answer(question_id=q_csharp3.id, text='double', is_correct=False),
                Answer(question_id=q_csharp3.id, text='decimal', is_correct=False)
            ])
            
            # Вопрос 4: Ключевое слово для констант
            q_csharp4 = Question(test_id=test_csharp.id, text='Какое ключевое слово используется для объявления констант в C#?')
            db.session.add(q_csharp4)
            db.session.flush()
            db.session.add_all([
                Answer(question_id=q_csharp4.id, text='const', is_correct=True),
                Answer(question_id=q_csharp4.id, text='final', is_correct=False),
                Answer(question_id=q_csharp4.id, text='readonly', is_correct=False),
                Answer(question_id=q_csharp4.id, text='static', is_correct=False)
            ])
            
            # Вопрос 5: Сборщик мусора
            q_csharp5 = Question(test_id=test_csharp.id, text='Как в C# называется автоматический механизм управления памятью?')
            db.session.add(q_csharp5)
            db.session.flush()
            db.session.add_all([
                Answer(question_id=q_csharp5.id, text='Garbage Collector (GC)', is_correct=True),
                Answer(question_id=q_csharp5.id, text='Memory Manager', is_correct=False),
                Answer(question_id=q_csharp5.id, text='Auto Dispose', is_correct=False),
                Answer(question_id=q_csharp5.id, text='Cleaner', is_correct=False)
            ])
            
            # Вопрос 6: var ключевое слово
            q_csharp6 = Question(test_id=test_csharp.id, text='Что делает ключевое слово var в C#?')
            db.session.add(q_csharp6)
            db.session.flush()
            db.session.add_all([
                Answer(question_id=q_csharp6.id, text='Позволяет компилятору определить тип переменной', is_correct=True),
                Answer(question_id=q_csharp6.id, text='Создает переменную типа Variant', is_correct=False),
                Answer(question_id=q_csharp6.id, text='Объявляет глобальную переменную', is_correct=False),
                Answer(question_id=q_csharp6.id, text='Создает переменную типа var', is_correct=False)
            ])
            
            # Вопрос 7: Пространство имен
            q_csharp7 = Question(test_id=test_csharp.id, text='Какое ключевое слово используется для подключения пространства имен?')
            db.session.add(q_csharp7)
            db.session.flush()
            db.session.add_all([
                Answer(question_id=q_csharp7.id, text='using', is_correct=True),
                Answer(question_id=q_csharp7.id, text='import', is_correct=False),
                Answer(question_id=q_csharp7.id, text='include', is_correct=False),
                Answer(question_id=q_csharp7.id, text='namespace', is_correct=False)
            ])
            
            # Вопрос 8: Комментарии
            q_csharp8 = Question(test_id=test_csharp.id, text='Как создать однострочный комментарий в C#?')
            db.session.add(q_csharp8)
            db.session.flush()
            db.session.add_all([
                Answer(question_id=q_csharp8.id, text='// комментарий', is_correct=True),
                Answer(question_id=q_csharp8.id, text='# комментарий', is_correct=False),
                Answer(question_id=q_csharp8.id, text='<!-- комментарий -->', is_correct=False),
                Answer(question_id=q_csharp8.id, text='/* комментарий */', is_correct=False)
            ])
            
            # Вопрос 9: Интерполяция строк
            q_csharp9 = Question(test_id=test_csharp.id, text='Какой символ используется для интерполяции строк в C#?')
            db.session.add(q_csharp9)
            db.session.flush()
            db.session.add_all([
                Answer(question_id=q_csharp9.id, text='$', is_correct=True),
                Answer(question_id=q_csharp9.id, text='@', is_correct=False),
                Answer(question_id=q_csharp9.id, text='#', is_correct=False),
                Answer(question_id=q_csharp9.id, text='%', is_correct=False)
            ])
            
            # Вопрос 10: Nullable типы
            q_csharp10 = Question(test_id=test_csharp.id, text='Какой символ используется для создания nullable типа?')
            db.session.add(q_csharp10)
            db.session.flush()
            db.session.add_all([
                Answer(question_id=q_csharp10.id, text='?', is_correct=True),
                Answer(question_id=q_csharp10.id, text='*', is_correct=False),
                Answer(question_id=q_csharp10.id, text='!', is_correct=False),
                Answer(question_id=q_csharp10.id, text='~', is_correct=False)
            ])
            
            print("  ✅ Создан тест 'Основы языка C#' с 10 вопросами и 40 ответами")
            
            # Добавляем прогресс для C# (первые три шага пройдены)
            if user:
                progress_csharp1 = UserProgress(
                    user_id=user.id,
                    step_id=step_csharp1.id,
                    completed=True,
                    completed_at=datetime.now(timezone.utc) - timedelta(hours=5)
                )
                db.session.add(progress_csharp1)
                
                progress_csharp2 = UserProgress(
                    user_id=user.id,
                    step_id=step_csharp2.id,
                    completed=True,
                    completed_at=datetime.now(timezone.utc) - timedelta(hours=4)
                )
                db.session.add(progress_csharp2)
                
                progress_csharp3 = UserProgress(
                    user_id=user.id,
                    step_id=step_csharp3.id,
                    completed=True,
                    completed_at=datetime.now(timezone.utc) - timedelta(hours=3)
                )
                db.session.add(progress_csharp3)
                
                progress_csharp4 = UserProgress(
                    user_id=user.id,
                    step_id=step_csharp4.id,
                    completed=True,
                    completed_at=datetime.now(timezone.utc) - timedelta(hours=2)
                )
                db.session.add(progress_csharp4)
                
                xp_csharp1 = XPLog(user_id=user.id, amount=20, reason='Пройден шаг: Введение в C# и .NET')
                xp_csharp2 = XPLog(user_id=user.id, amount=20, reason='Пройден шаг: Типы данных и переменные')
                xp_csharp3 = XPLog(user_id=user.id, amount=20, reason='Пройден шаг: Управляющие конструкции')
                xp_csharp4 = XPLog(user_id=user.id, amount=20, reason='Пройден шаг: Массивы и коллекции')
                db.session.add_all([xp_csharp1, xp_csharp2, xp_csharp3, xp_csharp4])
                
                user.profile.xp += 80
        
        else:
            print("  ✅ Путь C# разработчик уже существует")
        
        # Сохраняем все изменения
        db.session.commit()
        
        print("\n" + "="*50)
        print("✅ БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")
        print("="*50)
        print("\n📊 СТАТИСТИКА:")
        print(f"  👤 Пользователей: {User.query.count()}")
        print(f"  🗺️ Путей: {Path.query.count()}")
        print(f"  📦 Этапов: {Stage.query.count()}")
        print(f"  📚 Шагов: {Step.query.count()}")
        print(f"  📝 Тестов: {Test.query.count()}")
        print(f"  ❓ Вопросов: {Question.query.count()}")
        print(f"  💡 Ответов: {Answer.query.count()}")
        print(f"  📊 Прогресс: {UserProgress.query.count()} записей")
        
        print("\n" + "="*50)
        print("🔑 ТЕСТОВЫЕ ДАННЫЕ ДЛЯ ВХОДА:")
        print("="*50)
        print("\n👤 Студент:")
        print("   Email: student@example.com")
        print("   Пароль: student123")
        student = User.query.filter_by(email='student@example.com').first()
        if student:
            print(f"   XP: {student.profile.xp}")
        print("\n👑 Администратор:")
        print("   Email: admin@example.com")
        print("   Пароль: admin123")
        
        print("\n" + "="*50)
        print("📋 ДОСТУПНЫЕ ТЕСТЫ:")
        print("="*50)
        tests = Test.query.all()
        for i, test in enumerate(tests, 1):
            if test.step:
                print(f"\n  {i}. 📝 {test.step.title}:")
                print(f"     - Вопросов: {len(test.questions)}")
                print(f"     - Проходной балл: {test.passing_score}%")
                print(f"     - Награда: {test.step.xp_reward} XP")
            else:
                print(f"\n  {i}. ⚠️ Тест ID {test.id} (без привязанного шага)")
                print(f"     - Вопросов: {len(test.questions)}")
                print(f"     - Проходной балл: {test.passing_score}%")

if __name__ == '__main__':
    seed_data()