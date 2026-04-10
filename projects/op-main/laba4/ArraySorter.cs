using System;
using System.Diagnostics;

static class ArraySorter
{
    public static void SortArray()
    {
        int size = InputHelper.GetArraySize();
        int[] array = CreateArray(size);
        int[] arrayCopy = CopyArray(array);

        Console.WriteLine("Исходный массив:");
        PrintArray(array);

        Stopwatch sw = new Stopwatch();

        // Сортировка пузырьком
        sw.Start();
        int[] bubble = BubbleSort(array);
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

    private static int[] CreateArray(int size)
    {
        Random random = new Random();
        int[] arr = new int[size];
        for (int i = 0; i < size; i++)
            arr[i] = random.Next(-100, 101);
        return arr;
    }

    private static int[] CopyArray(int[] arr)
    {
        int[] copy = new int[arr.Length];
        Array.Copy(arr, copy, arr.Length);
        return copy;
    }

    private static void PrintArray(int[] arr)
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

    private static int[] BubbleSort(int[] arr)
    {
        int[] sorted = CopyArray(arr);
        for (int i = 0; i < sorted.Length - 1; i++)
            for (int j = 0; j < sorted.Length - i - 1; j++)
                if (sorted[j] > sorted[j + 1])
                    (sorted[j], sorted[j + 1]) = (sorted[j + 1], sorted[j]);
        return sorted;
    }

    private static int[] ShellSort(int[] arr)
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
