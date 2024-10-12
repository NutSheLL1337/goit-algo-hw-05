def binary_search(arr, target):
    """
    Функція для бінарного пошуку елемента в відсортованому масиві.

    Parameters:
    arr (list): Відсортований масив для пошуку.
    target: Елемент, який шукаємо.

    Returns:
    tuple: (кількість ітерацій, верхня межа або -1, якщо елемент не знайдено)
    """
    left = 0
    right = len(arr) - 1
    iterations = 0
    upper_bound = None  # Для зберігання найменшого елемента, більшого за target

    while left <= right:
        iterations += 1  # Підраховуємо кількість ітерацій
        mid = (left + right) // 2

        if arr[mid] == target:
            return (iterations, arr[mid])  # Повертаємо кількість ітерацій і знайдений елемент
        
        elif arr[mid] < target:
            left = mid + 1  # Пошук в правій половині
        else:
            upper_bound = arr[mid]  # Можливий кандидат на "верхню межу"
            right = mid - 1  # Пошук в лівій половині

    # Якщо не знайдено точний елемент, повертаємо кількість ітерацій і "верхню межу"
    return (iterations, upper_bound)

# Приклад використання
array = [0.4, 1.666, 8, 12, 16, 12, 38, 56, 72, 91] # Видаляємо 23
target = 23
result = binary_search(array, target)

if result[1] is not None:
    print(f"Кількість ітерацій: {result[0]}\nВерхня межа: {result[1]}")
else:
    print(f"Елемент не знайдено, кількість ітерацій: {result[0]}")
