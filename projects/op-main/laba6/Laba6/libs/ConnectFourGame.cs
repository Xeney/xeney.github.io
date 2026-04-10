using System;

namespace Laba6
{
    /// <summary>
    /// Класс для реализации игры "4 в ряд" (Connect Four)
    /// </summary>
    public class ConnectFourGame
    {
        private const char PLAYER1_SYMBOL = 'X';
        private const char PLAYER2_SYMBOL = 'O';
        private const char EMPTY_SYMBOL = ' ';

        private byte _rows;
        private byte _cols;
        private char[,] _gameBoard;
        private bool _currentPlayer;

        /// <summary>
        /// Получает количество строк игрового поля
        /// </summary>
        public byte Rows => _rows;

        /// <summary>
        /// Получает количество столбцов игрового поля
        /// </summary>
        public byte Cols => _cols;

        /// <summary>
        /// Получает копию игрового поля
        /// </summary>
        public char[,] GameBoard => (char[,])_gameBoard.Clone();

        /// <summary>
        /// Получает текущего игрока (true - игрок 1, false - игрок 2)
        /// </summary>
        public bool CurrentPlayer => _currentPlayer;

        /// <summary>
        /// Получает символ текущего игрока
        /// </summary>
        public char CurrentPlayerSymbol => _currentPlayer ? PLAYER1_SYMBOL : PLAYER2_SYMBOL;

        /// <summary>
        /// Конструктор по умолчанию (6x7 поле)
        /// </summary>
        public ConnectFourGame() : this(6, 7) { }

        /// <summary>
        /// Конструктор с параметрами размера поля
        /// </summary>
        /// <param name="rows">Количество строк</param>
        /// <param name="cols">Количество столбцов</param>
        public ConnectFourGame(byte rows, byte cols)
        {
            if (rows < 4 || rows > 10 || cols < 4 || cols > 10)
                throw new ArgumentException("Размер поля должен быть от 4x4 до 10x10");

            _rows = rows;
            _cols = cols;
            _gameBoard = new char[rows, cols];
            _currentPlayer = true; // Начинает игрок 1
            InitializeBoard();
        }

        /// <summary>
        /// Инициализирует игровое поле пустыми значениями
        /// </summary>
        private void InitializeBoard()
        {
            for (int i = 0; i < _rows; i++)
                for (int j = 0; j < _cols; j++)
                    _gameBoard[i, j] = EMPTY_SYMBOL;
        }

        /// <summary>
        /// Размещает фишку в указанном столбце
        /// </summary>
        /// <param name="column">Номер столбца (от 0 до Cols-1)</param>
        /// <returns>True если фишка размещена успешно, иначе False</returns>
        public bool PlaceDisc(int column)
        {
            if (column < 0 || column >= _cols)
                return false;

            // Находим первую свободную ячейку сверху вниз
            for (int row = _rows - 1; row >= 0; row--)
            {
                if (_gameBoard[row, column] == EMPTY_SYMBOL)
                {
                    _gameBoard[row, column] = CurrentPlayerSymbol;
                    _currentPlayer = !_currentPlayer; // Смена игрока
                    return true;
                }
            }
            return false; // Столбец заполнен
        }

        /// <summary>
        /// Проверяет, есть ли выигрышная комбинация на поле
        /// </summary>
        /// <returns>True если есть победитель, иначе False</returns>
        public bool CheckWin()
        {
            char playerSymbol = _currentPlayer ? PLAYER2_SYMBOL : PLAYER1_SYMBOL;

            // Проверка горизонтали
            for (int row = 0; row < _rows; row++)
            {
                for (int col = 0; col < _cols - 3; col++)
                {
                    if (_gameBoard[row, col] == playerSymbol &&
                        _gameBoard[row, col + 1] == playerSymbol &&
                        _gameBoard[row, col + 2] == playerSymbol &&
                        _gameBoard[row, col + 3] == playerSymbol)
                        return true;
                }
            }

            // Проверка вертикали
            for (int row = 0; row < _rows - 3; row++)
            {
                for (int col = 0; col < _cols; col++)
                {
                    if (_gameBoard[row, col] == playerSymbol &&
                        _gameBoard[row + 1, col] == playerSymbol &&
                        _gameBoard[row + 2, col] == playerSymbol &&
                        _gameBoard[row + 3, col] == playerSymbol)
                        return true;
                }
            }

            // Проверка диагонали (вправо-вниз)
            for (int row = 0; row < _rows - 3; row++)
            {
                for (int col = 0; col < _cols - 3; col++)
                {
                    if (_gameBoard[row, col] == playerSymbol &&
                        _gameBoard[row + 1, col + 1] == playerSymbol &&
                        _gameBoard[row + 2, col + 2] == playerSymbol &&
                        _gameBoard[row + 3, col + 3] == playerSymbol)
                        return true;
                }
            }

            // Проверка диагонали (влево-вниз)
            for (int row = 0; row < _rows - 3; row++)
            {
                for (int col = 3; col < _cols; col++)
                {
                    if (_gameBoard[row, col] == playerSymbol &&
                        _gameBoard[row + 1, col - 1] == playerSymbol &&
                        _gameBoard[row + 2, col - 2] == playerSymbol &&
                        _gameBoard[row + 3, col - 3] == playerSymbol)
                        return true;
                }
            }

            return false;
        }

        /// <summary>
        /// Проверяет, заполнено ли игровое поле полностью
        /// </summary>
        /// <returns>True если поле заполнено, иначе False</returns>
        public bool IsBoardFull()
        {
            for (int col = 0; col < _cols; col++)
            {
                if (_gameBoard[0, col] == EMPTY_SYMBOL)
                    return false;
            }
            return true;
        }

        /// <summary>
        /// Сбрасывает игровое поле для новой игры
        /// </summary>
        public void ResetGame()
        {
            InitializeBoard();
            _currentPlayer = true;
        }

        /// <summary>
        /// Получает символ игрока по строке и столбцу
        /// </summary>
        /// <param name="row">Строка</param>
        /// <param name="col">Столбец</param>
        /// <returns>Символ в указанной ячейке</returns>
        public char GetCellSymbol(int row, int col)
        {
            if (row < 0 || row >= _rows || col < 0 || col >= _cols)
                return EMPTY_SYMBOL;

            return _gameBoard[row, col];
        }
    }
}