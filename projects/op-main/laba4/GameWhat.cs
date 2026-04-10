using System;

static class GameWhat
{
    public static void PlayGuessGame()
    {
        double a = InputHelper.GetValidDouble("Введите a: ");
        double b = InputHelper.GetValidDouble("Введите b: ");

        double correctAnswer = CalculateFunction(a, b);
        GuessNumber(correctAnswer);

        Console.WriteLine("Нажмите любую клавишу для продолжения...");
        Console.ReadKey();
    }

    private static double CalculateFunction(double a, double b)
    {
        const double PI = Math.PI;
        double numerator = Math.Pow(Math.Cos(PI), 7) + Math.Sqrt(Math.Log(Math.Pow(b, 4)));
        double denominator = Math.Pow(Math.Sin(PI / 2 + a), 2);
        return numerator / denominator;
    }

    private static void GuessNumber(double correctAnswer)
    {
        double roundedAnswer = Math.Round(correctAnswer, 2);
        int attempts = 3;
        bool guessed = false;

        while (attempts > 0 && !guessed)
        {
            Console.WriteLine($"Осталось попыток: {attempts}");
            double userAnswer = InputHelper.GetValidDouble("Введите ваш ответ: ");
            double userRounded = Math.Round(userAnswer, 2);

            if (userRounded == roundedAnswer)
            {   
                guessed = true;
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("Ответ верный!");
                Console.ResetColor();
            }
            else
            {
                attempts--;
                if (attempts > 0)
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("Ответ неверный!");
                    Console.ResetColor();
            }
        }

        if (!guessed)
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine($"Правильный ответ: {roundedAnswer:F2}");
            Console.ResetColor();
            
    }
}
