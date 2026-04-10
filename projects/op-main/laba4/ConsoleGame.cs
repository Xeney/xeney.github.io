using System;
using System.Numerics;
using System.Reflection;
using static System.Runtime.InteropServices.JavaScript.JSType;

class ConsoleGame
{
    // по возможности сделать игру с ботом
    public static void Run()
    {
        byte rows = 6;
        byte cols = 7;
        char[,] screen = InitScreen(rows, cols);
        char player1 = 'X';
        char player2 = 'O';
        while (true)
        {
            Console.Clear();
            HelloScreen();
            Console.Write("Введите команду: /");
            switch (Console.ReadLine())
            {
                case "start":
                    screen = InitScreen(rows, cols);
                    RunGame(player1, player2, screen);
                    Console.Write("Нажмите Enter чтобы продолжить...");
                    Console.ReadKey();
                    break;
                case "rules":
                    RulesGame();
                    Console.Write("Нажмите Enter чтобы продолжить...");
                    Console.ReadKey();
                    break;
                case "setting":
                    Settings(out rows, out cols);
                    Console.Write("Нажмите Enter чтобы продолжить...");
                    Console.ReadKey();
                    break;
                case "exit":
                    Console.Clear();
                    return;
                default:
                    Console.Write("Команда не найдена!\nНажмите Enter чтобы повторить...");
                    Console.ReadKey();
                    break;
            }
        }
    }

    public static void Settings(out byte rows, out byte cols)
    {
        rows = 6; cols = 7;
        Console.Clear();
        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine("=====================================");
        Console.WriteLine("            НАСТРОЙКИ ИГРЫ");
        Console.WriteLine("=====================================\n");
        Console.ForegroundColor = ConsoleColor.DarkCyan;
        Console.WriteLine("Вы можете изменить размер игрового поля,");
        Console.WriteLine("чтобы сделать игру проще или сложнее.\n");
        Console.WriteLine("РАЗМЕР ПОЛЯ:");
        Console.WriteLine("По умолчанию — 6 строк и 7 столбцов.\n");
        Console.WriteLine("Введите желаемый размер поля:");
        Console.WriteLine(" - Количество строк (4–10)");
        Console.WriteLine(" - Количество столбцов (4–10)\n");
        Console.WriteLine("=====================================\n");
        Console.ResetColor();

        bool correctInput = false;
        while (!correctInput)
        {
            rows = GetMove("Строки: ");
            cols = GetMove("Столбцы: ");
            if (cols == 0 && rows == 0)
            {
                correctInput = true; continue;
            }
            if (!(cols < 11 && rows < 11
                && cols > 3 && rows > 3))
            {
                Console.WriteLine("Неверное значение!");
            } else { correctInput = true; continue; }
        }

        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine($"\nУстановлен размер поля: {rows} x {cols}");
        Console.ResetColor();
    }

