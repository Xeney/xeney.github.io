using System;

/// <summary>
/// Главный класс программы
/// </summary>
class Program
{
    /// <summary>
    /// Главный метод программы
    /// </summary>
    static void Main()
    {
        bool exitProgram = false;

        while (!exitProgram)
        {
            Console.Clear();
            ShowMainMenu();

            Console.Write("Выберите действие: ");
            string? choice = Console.ReadLine();

            switch (choice)
            {
                case "1":
                    Console.Clear();
                    GameWhat.PlayGuessGame();
                    break;
                case "2":
                    Console.Clear();
                    AuthorInfo.ShowAuthorInfo();
                    break;
                case "3":
                    Console.Clear();
                    DemonstrateArrayProcessors();
                    break;
                case "4":
                    Console.Clear();
                    ConnectFourGame game = new ConnectFourGame();
                    game.Run();
                    break;
                case "5":
                    Console.Clear();
                    exitProgram = ExitProgram();
                    break;
                default:
                    ShowError("Команда не найдена!");
                    break;
            }
        }
    }

    /// <summary>
    /// Показывает главное меню
    /// </summary>
    private static void ShowMainMenu()
    {
        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine("=====================================");
        Console.WriteLine("         КОНСОЛЬНОЕ ПРИЛОЖЕНИЕ");
        Console.WriteLine("=====================================\n");
        Console.ForegroundColor = ConsoleColor.DarkCyan;
        Console.WriteLine("1. Игра \"Отгадай ответ\"");
        Console.WriteLine("2. Об авторе");
        Console.WriteLine("3. Сортировка массива");
        Console.WriteLine("4. Игра \"4 в ряд\"");
        Console.WriteLine("5. Выход");
        Console.WriteLine("=====================================\n");
        Console.ResetColor();
    }

    /// <summary>
    /// Демонстрирует работу с ArrayProcessor (оба конструктора)
    /// </summary>
    private static void DemonstrateArrayProcessors()
    {
        // Демонстрация конструктора по умолчанию
        Console.WriteLine("=== Создание ArrayProcessor конструктором по умолчанию ===");
        ArrayProcessor processor1 = new ArrayProcessor();
        processor1.SortArray();

        Console.WriteLine("\n=== Создание ArrayProcessor конструктором с параметрами ===");
        int size = InputHelper.GetArraySize();
        ArrayProcessor processor2 = new ArrayProcessor(size);
        processor2.SortArray();
    }

    /// <summary>
    /// Показывает сообщение об ошибке
    /// </summary>
    /// <param name="message">Текст сообщения</param>
    private static void ShowError(string message)
    {
        Console.ForegroundColor = ConsoleColor.Red;
        Console.WriteLine(message);
        Console.ResetColor();
        Console.WriteLine("Нажмите Enter чтобы продолжить...");
        Console.ReadKey();
        Console.Clear();
    }

    /// <summary>
    /// Подтверждение выхода из программы
    /// </summary>
    /// <returns>True если выход подтвержден, иначе False</returns>
    private static bool ExitProgram()
    {
        while (true)
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.Write("Вы уверены, что хотите выйти? (д/н): ");
            Console.ResetColor();
            string? answer = Console.ReadLine()?.ToLower();

            Console.ForegroundColor = ConsoleColor.Red;
            if (answer == "д") return true;
            else if (answer == "н") return false;
            else Console.WriteLine("Ошибка ввода!");
            Console.ResetColor();
        }
    }
}