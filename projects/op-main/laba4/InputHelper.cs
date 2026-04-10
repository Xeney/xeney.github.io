using System;

static class InputHelper
{
    public static double GetValidDouble(string prompt)
    {
        double value;
        while (true)
        {
            Console.Write(prompt);
            if (double.TryParse(Console.ReadLine(), out value))
                return value;
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("Ошибка! Введите число.");
            Console.ResetColor();
        }
    }

    public static int GetArraySize()
    {
        int size;
        while (true)
        {
            Console.Write("Введите размер массива: ");
            if (int.TryParse(Console.ReadLine(), out size) && size > 0)
                return size;
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("Ошибка! Размер должен быть положительным числом.");
            Console.ResetColor();
        }
    }
}