    public static void RunGame(char player1, char player2, char[,] GameScreen)
    {
        bool GameWork = true;
        bool player   = true;
        while (GameWork)
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("=====================================");
            Console.WriteLine("        ИГРА \"ЧЕТЫРЕ В РЯД\"");
            Console.WriteLine("=====================================\n");
            Console.ForegroundColor = ConsoleColor.DarkCyan;
            Console.WriteLine("ЦЕЛЬ:");
            Console.WriteLine("Собери линию из четырёх своих фишек подряд");
            Console.WriteLine("по горизонтали, вертикали или диагонали.\n");
            Console.WriteLine("=====================================\n");
            Console.ResetColor();

            if (IsScreenFull(GameScreen))
            {
                PrintScreen(GameScreen, player1, player2);
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("Ничья! Победила дружба :)");
                Console.ResetColor();
                GameWork = false; continue;
            }
            if (CheckWin(GameScreen, player1))
            {
                PrintScreen(GameScreen, player1, player2);
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("Победа! Победил игрок #1");
                Console.ResetColor();
                GameWork = false; continue;
            } else if (CheckWin(GameScreen, player2))
            {
                PrintScreen(GameScreen, player1, player2);
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("Победа! Победил игрок #2");
                Console.ResetColor();
                GameWork = false; continue;
            }

            PrintScreen(GameScreen, player1, player2);

            bool result;
            if (player)
            {
                result = PlaceDisc(GameScreen, GetMove("Игрок #1 выбирает столбец: "), player1);
                if (!result){
                    Console.Write("Нажмите Enter чтобы продолжить...");
                    Console.ReadKey();
                    continue;
                }
                player = !player;
            } else
            {
                result = PlaceDisc(GameScreen, GetMove("Игрок #2 выбирает столбец: "), player2);
                if (!result){
                    Console.Write("Нажмите Enter чтобы продолжить...");
                    Console.ReadKey();
                    continue;
                }
                player = !player;
            }
        }
    }

    public static void HelloScreen()
    {
        Console.Clear();
        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine("=====================================");
        Console.WriteLine("        ИГРА \"ЧЕТЫРЕ В РЯД\"");
        Console.WriteLine("=====================================\n");
        Console.ForegroundColor = ConsoleColor.DarkCyan;
        Console.WriteLine("Автор: Варламов Дамир, группа 6105\n");
        Console.WriteLine("=====================================\n");
        Console.WriteLine("ДОСТУПНЫЕ КОМАНДЫ:");
        Console.WriteLine("-------------------------------------");
        Console.WriteLine("/start    - начать новую игру");
        Console.WriteLine("/rules    - правила игры");
        Console.WriteLine("/setting  - настройки игры");
        Console.WriteLine("/exit     - выход из игры");
        Console.WriteLine("=====================================\n");
        Console.ResetColor();
    }

    public static void RulesGame()
    {
        Console.Clear();
        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine("=====================================");
        Console.WriteLine("        ИГРА \"ЧЕТЫРЕ В РЯД\"");
        Console.WriteLine("=====================================\n");
        Console.ForegroundColor = ConsoleColor.DarkCyan;
        Console.WriteLine("ЦЕЛЬ:");
        Console.WriteLine("Собери линию из четырёх своих фишек подряд");
        Console.WriteLine("по горизонтали, вертикали или диагонали.\n");
        Console.WriteLine("-------------------------------------");
        Console.WriteLine("ПРАВИЛА:");
        Console.WriteLine("1. Игра проходит на поле 6 x 7.");
        Console.WriteLine("2. Игроки ходят по очереди: Игрок 1 — 'X', Игрок 2 — 'O'.");
        Console.WriteLine("3. На своём ходу игрок выбирает номер столбца (1–7).");
        Console.WriteLine("4. Фишка падает в самый нижний доступный ряд выбранного столбца.");
        Console.WriteLine("5. Побеждает тот, кто первым соберёт четыре свои фишки подряд.");
        Console.WriteLine("6. Если поле заполнено, а победителя нет — ничья.\n");
        Console.WriteLine("-------------------------------------");
        Console.WriteLine("УПРАВЛЕНИЕ:");
        Console.WriteLine("Вводи номер столбца и нажимай Enter.\n");
        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine("=====================================");
        Console.WriteLine("           УДАЧИ В ИГРЕ!");
        Console.WriteLine("=====================================\n");
        Console.ResetColor();
    }

    public static bool IsScreenFull(char[,] GameScreen)
    {
        foreach (char i in GameScreen)
        {
            if (i == ' ')
            {
                return false;
            }
        }
        return true;
    }

    public static bool PlaceDisc(char[,] GameScreen, byte column, char player)
    {
        column--;
        if (column < 0 || column >= GameScreen.GetLength(1))
        {
            Console.WriteLine("Столбец, который вы выбрали, не существует!");
            return false;
        }

        for (int row = GameScreen.GetLength(0) - 1; row >= 0; row--)
        {
            if (GameScreen[row, column] == ' ')
            {
                GameScreen[row, column] = player;
                return true;
            }
        }
        Console.WriteLine("Столбец заполнен!");
        return false;
    }


    public static byte GetMove(string message)
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
    public static char[,] InitScreen(byte column, byte row)
    {
        char[,] screen = new char[column, row];
        for (int i = 0; i < column; i++)
        {
            for (int j = 0; j < row; j++)
            {
                screen[i, j] = ' ';
            }
        }

        return screen;
    }

    public static bool CheckWin(char[,] GameScreen, char player)
    {
        int rows = GameScreen.GetLength(0);
        int cols = GameScreen.GetLength(1);

        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                if (GameScreen[i, j] != player)
                    continue;
                if (j + 3 < cols &&
                    GameScreen[i, j + 1] == player &&
                    GameScreen[i, j + 2] == player &&
                    GameScreen[i, j + 3] == player)
                {
                    return true;
                }
                if (i + 3 < rows &&
                    GameScreen[i + 1, j] == player &&
                    GameScreen[i + 2, j] == player &&
                    GameScreen[i + 3, j] == player)
                {
                    return true;
                }
                if (i + 3 < rows && j + 3 < cols &&
                    GameScreen[i + 1, j + 1] == player &&
                    GameScreen[i + 2, j + 2] == player &&
                    GameScreen[i + 3, j + 3] == player)
                {
                    return true;
                }
                if (i - 3 >= 0 && j + 3 < cols &&
                    GameScreen[i - 1, j + 1] == player &&
                    GameScreen[i - 2, j + 2] == player &&
                    GameScreen[i - 3, j + 3] == player)
                {
                    return true;
                }
            }
        }
        return false;
    }


    public static void PrintScreen(char[,] GameScreen, char player1, char player2)
    {
        int j = 0;
        for (int i = 0; i < GameScreen.GetLength(0); i++)
        {
            Console.BackgroundColor = ConsoleColor.DarkBlue;
            Console.WriteLine("  ");
            Console.Write("#" + (1 + i));
            Console.ResetColor();
            for (j = 0; j < GameScreen.GetLength(1); j++)
            {
                // Console.Write("\t" + "|" + GameScreen[i, j] + "|");
                Console.Write("\t" + "|");
                if (GameScreen[i, j] == player1)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.Cyan;
                }
                Console.Write(GameScreen[i, j]);
                Console.ResetColor();
                Console.Write("|");
            }
            Console.WriteLine(" ");
        }
        Console.WriteLine();
        for (int i = 0; i < j; i++)
        {
            Console.BackgroundColor = ConsoleColor.DarkBlue;
            Console.Write("\t#" + (1 + i) + " ");
            Console.ResetColor();
        }
        Console.WriteLine();
    }
}