using System;

class Program
{
    static void Main()
    {
        bool exitProgram = false;

        while (!exitProgram)
        {
            Console.Clear();
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
            
            Console.Write("Выберите действие: ");
            string? choice = Console.ReadLine();

            switch (choice)
            {
                case "1":
                    Console.Clear();
                    GameWhat.PlayGuessGame();
                    Console.Clear();
                    break;
                case "2":
                    Console.Clear();
                    AuthorInfo.ShowAuthorInfo();
                    Console.Clear();
                    break;
                case "3":
                    Console.Clear();
                    ArraySorter.SortArray();
                    Console.Clear();
                    break;
                case "4":
                    Console.Clear();
                    ConsoleGame.Run();
                    Console.Clear();
                    break;
                case "5":
                    Console.Clear();
                    exitProgram = ExitProgram();
                    Console.Clear();
                    break;
                default:
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("Команда не найдена!");
                    Console.ResetColor();

                    Console.WriteLine("Нажмите Enter чтобы продолжить...");
                    Console.ReadKey();
                    Console.Clear();
                    break;
            }
        }
    }
    static bool ExitProgram()
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
