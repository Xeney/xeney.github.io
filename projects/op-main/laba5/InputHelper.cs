using System;

/// <summary>
/// Статический класс для проверки и валидации вводимых данных
/// </summary>
static class InputHelper
{
    /// <summary>
    /// Получает корректное double значение от пользователя
    /// </summary>
    /// <param name="prompt">Сообщение для пользователя</param>
    /// <returns>Корректное double значение</returns>
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

    /// <summary>
    /// Получает корректный размер массива от пользователя
    /// </summary>
    /// <returns>Корректный размер массива</returns>
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

    /// <summary>
    /// Получает корректное byte значение от пользователя
    /// </summary>
    /// <param name="message">Сообщение для пользователя</param>
    /// <returns>Корректное byte значение</returns>
    public static byte GetByte(string message)
    {
        byte result;
        Console.Write(message);
        while (!(byte.TryParse(Console.ReadLine(), out result) && result > 0))
        {
            Console.WriteLine("Неверный ввод! Попробуйте ещё раз...");
            Console.Write(message);
        }
        return result;
    }
}