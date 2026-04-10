using System;

/// <summary>
/// Класс для реализации игры "4 в ряд"
/// </summary>
class ConnectFourGame
{
    private const byte DEFAULT_ROWS = 6;
    private const byte DEFAULT_COLS = 7;
    private const char PLAYER1_SYMBOL = 'X';
    private const char PLAYER2_SYMBOL = 'O';
    private const char EMPTY_SYMBOL = ' ';

    private byte _rows;
    private byte _cols;
    private char[,] _gameScreen;

    /// <summary>
    /// Конструктор по умолчанию
    /// </summary>
    public ConnectFourGame()
    {
        _rows = DEFAULT_ROWS;
        _cols = DEFAULT_COLS;
        _gameScreen = InitScreen(_rows, _cols);
    }

    /// <summary>
    /// Конструктор с параметрами размера поля
    /// </summary>
    /// <param name="rows">Количество строк</param>
    /// <param name="cols">Количество столбцов</param>
    public ConnectFourGame(byte rows, byte cols)
    {
        _rows = rows;
        _cols = cols;
        _gameScreen = InitScreen(_rows, _cols);
    }

    /// <summary>
    /// Запускает главный цикл игры
    /// </summary>
    public void Run()
    {
        while (true)
        {
            Console.Clear();
            ShowHelloScreen();
            Console.Write("Введите команду: /");
            switch (Console.ReadLine())
            {
                case "start":
                    _gameScreen = InitScreen(_rows, _cols);
                    RunGame();
                    Console.Write("Нажмите Enter чтобы продолжить...");
                    Console.ReadKey();
                    break;
                case "rules":
                    ShowRules();
                    Console.Write("Нажмите Enter чтобы продолжить...");
                    Console.ReadKey();
                    break;
                case "setting":
                    Settings();
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

    /// <summary>
    /// Настройки размера игрового поля
    /// </summary>
    public void Settings()
    {
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
            byte newRows = InputHelper.GetByte("Строки: ");
            byte newCols = InputHelper.GetByte("Столбцы: ");
            
            if (newCols < 11 && newRows < 11 && newCols > 3 && newRows > 3)
            {
                _rows = newRows;
                _cols = newCols;
                _gameScreen = InitScreen(_rows, _cols);
                correctInput = true;
            }
            else
            {
                Console.WriteLine("Неверное значение! Допустимый диапазон: 4-10");
            }
        }

        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine($"\nУстановлен размер поля: {_rows} x {_cols}");
        Console.ResetColor();
    }

    /// <summary>
    /// Запускает игровой процесс
    /// </summary>
    private void RunGame()
    {
        bool gameRunning = true;
        bool currentPlayer = true; // true - игрок 1, false - игрок 2

        while (gameRunning)
        {
            Console.Clear();
            ShowGameHeader();

            if (IsScreenFull())
            {
                PrintScreen();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("Ничья! Победила дружба :)");
                Console.ResetColor();
                gameRunning = false;
                continue;
            }

            if (CheckWin(PLAYER1_SYMBOL))
            {
                PrintScreen();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("Победа! Победил игрок #1");
                Console.ResetColor();
                gameRunning = false;
                continue;
            }
            else if (CheckWin(PLAYER2_SYMBOL))
            {
                PrintScreen();
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("Победа! Победил игрок #2");
                Console.ResetColor();
                gameRunning = false;
                continue;
            }

            PrintScreen();

            bool result;
            if (currentPlayer)
            {
                result = PlaceDisc(InputHelper.GetByte("Игрок #1 выбирает столбец: "), PLAYER1_SYMBOL);
                if (result)
                    currentPlayer = !currentPlayer;
            }
            else
            {
                result = PlaceDisc(InputHelper.GetByte("Игрок #2 выбирает столбец: "), PLAYER2_SYMBOL);
                if (result)
                    currentPlayer = !currentPlayer;
            }

            if (!result)
            {
                Console.Write("Нажмите Enter чтобы продолжить...");
                Console.ReadKey();
            }
        }
    }

    /// <summary>
    /// Показывает стартовый экран
    /// </summary>
    private void ShowHelloScreen()
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

    /// <summary>
    /// Показывает правила игры
    /// </summary>
    private void ShowRules()
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
        Console.WriteLine($"1. Игра проходит на поле {_rows} x {_cols}.");
        Console.WriteLine("2. Игроки ходят по очереди: Игрок 1 — 'X', Игрок 2 — 'O'.");
        Console.WriteLine($"3. На своём ходу игрок выбирает номер столбца (1–{_cols}).");
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

    /// <summary>
    /// Показывает заголовок игры
    /// </summary>
    private void ShowGameHeader()
    {
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
    }

    /// <summary>
    /// Проверяет, заполнено ли игровое поле полностью
    /// </summary>
    /// <returns>True если поле заполнено, иначе False</returns>
    private bool IsScreenFull()
    {
        foreach (char cell in _gameScreen)
        {
            if (cell == EMPTY_SYMBOL)
                return false;
        }
        return true;
    }

    /// <summary>
    /// Размещает фишку в указанном столбце
    /// </summary>
    /// <param name="column">Номер столбца</param>
    /// <param name="player">Символ игрока</param>
    /// <returns>True если фишка размещена успешно, иначе False</returns>
    private bool PlaceDisc(byte column, char player)
    {
        column--;
        if (column < 0 || column >= _cols)
        {
            Console.WriteLine("Столбец, который вы выбрали, не существует!");
            return false;
        }

        for (int row = _rows - 1; row >= 0; row--)
        {
            if (_gameScreen[row, column] == EMPTY_SYMBOL)
            {
                _gameScreen[row, column] = player;
                return true;
            }
        }
        Console.WriteLine("Столбец заполнен!");
        return false;
    }

    /// <summary>
    /// Инициализирует игровое поле
    /// </summary>
    /// <param name="rows">Количество строк</param>
    /// <param name="cols">Количество столбцов</param>
    /// <returns>Инициализированное игровое поле</returns>
    private char[,] InitScreen(byte rows, byte cols)
    {
        char[,] screen = new char[rows, cols];
        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                screen[i, j] = EMPTY_SYMBOL;
            }
        }
        return screen;
    }

