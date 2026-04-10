using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;

namespace SalaryCalculatorOOP
{
    // Класс для хранения данных о расчете зарплаты
    class SalaryData
    {
        // Свойства ввода
        public double BaseSalary { get; set; }
        public int WorkedDays { get; set; }
        public int NightShifts { get; set; }
        public int OvertimeHours { get; set; }
        public int Experience { get; set; }
        public bool HasViolations { get; set; }
        
        // Свойства результатов расчета
        public double NightBonus { get; set; }
        public double OvertimePay { get; set; }
        public double ExperienceBonus { get; set; }
        public double Penalty { get; set; }
        public double TaxAmount { get; set; }
        public double NetSalary { get; set; }
        public DateTime CalculationDate { get; set; }
        public string Description { get; set; }

        // Конструктор
        public SalaryData(double baseSalary, int workedDays, int nightShifts, int overtimeHours, 
                         int experience, bool hasViolations)
        {
            BaseSalary = baseSalary;
            WorkedDays = workedDays;
            NightShifts = nightShifts;
            OvertimeHours = overtimeHours;
            Experience = experience;
            HasViolations = hasViolations;
            CalculationDate = DateTime.Now;
            Description = $"Оклад: {baseSalary}, Дни: {workedDays}, Ночные: {nightShifts}";
        }

        // Метод для красивого вывода информации о расчете
        public void DisplayInfo()
        {
            Console.WriteLine($"Дата расчета: {CalculationDate:dd.MM.yyyy HH:mm}");
            Console.WriteLine($"Оклад: {BaseSalary:F2} руб.");
            Console.WriteLine($"Отработано дней: {WorkedDays}");
            Console.WriteLine($"Ночные смены: {NightShifts}");
            Console.WriteLine($"Сверхурочные часы: {OvertimeHours}");
            Console.WriteLine($"Стаж: {Experience} лет");
            Console.WriteLine($"Нарушения: {(HasViolations ? "yes" : "no")}");
            Console.WriteLine($"Надбавка за ночные: {NightBonus:F2} руб.");
            Console.WriteLine($"Оплата сверхурочных: {OvertimePay:F2} руб.");
            Console.WriteLine($"Премия за стаж: {ExperienceBonus:F2} руб.");
            
            if (HasViolations)
            {
                Console.WriteLine($"Штраф: {Penalty:F2} руб.");
            }
            
            Console.WriteLine($"Налог: {TaxAmount:F2} руб.");
            Console.WriteLine($"Итого на руки: {NetSalary:F2} руб.");
            Console.WriteLine(new string('-', 50));
        }

        // Метод для краткого отображения (для списков)
        public void DisplayShortInfo()
        {
            Console.WriteLine($"{CalculationDate:dd.MM.yyyy} - {NetSalary:F2} руб. ({Description})");
        }
    }

    // Класс для расчета зарплаты
    class SalaryCalculator
    {
        // Константы
        private const double NIGHT_BONUS_RATE = 0.20;
        private const double OVERTIME_RATE = 300.0;
        private const double TAX_RATE = 0.13;
        private const double PENALTY_RATE = 0.15;
        private const double EXPERIENCE_5_YEARS_BONUS = 0.10;
        private const double EXPERIENCE_10_YEARS_BONUS = 0.20;

        // История расчетов
        private List<SalaryData> salaryHistory = new List<SalaryData>();
        private const int MAX_HISTORY_SIZE = 10;

        // Основной метод расчета зарплаты
        public SalaryData CalculateSalary(double baseSalary, int workedDays, int nightShifts, 
                                        int overtimeHours, int experience, bool hasViolations)
        {
            SalaryData data = new SalaryData(baseSalary, workedDays, nightShifts, overtimeHours, 
                                           experience, hasViolations);

            // Основные расчеты
            double dailyRate = baseSalary / 22;
            data.NightBonus = CalculateNightBonus(nightShifts, dailyRate);
            data.OvertimePay = CalculateOvertimePay(overtimeHours);
            data.ExperienceBonus = ApplyExperienceBonus(baseSalary, experience);
            
            double totalBeforeTax = baseSalary + data.NightBonus + data.OvertimePay + data.ExperienceBonus;
            data.Penalty = ApplyPenalties(totalBeforeTax, hasViolations);
            
            double taxableAmount = totalBeforeTax - data.Penalty;
            data.TaxAmount = CalculateTax(taxableAmount);
            data.NetSalary = taxableAmount - data.TaxAmount;

            // Сохранение в историю
            AddToHistory(data);

            return data;
        }

