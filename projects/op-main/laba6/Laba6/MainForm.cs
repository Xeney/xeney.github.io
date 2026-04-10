using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;

namespace Laba6
{
    public partial class MainForm : Form
    {
        // Экземпляр игры "4 в ряд"
        private ConnectFourGame _game;
        // Хранение ссылок на кнопки UI
        private Button[,] gameButtons;

        private ArrayProcessor _arrayProcessor;
        private int _minIndex = -1;
        private int _maxIndex = -1;

        // Добавляем недостающие поля для кнопок
        private Button btnUpdateArrayStats;
        private Button btnClearArray;
        private Button btnGenerateRandom;
        private Button btnCreateCustom;
        private Button btnShellSort;
        private Button btnCompareSort;

        public MainForm()
        {
            InitializeComponent();
            InitializeArrayTab();
            InitializeAuthorInfo();

            // игра 4 в ряд
            _game = new ConnectFourGame();
            InitializeGameScreen();
            UpdateStatusLabel();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {

        }

        private void set_gameWhat_Click(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void MainForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            var result = MessageBox.Show(
                "Вы уверены, что хотите выйти?",
                "Подтверждение выхода",
                MessageBoxButtons.YesNo,
                MessageBoxIcon.Question
            );

            if (result == DialogResult.No)
                e.Cancel = true;
        }

        private void Menu_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        // Игра Отгадай ответ
        private void GameWhat_Click(object sender, EventArgs e)
        {

        }

        private void checkGameWhat_Click(object sender, EventArgs e)
        {
            double a, b, userInputRes, calcFuncRes;
            int attempts;

            try
            {
                a = GameLogic.GetValidDouble(textBox1.Text, "A");
                b = GameLogic.GetValidDouble(textBox2.Text, "B");
                userInputRes = GameLogic.GetValidDouble(textBoxResult.Text, "Ответ");
                attempts = GameLogic.GetValidInt(attemptsTextBox.Text, "Попытки");
                calcFuncRes = GameLogic.CalculateFunction(a, b);
            }
            catch (ArgumentException ex)
            {
                MessageBox.Show(ex.Message, "Ошибка ввода", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Уменьшаем количество попыток при неверном ответе
            if (!GameLogic.CheckAnswer(userInputRes, calcFuncRes))
            {
                attempts--;
                attemptsTextBox.Text = attempts.ToString();
            }

            // Логика отображения результатов
            if (attempts < 0)
            {
                result.ForeColor = Color.Red;
                result.Text = "Попытки закончились, вы проиграли.";
            }
            else if (calcFuncRes == userInputRes)
            {
                result.ForeColor = Color.Green;
                result.Text = $"Верно! Ответ: {calcFuncRes:F2}";
            }
            else
            {
                result.ForeColor = Color.Red;
                result.Text = attempts == 0
                    ? $"Неверно! Правильный ответ: {calcFuncRes:F2}"
                    : "Неверно! Попробуйте еще раз.";
            }
        }

        private void arraySort_Click(object sender, EventArgs e)
        {
        }

        /// <summary>
        /// Инициализирует вкладку работы с массивами
        /// </summary>
        private void InitializeArrayTab()
        {
            // Инициализация DataGridView
            dataGridViewArray.AutoGenerateColumns = false;
            dataGridViewArray.Columns.Clear();

            dataGridViewArray.Columns.Add(new DataGridViewTextBoxColumn()
            {
                Name = "Index",
                HeaderText = "Индекс",
                ReadOnly = true,
                Width = 60
            });

            dataGridViewArray.Columns.Add(new DataGridViewTextBoxColumn()
            {
                Name = "Value",
                HeaderText = "Значение",
                Width = 100
            });
        }

        /// <summary>
        /// Создает массив с размером по умолчанию
        /// </summary>
        private void btnCreateDefault_Click(object sender, EventArgs e)
        {
            try
            {
                _arrayProcessor = new ArrayProcessor();
                DisplayArray();
                UpdateArrayStats();
                ClearArrayHighlights();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при создании массива: {ex.Message}", "Ошибка",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Создает массив с пользовательским размером
        /// </summary>
        private void btnCreateCustom_Click_1(object sender, EventArgs e)
        {
            try
            {
                int size = GameLogic.GetValidInt(txtArraySize.Text, "размер массива");
                _arrayProcessor = new ArrayProcessor(size);
                DisplayArray();
                UpdateArrayStats();
                ClearArrayHighlights();
            }
            catch (ArgumentException ex)
            {
                MessageBox.Show(ex.Message, "Ошибка ввода", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при создании массива: {ex.Message}", "Ошибка",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Генерирует случайные значения для массива
        /// </summary>
        private void btnGenerateRandom_Click_1(object sender, EventArgs e)
        {
            if (_arrayProcessor == null)
            {
                MessageBox.Show("Сначала создайте массив!", "Информация",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                _arrayProcessor.GenerateRandomArray();
                DisplayArray();
                UpdateArrayStats();
                ClearArrayHighlights();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при генерации массива: {ex.Message}", "Ошибка",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Отображает массив в DataGridView
        /// </summary>
        private void DisplayArray()
        {
            dataGridViewArray.Rows.Clear();

            if (_arrayProcessor == null) return;

            var array = _arrayProcessor.Array;
            for (int i = 0; i < array.Length; i++)
            {
                dataGridViewArray.Rows.Add(i, array[i]);
            }

            HighlightMinMax();
        }

        /// <summary>
        /// Выделяет минимальный и максимальный элементы цветом
        /// </summary>
        private void HighlightMinMax()
        {
            if (_arrayProcessor == null) return;

            try
            {
                _minIndex = _arrayProcessor.FindMinIndex();
                _maxIndex = _arrayProcessor.FindMaxIndex();

                for (int i = 0; i < dataGridViewArray.Rows.Count; i++)
                {
                    var row = dataGridViewArray.Rows[i];
                    if (i == _minIndex)
                    {
                        row.DefaultCellStyle.BackColor = Color.LightBlue;
                        row.DefaultCellStyle.ForeColor = Color.DarkBlue;
                    }
                    else if (i == _maxIndex)
                    {
                        row.DefaultCellStyle.BackColor = Color.LightCoral;
                        row.DefaultCellStyle.ForeColor = Color.DarkRed;
                    }
                    else
                    {
                        row.DefaultCellStyle.BackColor = Color.White;
                        row.DefaultCellStyle.ForeColor = Color.Black;
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при выделении элементов: {ex.Message}", "Ошибка",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Снимает выделение с элементов массива
        /// </summary>
        private void ClearArrayHighlights()
        {
            _minIndex = -1;
            _maxIndex = -1;

            foreach (DataGridViewRow row in dataGridViewArray.Rows)
            {
                row.DefaultCellStyle.BackColor = Color.White;
                row.DefaultCellStyle.ForeColor = Color.Black;
            }
        }

        /// <summary>
        /// Обновляет статистику массива
        /// </summary>
        private void UpdateArrayStats()
        {
            if (_arrayProcessor == null) return;

            try
            {
                lblArrayMin.Text = $"Минимум: {_arrayProcessor.FindMin()}";
                lblArrayMax.Text = $"Максимум: {_arrayProcessor.FindMax()}";
                lblArrayAverage.Text = $"Среднее: {_arrayProcessor.CalculateAverage():F2}";
                lblArraySize.Text = $"Размер: {_arrayProcessor.Size}";
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при расчете статистики: {ex.Message}", "Ошибка",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Сортирует массив методом пузырька
        /// </summary>
        private void btnBubbleSort_Click_1(object sender, EventArgs e)
        {
            if (_arrayProcessor == null)
            {
                MessageBox.Show("Сначала создайте массив!", "Информация",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                var (sortedArray, timeMs) = _arrayProcessor.BubbleSort();

                // Обновляем массив в процессоре
                for (int i = 0; i < sortedArray.Length; i++)
                {
                    _arrayProcessor.UpdateValue(i, sortedArray[i]);
                }

                DisplayArray();
                UpdateArrayStats();

                MessageBox.Show($"Сортировка пузырьком выполнена за {timeMs} мс", "Информация",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при сортировке: {ex.Message}", "Ошибка",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Сортирует массив методом Шелла
        /// </summary>
        private void btnShellSort_Click_1(object sender, EventArgs e)
        {
            if (_arrayProcessor == null)
            {
                MessageBox.Show("Сначала создайте массив!", "Информация",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                var (sortedArray, timeMs) = _arrayProcessor.ShellSort();

                // Обновляем массив в процессоре
                for (int i = 0; i < sortedArray.Length; i++)
                {
                    _arrayProcessor.UpdateValue(i, sortedArray[i]);
                }

                DisplayArray();
                UpdateArrayStats();

                MessageBox.Show($"Сортировка Шелла выполнена за {timeMs} мс", "Информация",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при сортировке: {ex.Message}", "Ошибка",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Сравнивает время выполнения сортировок
        /// </summary>
        private void btnCompareSort_Click_1(object sender, EventArgs e)
        {
            if (_arrayProcessor == null)
            {
                MessageBox.Show("Сначала создайте массив!", "Информация",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            try
            {
                var (bubbleSorted, bubbleTime) = _arrayProcessor.BubbleSort();
                var (shellSorted, shellTime) = _arrayProcessor.ShellSort();

                string comparison = $"Сравнение времени сортировки:\n" +
                                  $"Сортировка пузырьком: {bubbleTime} мс\n" +
                                  $"Сортировка Шелла: {shellTime} мс\n" +
                                  $"Разница: {Math.Abs(bubbleTime - shellTime)} мс";

                MessageBox.Show(comparison, "Сравнение сортировок",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при сравнении сортировок: {ex.Message}", "Ошибка",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        /// <summary>
        /// Обрабатывает редактирование ячеек DataGridView
        /// </summary>
        private void dataGridViewArray_CellEndEdit(object sender, DataGridViewCellEventArgs e)
        {
            if (_arrayProcessor == null || e.RowIndex < 0 || e.ColumnIndex != 1) return;

            try
            {
                var cellValue = dataGridViewArray.Rows[e.RowIndex].Cells[1].Value?.ToString();
                if (string.IsNullOrEmpty(cellValue)) return;

                int value = GameLogic.GetValidInt(cellValue, "значение массива");
                _arrayProcessor.UpdateValue(e.RowIndex, value);

                UpdateArrayStats();
                HighlightMinMax();
            }
            catch (ArgumentException ex)
            {
                MessageBox.Show(ex.Message, "Ошибка ввода", MessageBoxButtons.OK, MessageBoxIcon.Error);
                DisplayArray(); // Восстанавливаем предыдущее значение
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при обновлении значения: {ex.Message}", "Ошибка",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
                DisplayArray();
            }
        }

        /// <summary>
        /// Очищает массив и форму
        /// </summary>
        private void btnClearArray_Click_1(object sender, EventArgs e)
        {
            _arrayProcessor = null;
            dataGridViewArray.Rows.Clear();
            ClearArrayHighlights();
            lblArrayMin.Text = "Минимум: ";
            lblArrayMax.Text = "Максимум: ";
            lblArrayAverage.Text = "Среднее: ";
            lblArraySize.Text = "Размер: ";
            txtArraySize.Text = "10";
        }

        /// <summary>
        /// Обновляет статистику массива
        /// </summary>
        private void btnUpdateArrayStats_Click_1(object sender, EventArgs e)
        {
            UpdateArrayStats();
            HighlightMinMax();
        }
        private void lblArrayMax_Click(object sender, EventArgs e)
        {

        }

        // Информация об авторе
        private void InitializeAuthorInfo()
        {
            textAuthor.Text = AuthorInfo.GetAuthorInfo();
        }

        // Игра "4 в ряд"

        /// <summary>
        /// Метод инициализации игрового поля UI
        /// </summary>
        private void InitializeGameScreen()
        {
            int rows = _game.Rows;
            int cols = _game.Cols;

            ScreenGame.RowCount = rows;
            ScreenGame.ColumnCount = cols;
            ScreenGame.CellBorderStyle = TableLayoutPanelCellBorderStyle.None;

            gameButtons = new Button[rows, cols];

            // Настройка стилей строк и столбцов
            ScreenGame.ColumnStyles.Clear();
            ScreenGame.RowStyles.Clear();
            for (int i = 0; i < cols; i++)
                ScreenGame.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100f / cols)); // фишка с процентами для нормального размера
            for (int i = 0; i < rows; i++)
                ScreenGame.RowStyles.Add(new RowStyle(SizeType.Percent, 100f / rows));

            // Заполнение ячеек кнопками
            for (int row = 0; row < rows; row++)
            {
                for (int col = 0; col < cols; col++)
                {
                    Button btn = new Button();
                    btn.Dock = DockStyle.Fill;
                    btn.Margin = new Padding(3);
                    btn.BackColor = Color.WhiteSmoke;
                    btn.Tag = new Point(row, col);
                    btn.Click += Cell_Click;

                    ScreenGame.Controls.Add(btn, col, row);
                    gameButtons[row, col] = btn;
                }
            }
        }

        /// <summary>
        /// Обработчик клика по ячейке
        /// </summary>
        private void Cell_Click(object sender, EventArgs e)
        {
            Button clickedButton = (Button)sender;
            Point position = (Point)clickedButton.Tag;
            int clickedColumn = position.Y;

            bool success = _game.PlaceDisc(clickedColumn);

            if (success)
            {
                UpdateGameBoardUI();

                if (_game.CheckWin())
                {
                    if (_game.CurrentPlayerSymbol == 'X')
                    {
                        MessageBox.Show($"Победил игрок 2 (O - Желтый)!");
                    }
                    else MessageBox.Show($"Победил игрок 1 (X - Красный)!");
                    foreach (Button btn in gameButtons) btn.Enabled = false;
                }
                else if (_game.IsBoardFull())
                {
                    MessageBox.Show("Ничья! Поле заполнено.");
                }
                else
                {
                    UpdateStatusLabel();
                }
            }
        }

        /// <summary>
        /// Обновления цветов кнопок
        /// </summary>
        private void UpdateGameBoardUI()
        {
            for (int row = 0; row < _game.Rows; row++)
            {
                for (int col = 0; col < _game.Cols; col++)
                {
                    char symbol = _game.GetCellSymbol(row, col);
                    if (symbol == 'X')
                    {
                        gameButtons[row, col].BackColor = Color.Red;
                    }
                    else if (symbol == 'O')
                    {
                        gameButtons[row, col].BackColor = Color.Yellow;
                    }
                    else
                    {
                        gameButtons[row, col].BackColor = Color.WhiteSmoke;
                    }
                }
            }
        }

        /// <summary>
        /// Обновляет Label статус
        /// </summary>
        private void UpdateStatusLabel()
        {
            StatusLabel.Text = _game.CurrentPlayer
                ? "Ход Игрока 1 (X - Красный)"
                : "Ход Игрока 2 (O - Желтый)";
        }

        /// <summary>
        /// Обработчик кнопки "Сброс игры"
        /// </summary>
        private void resetGameBtn_Click(object sender, EventArgs e)
        {
            _game.ResetGame();
            UpdateGameBoardUI();
            UpdateStatusLabel();

            foreach (Button btn in gameButtons) btn.Enabled = true;
        }


    }
}
