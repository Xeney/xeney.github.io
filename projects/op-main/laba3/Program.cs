using System;
using System.Diagnostics;

class Program
{
    static void Main()
    {
        bool exitProgram = false;
        
        while (!exitProgram)
        {
            Console.WriteLine("1. Отгадай ответ");
            Console.WriteLine("2. Об авторе");
            Console.WriteLine("3. Сортировка массива");
            Console.WriteLine("4. Выход");
            Console.Write("Выберите действие: ");
            
            string choice = Console.ReadLine();
            
            switch (choice)
            {
                case "1":
                    PlayGuessGame();
                    break;
                case "2":
                    ShowAuthorInfo();
                    break;
                case "3":
                    SortArray();
                    break;
                case "4":
                    exitProgram = ExitProgram();
                    break;
                default:
                    Console.WriteLine("Неверный выбор!");
                    break;
            }
        }
    }

    static void ShowAuthorInfo()
    {
        Console.WriteLine("ФИО: Варламов Дамир Алексеевич");
        Console.WriteLine("Группа: 6105-090301D");
        Console.WriteLine("Нажмите любую клавишу для продолжения...");
        Console.ReadKey();
    }

    static bool ExitProgram()
    {
        while (true)
        {
            Console.Write("Вы уверены, что хотите выйти? (д/н): ");
            string answer = Console.ReadLine().ToLower();
            
            if (answer == "д")
            {
                return true;
            }
            else if (answer == "н")
            {
                return false;
            }
            else
            {
                Console.WriteLine("Ошибка ввода!");
            }
        }
    }

    static void PlayGuessGame()
    {
        double a = GetValidDouble("Введите a: ");
        double b = GetValidDouble("Введите b: ");
        
        double correctAnswer = CalculateFunction(a, b);
        
        GuessNumber(correctAnswer);
        
        Console.WriteLine("Нажмите любую клавишу для продолжения...");
        Console.ReadKey();
    }

    static double CalculateFunction(double a, double b)
    {
        const double PI = Math.PI;
        double numerator = Math.Pow(Math.Cos(PI), 7) + Math.Sqrt(Math.Log(Math.Pow(b, 4)));
        double denominator = Math.Pow(Math.Sin(PI/2 + a), 2);
        return numerator / denominator;
    }

    static void GuessNumber(double correctAnswer)
    {
        double roundedAnswer = Math.Round(correctAnswer, 2);
        int attempts = 3;
        bool guessed = false;
        
        while (attempts > 0 && !guessed)
        {
            Console.WriteLine($"Осталось попыток: {attempts}");
            double userAnswer = GetValidDouble("Введите ваш ответ: ");
            double userRounded = Math.Round(userAnswer, 2);
            
            if (userRounded == roundedAnswer)
            {
                guessed = true;
                Console.WriteLine("Ответ верный!");
            }
            else
            {
                attempts--;
                if (attempts > 0)
                {
                    Console.WriteLine("Ответ неверный!");
                }
            }
        }
        
        if (!guessed)
        {
            Console.WriteLine($"Правильный ответ: {roundedAnswer:F2}");
        }
    }

    static void SortArray()
    {
        int size = GetArraySize();
        int[] array = CreateArray(size);
        int[] arrayCopy = CopyArray(array);
        
        Console.WriteLine("Исходный массив:");
        PrintArray(array);
        
        Stopwatch stopwatch = new Stopwatch();
        
        stopwatch.Start();
        int[] bubbleSorted = BubbleSort(array);
        stopwatch.Stop();
        long bubbleTime = stopwatch.ElapsedMilliseconds;
        
        stopwatch.Restart();
        int[] shellSorted = ShellSort(arrayCopy);
        stopwatch.Stop();
        long shellTime = stopwatch.ElapsedMilliseconds;
        
        Console.WriteLine("После сортировки пузырьком:");
        PrintArray(bubbleSorted);
        
        Console.WriteLine("После сортировки Шелла:");
        PrintArray(shellSorted);
        
        Console.WriteLine($"Время сортировки пузырьком: {bubbleTime} мс");
        Console.WriteLine($"Время сортировки Шелла: {shellTime} мс");
        
        Console.WriteLine("Нажмите любую клавишу для продолжения...");
        Console.ReadKey();
    }

    static int GetArraySize()
    {
        int size;
        while (true)
        {
            Console.Write("Введите размер массива: ");
            if (int.TryParse(Console.ReadLine(), out size) && size > 0)
            {
                return size;
            }
            Console.WriteLine("Ошибка! Размер должен быть положительным числом.");
        }
    }

    static int[] CreateArray(int size)
    {
        Random random = new Random();
        int[] array = new int[size];
        for (int i = 0; i < size; i++)
        {
            array[i] = random.Next(-100, 101);
        }
        return array;
    }

    static int[] CopyArray(int[] array)
    {
        int[] copy = new int[array.Length];
        Array.Copy(array, copy, array.Length);
        return copy;
    }

    static void PrintArray(int[] array)
    {
        if (array.Length > 10)
        {
            Console.WriteLine("Массивы не могут быть выведены на экран, так как длина массива больше 10");
            return;
        }
        
        for (int i = 0; i < array.Length; i++)
        {
            Console.Write(array[i] + " ");
        }
        Console.WriteLine();
    }

    static int[] BubbleSort(int[] array)
    {
        int[] sortedArray = CopyArray(array);
        
        for (int i = 0; i < sortedArray.Length - 1; i++)
        {
            for (int j = 0; j < sortedArray.Length - i - 1; j++)
            {
                if (sortedArray[j] > sortedArray[j + 1])
                {
                    int temp = sortedArray[j];
                    sortedArray[j] = sortedArray[j + 1];
                    sortedArray[j + 1] = temp;
                }
            }
        }
        
        return sortedArray;
    }

    static int[] ShellSort(int[] array)
    {
        int[] sortedArray = CopyArray(array);
        int n = sortedArray.Length;
        
        for (int gap = n / 2; gap > 0; gap /= 2)
        {
            for (int i = gap; i < n; i++)
            {
                int temp = sortedArray[i];
                int j;
                for (j = i; j >= gap && sortedArray[j - gap] > temp; j -= gap)
                {
                    sortedArray[j] = sortedArray[j - gap];
                }
                sortedArray[j] = temp;
            }
        }
        
        return sortedArray;
    }

    static double GetValidDouble(string prompt)
    {
        double value;
        while (true)
        {
            Console.Write(prompt);
            if (double.TryParse(Console.ReadLine(), out value))
            {
                return value;
            }
            Console.WriteLine("Ошибка ввода! Введите число:");
        }
    }
}