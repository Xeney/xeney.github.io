using System;

class Program
{
    static void Main()
    {
        // Объявление констант
        const double PI = Math.PI;
        
        // Ввод данных
        Console.WriteLine("Введите значение a (в радианах):");
        double a = double.Parse(Console.ReadLine());
        
        Console.WriteLine("Введите значение b (b > 0):");
        double b = double.Parse(Console.ReadLine());
        
        // Математические вычисления
        // Вычисляем числитель: cos^7(π) + √(ln(b^4))
        double numerator = Math.Pow(Math.Cos(PI), 7) + Math.Sqrt(Math.Log(Math.Pow(b, 4)));
        
        // Вычисляем знаменатель: sin(π/2 + a)^2
        double denominator = Math.Pow(Math.Sin(PI/2 + a), 2);
        
        // Вычисляем результат
        double f = numerator / denominator;
        
        // Вывод результатов
        Console.WriteLine($"\nРезультаты вычислений:");
        Console.WriteLine($"a = {a:F2}");
        Console.WriteLine($"b = {b:F2}");
        Console.WriteLine($"cos^7(π) = {Math.Pow(Math.Cos(PI), 7):F2}");
        Console.WriteLine($"√(ln(b^4)) = {Math.Sqrt(Math.Log(Math.Pow(b, 4))):F2}");
        Console.WriteLine($"sin(π/2 + a)^2 = {Math.Pow(Math.Sin(PI/2 + a), 2):F2}");
        Console.WriteLine($"f = {f:F2}");
        
        // Ожидание нажатия клавиши
        Console.WriteLine("\nНажмите любую клавишу для выхода...");
        Console.ReadKey();
    }
}