        // Применение премий за стаж
        private double ApplyExperienceBonus(double salary, int experience)
        {
            if (experience > 10)
            {
                return salary * EXPERIENCE_10_YEARS_BONUS;
            }
            else if (experience > 5)
            {
                return salary * EXPERIENCE_5_YEARS_BONUS;
            }
            return 0;
        }

        // Применение штрафов
        private double ApplyPenalties(double totalBeforeTax, bool hasViolations)
        {
            return hasViolations ? totalBeforeTax * PENALTY_RATE : 0;
        }

        // Расчет налога
        private double CalculateTax(double taxableAmount)
        {
            return taxableAmount * TAX_RATE;
        }

        // Расчет надбавки за ночные смены
        private double CalculateNightBonus(int nightShifts, double dailyRate)
        {
            return nightShifts * dailyRate * NIGHT_BONUS_RATE;
        }

        // Расчет оплаты за сверхурочные
        private double CalculateOvertimePay(int overtimeHours)
        {
            return overtimeHours * OVERTIME_RATE;
        }

        // Добавление в историю с ограничением размера
        private void AddToHistory(SalaryData data)
        {
            if (salaryHistory.Count >= MAX_HISTORY_SIZE)
            {
                salaryHistory.RemoveAt(0); // Удаляем самую старую запись
            }
            salaryHistory.Add(data);
        }

        // Получение истории расчетов
        public List<SalaryData> GetSalaryHistory()
        {
            return new List<SalaryData>(salaryHistory); // Возвращаем копию для инкапсуляции
        }

        // Сравнение двух расчетов
        public void CompareCalculations(int firstIndex, int secondIndex)
        {
            if (firstIndex < 0 || firstIndex >= salaryHistory.Count || 
                secondIndex < 0 || secondIndex >= salaryHistory.Count)
            {
                throw new ArgumentException("Неверные индексы расчетов");
            }

            SalaryData first = salaryHistory[firstIndex];
            SalaryData second = salaryHistory[secondIndex];

            Console.WriteLine("\n=== Результаты сравнения ===");
            Console.WriteLine($"Расчет от {first.CalculationDate:dd.MM.yyyy}: {first.NetSalary:F2} руб.");
            Console.WriteLine($"Расчет от {second.CalculationDate:dd.MM.yyyy}: {second.NetSalary:F2} руб.");
            Console.WriteLine("Разница:");

            double salaryDiff = second.BaseSalary - first.BaseSalary;
            if (Math.Abs(salaryDiff) > 0.01)
            {
                Console.WriteLine($"- Оклад: {salaryDiff:+#;-#;0} руб.");
            }

            double bonusDiff = second.ExperienceBonus - first.ExperienceBonus;
            if (Math.Abs(bonusDiff) > 0.01)
            {
                Console.WriteLine($"- Премия: {bonusDiff:+#;-#;0} руб.");
            }

            double nightDiff = second.NightBonus - first.NightBonus;
            if (Math.Abs(nightDiff) > 0.01)
            {
                Console.WriteLine($"- Надбавка за ночные: {nightDiff:+#;-#;0} руб.");
            }

            double overtimeDiff = second.OvertimePay - first.OvertimePay;
            if (Math.Abs(overtimeDiff) > 0.01)
            {
                Console.WriteLine($"- Сверхурочные: {overtimeDiff:+#;-#;0} руб.");
            }

            double totalDiff = second.NetSalary - first.NetSalary;
            double percentDiff = first.NetSalary != 0 ? (totalDiff / first.NetSalary) * 100 : 0;

            Console.WriteLine($"- Итоговая разница: {totalDiff:+#;-#;0} руб. ({percentDiff:+#;-#;0}%)");
        }

        // Статистика по истории
        public void DisplayStatistics()
        {
            if (salaryHistory.Count == 0)
            {
                Console.WriteLine("История расчетов пуста.");
                return;
            }

            Console.WriteLine("\n=== Статистика зарплат ===");
            Console.WriteLine($"Количество расчетов: {salaryHistory.Count}");

            double averageSalary = salaryHistory.Average(s => s.NetSalary);
            double maxSalary = salaryHistory.Max(s => s.NetSalary);
            double minSalary = salaryHistory.Min(s => s.NetSalary);

            Console.WriteLine($"Средняя зарплата: {averageSalary:F2} руб.");
            Console.WriteLine($"Максимальная зарплата: {maxSalary:F2} руб.");
            Console.WriteLine($"Минимальная зарплата: {minSalary:F2} руб.");

            if (salaryHistory.Count >= 2)
            {
                var last = salaryHistory[salaryHistory.Count - 1];
                var previous = salaryHistory[salaryHistory.Count - 2];
                double change = ((last.NetSalary - previous.NetSalary) / previous.NetSalary) * 100;
                Console.WriteLine($"Изменение за последний период: {change:+#;-#;0}%");
            }
        }
    }