    /// <summary>
    /// Проверяет, есть ли выигрышная комбинация
    /// </summary>
    /// <param name="player">Символ игрока для проверки</param>
    /// <returns>True если есть выигрышная комбинация, иначе False</returns>
    private bool CheckWin(char player)
    {
        int rows = _gameScreen.GetLength(0);
        int cols = _gameScreen.GetLength(1);

        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                if (_gameScreen[i, j] != player)
                    continue;

                // Проверка горизонтали
                if (j + 3 < cols &&
                    _gameScreen[i, j + 1] == player &&
                    _gameScreen[i, j + 2] == player &&
                    _gameScreen[i, j + 3] == player)
                    return true;

                // Проверка вертикали
                if (i + 3 < rows &&
                    _gameScreen[i + 1, j] == player &&
                    _gameScreen[i + 2, j] == player &&
                    _gameScreen[i + 3, j] == player)
                    return true;

                // Проверка диагонали (вправо-вниз)
                if (i + 3 < rows && j + 3 < cols &&
                    _gameScreen[i + 1, j + 1] == player &&
                    _gameScreen[i + 2, j + 2] == player &&
                    _gameScreen[i + 3, j + 3] == player)
                    return true;

                // Проверка диагонали (вправо-вверх)
                if (i - 3 >= 0 && j + 3 < cols &&
                    _gameScreen[i - 1, j + 1] == player &&
                    _gameScreen[i - 2, j + 2] == player &&
                    _gameScreen[i - 3, j + 3] == player)
                    return true;
            }
        }
        return false;
    }

    /// <summary>
    /// Выводит игровое поле на экран
    /// </summary>
    private void PrintScreen()
    {
        for (int i = 0; i < _rows; i++)
        {
            Console.BackgroundColor = ConsoleColor.DarkBlue;
            Console.Write("  ");
            Console.Write("#" + (1 + i));
            Console.ResetColor();
            
            for (int j = 0; j < _cols; j++)
            {
                Console.Write("\t" + "|");
                if (_gameScreen[i, j] == PLAYER1_SYMBOL)
                    Console.ForegroundColor = ConsoleColor.Red;
                else
                    Console.ForegroundColor = ConsoleColor.Cyan;
                
                Console.Write(_gameScreen[i, j]);
                Console.ResetColor();
                Console.Write("|");
            }
            Console.WriteLine(" ");
        }
        
        Console.WriteLine();
        for (int i = 0; i < _cols; i++)
        {
            Console.BackgroundColor = ConsoleColor.DarkBlue;
            Console.Write("\t#" + (1 + i) + " ");
            Console.ResetColor();
        }
        Console.WriteLine();
    }
}