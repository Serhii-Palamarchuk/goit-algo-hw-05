# Завдання 2
# Реалізувати двійковий пошук для відсортованого масиву з дробовими числами. 
# Написана функція для двійкового пошуку повинна повертати кортеж, де першим елементом є кількість ітерацій, потрібних для знаходження елемента. 
# Другим елементом має бути "верхня межа" — це найменший елемент, який є більшим або рівним заданому значенню.

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        if arr[mid] == target:
            return (iterations, arr[mid])
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            upper_bound = arr[mid]

    if upper_bound is None and left < len(arr):
        upper_bound = arr[left]

    return (iterations, upper_bound)

# Тестуємо двійковий пошук
sorted_array = [1.2, 2.3, 3.5, 4.8, 5.9, 7.1, 8.4]
target_value = 4.0
print(binary_search(sorted_array, target_value))  # Виведе: (кількість ітерацій, верхня межа)