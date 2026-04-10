using System;
using System.Diagnostics;

/// <summary>
/// Класс для работы с массивами и их сортировки
/// </summary>
class ArrayProcessor
{
    private int _size;
    private int[] _array;

    /// <summary>
    /// Конструктор по умолчанию (размер массива = 10)
    /// </summary>
    public ArrayProcessor()
    {
        _size = 10;
        _array = CreateArray(_size);
    }

    /// <summary>
    /// Конструктор с параметром размера массива
    /// </summary>
    /// <param name="size">Размер массива</param>
    public ArrayProcessor(int size)
    {
        _size = size;
        _array = CreateArray(_size);
    }

    /// <summary>
    /// Свойство для получения размера массива
    /// </summary>
    public int Size
    {
        get { return _size; }
    }

    /// <summary>
    /// Свойство для получения копии массива
    /// </summary>
    public int[] Array
    {
        get { return CopyArray(_array); }
    }

    /// <summary>
    /// Запускает процесс сортировки массива
    /// </summary>
    public void SortArray()
    {
        int[] arrayCopy = CopyArray(_array);

        Console.WriteLine("Исходный массив:");
        PrintArray(_array);

        Stopwatch sw = new Stopwatch();

        // Сортировка пузырьком
        sw.Start();
        int[] bubble = BubbleSort(_array);
        sw.Stop();
        long bubbleTime = sw.ElapsedMilliseconds;

        // Сортировка Шелла
        sw.Restart();
        int[] shell = ShellSort(arrayCopy);
        sw.Stop();
        long shellTime = sw.ElapsedMilliseconds;

        Console.WriteLine("После сортировки пузырьком:");
        PrintArray(bubble);

        Console.WriteLine("После сортировки Шелла:");
        PrintArray(shell);

        Console.ForegroundColor = ConsoleColor.Green;
        Console.WriteLine($"Время сортировки пузырьком: {bubbleTime} мс");
        Console.WriteLine($"Время сортировки Шелла: {shellTime} мс");
        Console.ResetColor();
        Console.WriteLine("Нажмите любую клавишу для продолжения...");
        Console.ReadKey();
    }

    /// <summary>
    /// Создает массив случайных чисел
    /// </summary>
    /// <param name="size">Размер массива</param>
    /// <returns>Созданный массив</returns>
    private int[] CreateArray(int size)
    {
        Random random = new Random();
        int[] arr = new int[size];
        for (int i = 0; i < size; i++)
            arr[i] = random.Next(-100, 101);
        return arr;
    }

    /// <summary>
    /// Создает копию массива
    /// </summary>
    /// <param name="arr">Исходный массив</param>
    /// <returns>Копия массива</returns>
    private int[] CopyArray(int[] arr)
    {
        int[] copy = new int[arr.Length];
        System.Array.Copy(arr, copy, arr.Length);
        return copy;
    }

    /// <summary>
    /// Выводит массив на экран
    /// </summary>
    /// <param name="arr">Массив для вывода</param>
    private void PrintArray(int[] arr)
    {
        if (arr.Length > 10)
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("Массивы не могут быть выведены на экран, так как длина массива больше 10");
            Console.ResetColor();
            return;
        }

        foreach (var item in arr)
            Console.Write(item + " ");
        Console.WriteLine();
    }

    /// <summary>
    /// Сортирует массив методом пузырька
    /// </summary>
    /// <param name="arr">Исходный массив</param>
    /// <returns>Отсортированный массив</returns>
    private int[] BubbleSort(int[] arr)
    {
        int[] sorted = CopyArray(arr);
        for (int i = 0; i < sorted.Length - 1; i++)
            for (int j = 0; j < sorted.Length - i - 1; j++)
                if (sorted[j] > sorted[j + 1])
                    (sorted[j], sorted[j + 1]) = (sorted[j + 1], sorted[j]);
        return sorted;
    }

    /// <summary>
    /// Сортирует массив методом Шелла
    /// </summary>
    /// <param name="arr">Исходный массив</param>
    /// <returns>Отсортированный массив</returns>
    private int[] ShellSort(int[] arr)
    {
        int[] sorted = CopyArray(arr);
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
        return sorted;
    }
}