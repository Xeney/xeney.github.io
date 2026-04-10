using System;

class Program
{
    static void Main()
    {
        bool exitProgram = false;
        
        while (!exitProgram)
        {
            Console.WriteLine("1. Отгадай ответ");
            Console.WriteLine("2. Об авторе");
            Console.WriteLine("3. Выход");
            Console.Write("Выберите действие: ");
            
            string choice = Console.ReadLine();
            
            switch (choice)
            {
                case "1":
                    PlayGuessGame();
                    break;
                case "2":
                    ShowAuthorInfo();
                    break;
                case "3":
                    exitProgram = ConfirmExit();
                    break;
                default:
                    Console.WriteLine("Неверный выбор!");
                    break;
            }
        }
    }

    static void ShowAuthorInfo()
    {
        Console.WriteLine("ФИО: Иванов Иван Иванович");
        Console.WriteLine("Группа: ПИ-123");
        Console.WriteLine("Нажмите любую клавишу для продолжения...");
        Console.ReadKey();
    }

    static bool ConfirmExit()
    {
        while (true)
        {
            Console.Write("Вы уверены, что хотите выйти? (д/н): ");
            string answer = Console.ReadLine().ToLower();
            
            if (answer == "д")
            {
                return true;
            }
            else if (answer == "н")
            {
                return false;
            }
            else
            {
                Console.WriteLine("Ошибка ввода!");
            }
        }
    }

    static void PlayGuessGame()
    {
        double a = GetValidDouble("Введите a: ");
        double b = GetValidDouble("Введите b: ");
        
        double correctAnswer = CalculateFunction(a, b);
        double roundedAnswer = Math.Round(correctAnswer, 2);
        
        int attempts = 3;
        bool guessed = false;
        
        while (attempts > 0 && !guessed)
        {
            Console.WriteLine($"Осталось попыток: {attempts}");
            double userAnswer = GetValidDouble("Введите ваш ответ: ");
            double userRounded = Math.Round(userAnswer, 2);
            
            if (userRounded == roundedAnswer)
            {
                guessed = true;
                Console.WriteLine("Ответ верный!");
            }
            else
            {
                attempts--;
                if (attempts > 0)
                {
                    Console.WriteLine("Ответ неверный!");
                }
            }
        }
        
        if (!guessed)
        {
            Console.WriteLine($"Правильный ответ: {roundedAnswer:F2}");
        }
        
        Console.WriteLine("Нажмите любую клавишу для продолжения...");
        Console.ReadKey();
    }

    static double CalculateFunction(double a, double b)
    {
        const double PI = Math.PI;
        double numerator = Math.Pow(Math.Cos(PI), 7) + Math.Sqrt(Math.Log(Math.Pow(b, 4)));
        double denominator = Math.Pow(Math.Sin(PI/2 + a), 2);
        return numerator / denominator;
    }

    static double GetValidDouble(string prompt)
    {
        double value;
        while (true)
        {
            Console.Write(prompt);
            if (double.TryParse(Console.ReadLine(), out value))
            {
                return value;
            }
            Console.WriteLine("Ошибка ввода! Введите число:");
        }
    }
}