    // Основной класс программы
    class Program
    {
        static SalaryCalculator calculator = new SalaryCalculator();

        static void Main()
        {
            Console.WriteLine("=== Система расчета зарплаты охранника (ООП) ===\n");
            
            bool continueProgram = true;
            
            while (continueProgram)
            {
                try
                {
                    ShowMainMenu();
                    string? choice = Console.ReadLine();
                    
                    switch (choice)
                    {
                        case "1":
                            CalculateNewSalary();
                            break;
                        case "2":
                            ShowSalaryHistory();
                            break;
                        case "3":
                            CompareSalaries();
                            break;
                        case "4":
                            ShowStatistics();
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

        // Главное меню
        static void ShowMainMenu()
        {
            Console.Clear();
            Console.WriteLine("=== Система расчета зарплаты (ООП) ===");
            Console.WriteLine("1. Новый расчет");
            Console.WriteLine("2. История расчетов");
            Console.WriteLine("3. Сравнить расчеты");
            Console.WriteLine("4. Статистика");
            Console.WriteLine("5. Выйти");
            Console.Write("\nВыберите действие: ");
        }

        // Новый расчет зарплаты
        static void CalculateNewSalary()
        {
            Console.Clear();
            Console.WriteLine("=== Новый расчет зарплаты ===\n");

            // Ввод данных
            double salary = GetValidDoubleInput("Введите оклад: ", 0);
            int workedDays = GetValidIntInput("Введите количество отработанных дней: ", 1, 31);
            int nightShifts = GetValidIntInput("Введите количество ночных смен: ", 0, 31);
            int overtimeHours = GetValidIntInput("Введите количество сверхурочных часов: ", 0, 200);
            int experience = GetValidIntInput("Введите стаж (лет): ", 0, 50);
            bool hasViolations = GetYesNoInput("Были нарушения? (yes/no): ");

            // Расчет
            SalaryData result = calculator.CalculateSalary(salary, workedDays, nightShifts, 
                                                         overtimeHours, experience, hasViolations);

            // Вывод результатов
            Console.WriteLine("\n=== Результат расчета ===");
            result.DisplayInfo();
        }

        // Просмотр истории расчетов
        static void ShowSalaryHistory()
        {
            Console.Clear();
            Console.WriteLine("=== История расчетов ===\n");

            var history = calculator.GetSalaryHistory();
            
            if (history.Count == 0)
            {
                Console.WriteLine("История расчетов пуста.");
                return;
            }

            for (int i = 0; i < history.Count; i++)
            {
                Console.Write($"{i + 1}. ");
                history[i].DisplayShortInfo();
            }
        }

        // Сравнение расчетов
        static void CompareSalaries()
        {
            Console.Clear();
            Console.WriteLine("=== Сравнение расчетов ===\n");

            var history = calculator.GetSalaryHistory();
            
            if (history.Count < 2)
            {
                Console.WriteLine("Для сравнения необходимо как минимум 2 расчета в истории.");
                return;
            }

            // Показываем историю для выбора
            for (int i = 0; i < history.Count; i++)
            {
                Console.WriteLine($"{i + 1}. {history[i].CalculationDate:dd.MM.yyyy} - {history[i].NetSalary:F2} руб.");
            }

            try
            {
                Console.Write("\nВыберите первый расчет (1-{0}): ", history.Count);
                int firstIndex = GetValidIntInput("", 1, history.Count) - 1;
                
                Console.Write("Выберите второй расчет (1-{0}): ", history.Count);
                int secondIndex = GetValidIntInput("", 1, history.Count) - 1;

                calculator.CompareCalculations(firstIndex, secondIndex);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Ошибка при сравнении: {ex.Message}");
            }
        }

        // Статистика
        static void ShowStatistics()
        {
            Console.Clear();
            calculator.DisplayStatistics();
        }

        // Вспомогательные методы для ввода данных
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
                if (!string.IsNullOrEmpty(prompt))
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
                string? answer = Console.ReadLine()?.ToLower();
                if (answer == "y" || answer == "yes")
                    return true;
                if (answer == "n" || answer == "no")
                    return false;
                Console.WriteLine("Ошибка! Введите 'yes' или 'no'.");
            }
        }
    }
}