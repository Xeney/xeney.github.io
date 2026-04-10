using System;
using System.Globalization;

class Program
{
    // Структура для хранения данных о зарплате
    struct SalaryRecord
    {
        public double Salary;
        public double NetSalary;
        public DateTime Date;
        public string Description;
    }

    // Массивы для хранения истории (максимум 6 месяцев)
    static SalaryRecord[] salaryHistory = new SalaryRecord[6];
    static int historyCount = 0;
    static int currentIndex = 0;

    // Константы
    const double NIGHT_BONUS_RATE = 0.20;
    const double OVERTIME_RATE = 300.0;
    const double TAX_RATE = 0.13;
    const double PENALTY_RATE = 0.15;
    const double EXPERIENCE_5_YEARS_BONUS = 0.10;
    const double EXPERIENCE_10_YEARS_BONUS = 0.20;

    static void Main()
    {
        Console.WriteLine("=== Калькулятор зарплаты охранника ===\n");
        
        bool continueProgram = true;
        
        while (continueProgram)
        {
            try
            {
                ShowMainMenu();
                string choice = Console.ReadLine();
                
                switch (choice)
                {
                    case "1":
                        CalculateCurrentSalary();
                        break;
                    case "2":
                        ShowSalaryHistory();
                        break;
                    case "3":
                        AnalyzeSalaryDynamics();
                        break;
                    case "4":
                        SearchInHistory();
                        break;
                    case "5":
                        continueProgram = false;
                        Console.WriteLine("До свидания!");
                        break;
                    default:
                        Console.WriteLine("Неверный выбор! Попробуйте снова.");
                        break;
                }
                
                if (continueProgram && choice != "5")
                {
                    Console.WriteLine("\nНажмите любую клавишу для продолжения...");
                    Console.ReadKey();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Произошла ошибка: {ex.Message}");
            }
        }
    }

    // Функция для отображения главного меню
    static void ShowMainMenu()
    {
        Console.Clear();
        Console.WriteLine("=== Калькулятор зарплаты охранника ===");
        Console.WriteLine("1. Рассчитать текущую зарплату");
        Console.WriteLine("2. Просмотреть историю расчётов");
        Console.WriteLine("3. Анализ динамики зарплат");
        Console.WriteLine("4. Поиск в истории");
        Console.WriteLine("5. Выйти");
        Console.Write("\nВыберите действие: ");
    }

    // Основная функция расчёта зарплаты
    static void CalculateCurrentSalary()
    {
        Console.Clear();
        Console.WriteLine("=== Расчёт текущей зарплаты ===\n");

        // Ввод данных с проверкой
        double salary = GetValidDoubleInput("Введите оклад: ", 0);
        int workedDays = GetValidIntInput("Введите количество отработанных дней: ", 1, 31);
        int nightShifts = GetValidIntInput("Введите количество ночных смен: ", 0, 31);
        int overtimeHours = GetValidIntInput("Введите количество сверхурочных часов: ", 0, 200);
        int experience = GetValidIntInput("Введите стаж (лет): ", 0, 50);
        
        bool hasViolations = GetYesNoInput("Были нарушения? (да/нет): ");

        // Основные расчёты
        double dailyRate = salary / 22;
        double nightBonus = CalculateNightBonus(nightShifts, dailyRate);
        double overtimePay = CalculateOvertimePay(overtimeHours);
        double experienceBonus = ApplyBonuses(salary, experience);
        double totalBeforeTax = salary + nightBonus + overtimePay + experienceBonus;
        double penalty = ApplyPenalties(totalBeforeTax, hasViolations);
        double taxableAmount = totalBeforeTax - penalty;
        double taxAmount = CalculateTax(taxableAmount);
        double netSalary = taxableAmount - taxAmount;

        // Сохранение в историю
        SaveToHistory(salary, netSalary, $"Оклад: {salary}, Дни: {workedDays}, Ночные: {nightShifts}");

        // Вывод результатов
        DisplaySalaryResults(salary, nightBonus, overtimePay, experienceBonus, 
                           penalty, taxAmount, netSalary, hasViolations);
    }

    // Функция применения премий
    static double ApplyBonuses(double salary, int experience)
    {
        double bonus = 0;
        
        if (experience > 10)
        {
            bonus = salary * EXPERIENCE_10_YEARS_BONUS;
        }
        else if (experience > 5)
        {
            bonus = salary * EXPERIENCE_5_YEARS_BONUS;
        }
        
        return bonus;
    }

    // Функция применения штрафов
    static double ApplyPenalties(double totalBeforeTax, bool hasViolations)
    {
        if (hasViolations)
        {
            return totalBeforeTax * PENALTY_RATE;
        }
        return 0;
    }

    // Функция расчёта налога
    static double CalculateTax(double taxableAmount)
    {
        return taxableAmount * TAX_RATE;
    }

    // Функция расчёта надбавки за ночные смены
    static double CalculateNightBonus(int nightShifts, double dailyRate)
    {
        return nightShifts * dailyRate * NIGHT_BONUS_RATE;
    }

    // Функция расчёта оплаты за сверхурочные
    static double CalculateOvertimePay(int overtimeHours)
    {
        return overtimeHours * OVERTIME_RATE;
    }

    // Функция сохранения в историю
    static void SaveToHistory(double salary, double netSalary, string description)
    {
        if (historyCount < salaryHistory.Length)
        {
            salaryHistory[historyCount] = new SalaryRecord
            {
                Salary = salary,
                NetSalary = netSalary,
                Date = DateTime.Now,
                Description = description
            };
            historyCount++;
        }
        else
        {
            // Циклический буфер - заменяем самую старую запись
            salaryHistory[currentIndex] = new SalaryRecord
            {
                Salary = salary,
                NetSalary = netSalary,
                Date = DateTime.Now,
                Description = description
            };
            currentIndex = (currentIndex + 1) % salaryHistory.Length;
        }
    }

    // Функция отображения истории
    static void ShowSalaryHistory()
    {
        Console.Clear();
        Console.WriteLine("=== История расчётов зарплат ===\n");

        if (historyCount == 0)
        {
            Console.WriteLine("История расчётов пуста.");
            return;
        }

        for (int i = 0; i < historyCount; i++)
        {
            var record = salaryHistory[i];
            Console.WriteLine($"{i + 1}. {record.Date:dd.MM.yyyy HH:mm}");
            Console.WriteLine($"   Описание: {record.Description}");
            Console.WriteLine($"   Оклад: {record.Salary:F2} руб.");
            Console.WriteLine($"   На руки: {record.NetSalary:F2} руб.");
            Console.WriteLine();
        }
    }

    // Функция анализа динамики
    static void AnalyzeSalaryDynamics()
    {
        Console.Clear();
        Console.WriteLine("=== Анализ динамики зарплат ===\n");

        if (historyCount < 2)
        {
            Console.WriteLine("Для анализа необходимо как минимум 2 записи в истории.");
            return;
        }

        // Расчёт средней зарплаты
        double totalNetSalary = 0;
        double maxSalary = double.MinValue;
        double minSalary = double.MaxValue;
        int maxIndex = 0, minIndex = 0;

        for (int i = 0; i < historyCount; i++)
        {
            double netSalary = salaryHistory[i].NetSalary;
            totalNetSalary += netSalary;

            if (netSalary > maxSalary)
            {
                maxSalary = netSalary;
                maxIndex = i;
            }

            if (netSalary < minSalary)
            {
                minSalary = netSalary;
                minIndex = i;
            }
        }

        double averageSalary = totalNetSalary / historyCount;

        // Расчёт изменения за последний месяц
        double lastChangePercent = 0;
        if (historyCount >= 2)
        {
            double current = salaryHistory[historyCount - 1].NetSalary;
            double previous = salaryHistory[historyCount - 2].NetSalary;
            lastChangePercent = ((current - previous) / previous) * 100;
        }

        // Вывод результатов анализа
        Console.WriteLine($"Количество записей в истории: {historyCount}");
        Console.WriteLine($"Средняя зарплата за период: {averageSalary:F2} руб.");
        Console.WriteLine($"Максимальная зарплата: {maxSalary:F2} руб. ({salaryHistory[maxIndex].Date:MMMM yyyy})");
        Console.WriteLine($"Минимальная зарплата: {minSalary:F2} руб. ({salaryHistory[minIndex].Date:MMMM yyyy})");
        
        if (historyCount >= 2)
        {
            string changeSymbol = lastChangePercent >= 0 ? "+" : "";
            Console.WriteLine($"Изменение за последний месяц: {changeSymbol}{lastChangePercent:F1}%");
        }

        // Дополнительная статистика
        Console.WriteLine("\n=== Дополнительная статистика ===");
        for (int i = 1; i < historyCount; i++)
        {
            double current = salaryHistory[i].NetSalary;
            double previous = salaryHistory[i - 1].NetSalary;
            double change = ((current - previous) / previous) * 100;
            string trend = change >= 0 ? "↑" : "↓";
            Console.WriteLine($"{salaryHistory[i].Date:MM.yyyy}: {current:F2} руб. ({trend} {change:+0.0;-0.0}%)");
        }
    }

    // Функция поиска в истории
    static void SearchInHistory()
    {
        Console.Clear();
        Console.WriteLine("=== Поиск в истории зарплат ===\n");

        if (historyCount == 0)
        {
            Console.WriteLine("История расчётов пуста.");
            return;
        }

        Console.WriteLine("1. Поиск по сумме");
        Console.WriteLine("2. Поиск по дате");
        Console.Write("Выберите тип поиска: ");

        string searchType = Console.ReadLine();
        
        switch (searchType)
        {
            case "1":
                SearchByAmount();
                break;
            case "2":
                SearchByDate();
                break;
            default:
                Console.WriteLine("Неверный выбор.");
                break;
        }
    }

    // Поиск по сумме
    static void SearchByAmount()
    {
        Console.Write("Введите минимальную сумму для поиска: ");
        if (double.TryParse(Console.ReadLine(), out double minAmount))
        {
            Console.WriteLine("\nРезультаты поиска:");
            bool found = false;
            
            for (int i = 0; i < historyCount; i++)
            {
                if (salaryHistory[i].NetSalary >= minAmount)
                {
                    Console.WriteLine($"{salaryHistory[i].Date:dd.MM.yyyy} - {salaryHistory[i].NetSalary:F2} руб.");
                    found = true;
                }
            }
            
            if (!found)
            {
                Console.WriteLine("Записей не найдено.");
            }
        }
        else
        {
            Console.WriteLine("Некорректная сумма.");
        }
    }

    // Поиск по дате
    static void SearchByDate()
    {
        Console.Write("Введите месяц и год для поиска (ММ.гггг): ");
        string dateInput = Console.ReadLine();
        
        if (DateTime.TryParseExact(dateInput, "MM.yyyy", CultureInfo.InvariantCulture, 
            DateTimeStyles.None, out DateTime searchDate))
        {
            Console.WriteLine("\nРезультаты поиска:");
            bool found = false;
            
            for (int i = 0; i < historyCount; i++)
            {
                if (salaryHistory[i].Date.Month == searchDate.Month && 
                    salaryHistory[i].Date.Year == searchDate.Year)
                {
                    Console.WriteLine($"{salaryHistory[i].Date:dd.MM.yyyy} - {salaryHistory[i].NetSalary:F2} руб.");
                    found = true;
                }
            }
            
            if (!found)
            {
                Console.WriteLine("Записей не найдено.");
            }
        }
        else
        {
            Console.WriteLine("Некорректный формат даты.");
        }
    }

    // Функция для вывода результатов
    static void DisplaySalaryResults(double salary, double nightBonus, double overtimePay, 
                                   double experienceBonus, double penalty, double taxAmount, 
                                   double netSalary, bool hasViolations)
    {
        Console.WriteLine("\n=== Результат расчёта ===");
        Console.WriteLine($"Оклад: {salary,15:F2} руб.");
        Console.WriteLine($"Надбавка за ночные смены: {nightBonus,8:F2} руб.");
        Console.WriteLine($"Сверхурочные: {overtimePay,18:F2} руб.");
        Console.WriteLine($"Премия за стаж: {experienceBonus,15:F2} руб.");
        
        if (hasViolations)
        {
            Console.WriteLine($"Штраф за нарушения: {penalty,13:F2} руб.");
        }
        
        Console.WriteLine($"Налог (13%): {taxAmount,17:F2} руб.");
        Console.WriteLine(new string('=', 40));
        Console.WriteLine($"Итого на руки: {netSalary,14:F2} руб.");
    }

    // Вспомогательные функции для ввода данных
    static double GetValidDoubleInput(string prompt, double minValue)
    {
        double value;
        while (true)
        {
            Console.Write(prompt);
            if (double.TryParse(Console.ReadLine(), out value) && value >= minValue)
                return value;
            Console.WriteLine($"Ошибка! Введите число больше или равно {minValue}.");
        }
    }

    static int GetValidIntInput(string prompt, int minValue, int maxValue)
    {
        int value;
        while (true)
        {
            Console.Write(prompt);
            if (int.TryParse(Console.ReadLine(), out value) && value >= minValue && value <= maxValue)
                return value;
            Console.WriteLine($"Ошибка! Введите целое число от {minValue} до {maxValue}.");
        }
    }

    static bool GetYesNoInput(string prompt)
    {
        while (true)
        {
            Console.Write(prompt);
            string answer = Console.ReadLine().ToLower();
            if (answer == "да" || answer == "д")
                return true;
            if (answer == "нет" || answer == "н")
                return false;
            Console.WriteLine("Ошибка! Введите 'да' или 'нет'.");
        }
    }
}