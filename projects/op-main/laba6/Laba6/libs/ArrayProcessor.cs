using System;
using System.Diagnostics;

namespace Laba6
{
    /// <summary>
    /// Класс для работы с одномерными массивами и их сортировки
    /// </summary>
    public class ArrayProcessor
    {
        private int[] _array;

        /// <summary>
        /// Получает копию массива
        /// </summary>
        public int[] Array => (int[])_array.Clone();

        /// <summary>
        /// Получает размер массива
        /// </summary>
        public int Size => _array.Length;

        /// <summary>
        /// Конструктор по умолчанию (размер массива = 10)
        /// </summary>
        public ArrayProcessor()
        {
            _array = new int[10];
            GenerateRandomArray();
        }

        /// <summary>
        /// Конструктор с параметром размера массива
        /// </summary>
        /// <param name="size">Размер создаваемого массива</param>
        /// <exception cref="ArgumentException">Выбрасывается при невалидном размере</exception>
        public ArrayProcessor(int size)
        {
            if (size <= 0)
                throw new ArgumentException("Размер массива должен быть положительным числом");

            _array = new int[size];
            GenerateRandomArray();
        }

        /// <summary>
        /// Заполняет массив случайными числами от -100 до 100
        /// </summary>
        public void GenerateRandomArray()
        {
            Random random = new Random();
            for (int i = 0; i < _array.Length; i++)
                _array[i] = random.Next(-100, 101);
        }

        /// <summary>
        /// Обновляет значение элемента массива по указанному индексу
        /// </summary>
        /// <param name="index">Индекс элемента</param>
        /// <param name="value">Новое значение</param>
        /// <exception cref="IndexOutOfRangeException">Выбрасывается при невалидном индексе</exception>
        public void UpdateValue(int index, int value)
        {
            if (index < 0 || index >= _array.Length)
                throw new IndexOutOfRangeException("Индекс вне диапазона массива");

            _array[index] = value;
        }

        /// <summary>
        /// Находит минимальное значение в массиве
        /// </summary>
        /// <returns>Минимальное значение массива</returns>
        public int FindMin()
        {
            if (_array.Length == 0) return 0;

            int min = _array[0];
            for (int i = 1; i < _array.Length; i++)
                if (_array[i] < min) min = _array[i];
            return min;
        }

        /// <summary>
        /// Находит максимальное значение в массиве
        /// </summary>
        /// <returns>Максимальное значение массива</returns>
        public int FindMax()
        {
            if (_array.Length == 0) return 0;

            int max = _array[0];
            for (int i = 1; i < _array.Length; i++)
                if (_array[i] > max) max = _array[i];
            return max;
        }

        /// <summary>
        /// Находит индекс минимального значения в массиве
        /// </summary>
        /// <returns>Индекс минимального элемента</returns>
        public int FindMinIndex()
        {
            if (_array.Length == 0) return -1;

            int minIndex = 0;
            for (int i = 1; i < _array.Length; i++)
                if (_array[i] < _array[minIndex]) minIndex = i;
            return minIndex;
        }

        /// <summary>
        /// Находит индекс максимального значения в массиве
        /// </summary>
        /// <returns>Индекс максимального элемента</returns>
        public int FindMaxIndex()
        {
            if (_array.Length == 0) return -1;

            int maxIndex = 0;
            for (int i = 1; i < _array.Length; i++)
                if (_array[i] > _array[maxIndex]) maxIndex = i;
            return maxIndex;
        }

        /// <summary>
        /// Вычисляет среднее арифметическое значений массива
        /// </summary>
        /// <returns>Среднее арифметическое</returns>
        public double CalculateAverage()
        {
            if (_array.Length == 0) return 0;

            double sum = 0;
            foreach (int num in _array) sum += num;
            return sum / _array.Length;
        }

        /// <summary>
        /// Сортирует массив методом пузырька
        /// </summary>
        /// <returns>Кортеж: отсортированный массив и время выполнения в миллисекундах</returns>
        public (int[] sortedArray, long timeMs) BubbleSort()
        {
            int[] sorted = (int[])_array.Clone();
            Stopwatch sw = Stopwatch.StartNew();

            for (int i = 0; i < sorted.Length - 1; i++)
                for (int j = 0; j < sorted.Length - i - 1; j++)
                    if (sorted[j] > sorted[j + 1])
                        (sorted[j], sorted[j + 1]) = (sorted[j + 1], sorted[j]);

            sw.Stop();
            return (sorted, sw.ElapsedMilliseconds);
        }

        /// <summary>
        /// Сортирует массив методом Шелла
        /// </summary>
        /// <returns>Кортеж: отсортированный массив и время выполнения в миллисекундах</returns>
        public (int[] sortedArray, long timeMs) ShellSort()
        {
            int[] sorted = (int[])_array.Clone();
            Stopwatch sw = Stopwatch.StartNew();

            int n = sorted.Length;
            for (int gap = n / 2; gap > 0; gap /= 2)
            {
                for (int i = gap; i < n; i++)
                {
                    int temp = sorted[i];
                    int j;
                    for (j = i; j >= gap && sorted[j - gap] > temp; j -= gap)
                        sorted[j] = sorted[j - gap];
                    sorted[j] = temp;
                }
            }

            sw.Stop();
            return (sorted, sw.ElapsedMilliseconds);
        }
    }
}