using System;

/// <summary>
/// Статический класс для отображения информации об авторе
/// </summary>
static class AuthorInfo
{
    /// <summary>
    /// Показывает информацию об авторе
    /// </summary>
    public static void ShowAuthorInfo()
    {
        Console.Clear();
        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine("=====================================");
        Console.WriteLine("         ИНФОРМАЦИЯ ОБ АВТОРЕ");
        Console.WriteLine("=====================================\n");
        Console.ForegroundColor = ConsoleColor.DarkCyan;
        Console.WriteLine("Варламов Дамир Алексеевич");
        Console.WriteLine("Группа: 6105-090301D\n");
        Console.WriteLine("=====================================\n");
        Console.ResetColor();
        Console.WriteLine("Нажмите любую клавишу для продолжения...");
        Console.ReadKey();
    }
}