using System;

namespace Laba6
{
    /// <summary>
    /// Статический класс для логики игры "Отгадай ответ"
    /// </summary>
    public static class GameLogic
    {
        /// <summary>
        /// Вычисляет значение функции по заданным параметрам
        /// </summary>
        /// <param name="a">Первый параметр функции</param>
        /// <param name="b">Второй параметр функции</param>
        /// <returns>Результат вычисления функции, округленный до 2 знаков</returns>
        public static double CalculateFunction(double a, double b)
        {
            const double PI = Math.PI;
            double numerator = Math.Pow(Math.Cos(PI), 7) + Math.Sqrt(Math.Log(Math.Pow(b, 4)));
            double denominator = Math.Pow(Math.Sin(PI / 2 + a), 2);
            return Math.Round(numerator / denominator, 2);
        }

        /// <summary>
        /// Проверяет правильность ответа пользователя
        /// </summary>
        /// <param name="userAnswer">Ответ пользователя</param>
        /// <param name="correctAnswer">Правильный ответ</param>
        /// <returns>True если ответ верный, иначе False</returns>
        public static bool CheckAnswer(double userAnswer, double correctAnswer)
        {
            double userRounded = Math.Round(userAnswer, 2);
            double correctRounded = Math.Round(correctAnswer, 2);
            return userRounded == correctRounded;
        }

        /// <summary>
        /// Валидирует и преобразует строку в целое число
        /// </summary>
        /// <param name="input">Входная строка</param>
        /// <param name="fieldName">Название поля для сообщения об ошибке</param>
        /// <returns>Валидное целое число</returns>
        /// <exception cref="ArgumentException">Выбрасывается при невалидном вводе</exception>
        public static int GetValidInt(string input, string fieldName)
        {
            if (int.TryParse(input, out int result) && result > 0)
                return result;

            throw new ArgumentException($"Некорректное значение для {fieldName}. Введите положительное число.");
        }

        /// <summary>
        /// Валидирует и преобразует строку в число с плавающей точкой
        /// </summary>
        /// <param name="input">Входная строка</param>
        /// <param name="fieldName">Название поля для сообщения об ошибке</param>
        /// <returns>Валидное число с плавающей точкой</returns>
        /// <exception cref="ArgumentException">Выбрасывается при невалидном вводе</exception>
        public static double GetValidDouble(string input, string fieldName)
        {
            if (double.TryParse(input, out double result))
                return result;

            throw new ArgumentException($"Некорректное значение для {fieldName}. Введите число.");
        }
    }
}