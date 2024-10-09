# Завдання 3
# Порівняти ефективність алгоритмів пошуку підрядка: Боєра-Мура, Кнута-Морріса-Пратта та Рабіна-Карпа на основі двох текстових файлів (стаття 1, стаття 2). 
# Використовуючи timeit, треба виміряти час виконання кожного алгоритму для двох видів підрядків: одного, що дійсно існує в тексті, та іншого — 
# вигаданого (вибір підрядків за вашим бажанням). На основі отриманих даних визначити найшвидший алгоритм для кожного тексту окремо та в цілому.

import timeit
import pandas as pd
import matplotlib.pyplot as plt

def knuth_morris_pratt(text, pattern):
    """
    Реалізація алгоритму Кнута-Морріса-Пратта для пошуку підрядка у тексті.
    
    Алгоритм використовує попередньо побудовану таблицю префіксів для прискорення пошуку.
    
    Параметри:
    text (str): Текст, в якому потрібно знайти підрядок.
    pattern (str): Підрядок, який потрібно знайти.
    
    Повертає:
    int: Індекс початку знайденого підрядка, або -1 якщо підрядок не знайдено.
    """
    def build_partial_match_table(pattern):
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    n = len(text)
    m = len(pattern)
    lps = build_partial_match_table(pattern)
    i = 0
    j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            return i - j  # Found pattern at index i - j
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1  # Pattern not found

def rabin_karp(text, pattern, q=101):
    """
    Реалізація алгоритму Рабіна-Карпа для пошуку підрядка у тексті.
    
    Алгоритм використовує хешування для порівняння підрядків та прискорення пошуку.
    
    Параметри:
    text (str): Текст, в якому потрібно знайти підрядок.
    pattern (str): Підрядок, який потрібно знайти.
    q (int): Просте число для запобігання переповнення (за замовчуванням 101).
    
    Повертає:
    int: Індекс початку знайденого підрядка, або -1 якщо підрядок не знайдено.
    """
    d = 256
    m = len(pattern)
    n = len(text)
    p = 0  # hash value for pattern
    t = 0  # hash value for text
    h = 1

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i  # Found pattern at index i

        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q

    return -1  # Pattern not found

def boyer_moore(text, pattern):
    """
    Реалізація алгоритму Боєра-Мура для пошуку підрядка у тексті.
    
    Алгоритм використовує таблицю поганих символів для пропуску частин тексту, що прискорює пошук.
    
    Параметри:
    text (str): Текст, в якому потрібно знайти підрядок.
    pattern (str): Підрядок, який потрібно знайти.
    
    Повертає:
    int: Індекс початку знайденого підрядка, або -1 якщо підрядок не знайдено.
    """
    def preprocess_bad_character(pattern):
        bad_char = {}
        for i in range(len(pattern)):
            bad_char[pattern[i]] = i
        return bad_char

    m = len(pattern)
    n = len(text)
    bad_char = preprocess_bad_character(pattern)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s  # Found pattern at index s
            s += (m - bad_char.get(text[s + m], -1) if s + m < n else 1)
        else:
            s += max(1, j - bad_char.get(text[s + j], -1))

    return -1  # Pattern not found

# Завантаження текстів з файлів
with open('стаття 1.txt', 'r', encoding='windows-1251') as f:
    text1 = f.read()

with open('стаття 2.txt', 'r', encoding='windows-1251') as f:
    text2 = f.read()

# Підрядки для пошуку
existing_substring = "алгоритм"
non_existing_substring = "вигаданийпідрядок"

# Вимірювання часу виконання алгоритмів для тексту 1
def measure_boyer_moore_text1():
    return boyer_moore(text1, existing_substring)

def measure_kmp_text1():
    return knuth_morris_pratt(text1, existing_substring)

def measure_rabin_karp_text1():
    return rabin_karp(text1, existing_substring)

# Для неіснуючого підрядка
def measure_boyer_moore_text1_non():
    return boyer_moore(text1, non_existing_substring)

def measure_kmp_text1_non():
    return knuth_morris_pratt(text1, non_existing_substring)

def measure_rabin_karp_text1_non():
    return rabin_karp(text1, non_existing_substring)

# Вимірювання часу для тексту 2
def measure_boyer_moore_text2():
    return boyer_moore(text2, existing_substring)

def measure_kmp_text2():
    return knuth_morris_pratt(text2, existing_substring)

def measure_rabin_karp_text2():
    return rabin_karp(text2, existing_substring)

# Для неіснуючого підрядка
def measure_boyer_moore_text2_non():
    return boyer_moore(text2, non_existing_substring)

def measure_kmp_text2_non():
    return knuth_morris_pratt(text2, non_existing_substring)

def measure_rabin_karp_text2_non():
    return rabin_karp(text2, non_existing_substring)

# Використовуємо timeit для вимірювання часу виконання
results = []

print("Текст 1 (існуючий підрядок):")
boyer_moore_time_text1 = timeit.timeit(measure_boyer_moore_text1, number=10)
kmp_time_text1 = timeit.timeit(measure_kmp_text1, number=10)
rabin_karp_time_text1 = timeit.timeit(measure_rabin_karp_text1, number=10)
results.append(("text1_existing", "Boyer-Moore", boyer_moore_time_text1))
results.append(("text1_existing", "KMP", kmp_time_text1))
results.append(("text1_existing", "Rabin-Karp", rabin_karp_time_text1))

print("Текст 1 (неіснуючий підрядок):")
boyer_moore_time_text1_non = timeit.timeit(measure_boyer_moore_text1_non, number=10)
kmp_time_text1_non = timeit.timeit(measure_kmp_text1_non, number=10)
rabin_karp_time_text1_non = timeit.timeit(measure_rabin_karp_text1_non, number=10)
results.append(("text1_non_existing", "Boyer-Moore", boyer_moore_time_text1_non))
results.append(("text1_non_existing", "KMP", kmp_time_text1_non))
results.append(("text1_non_existing", "Rabin-Karp", rabin_karp_time_text1_non))

print("Текст 2 (існуючий підрядок):")
boyer_moore_time_text2 = timeit.timeit(measure_boyer_moore_text2, number=10)
kmp_time_text2 = timeit.timeit(measure_kmp_text2, number=10)
rabin_karp_time_text2 = timeit.timeit(measure_rabin_karp_text2, number=10)
results.append(("text2_existing", "Boyer-Moore", boyer_moore_time_text2))
results.append(("text2_existing", "KMP", kmp_time_text2))
results.append(("text2_existing", "Rabin-Karp", rabin_karp_time_text2))

print("Текст 2 (неіснуючий підрядок):")
boyer_moore_time_text2_non = timeit.timeit(measure_boyer_moore_text2_non, number=10)
kmp_time_text2_non = timeit.timeit(measure_kmp_text2_non, number=10)
rabin_karp_time_text2_non = timeit.timeit(measure_rabin_karp_text2_non, number=10)
results.append(("text2_non_existing", "Boyer-Moore", boyer_moore_time_text2_non))
results.append(("text2_non_existing", "KMP", kmp_time_text2_non))
results.append(("text2_non_existing", "Rabin-Karp", rabin_karp_time_text2_non))

# Створюємо DataFrame для результатів
columns = ["Текст", "Алгоритм", "Час виконання (сек)"]
df_results = pd.DataFrame(results, columns=columns)

# Виводимо результати у вигляді таблиці
print(df_results)

# Побудова графіків
plt.figure(figsize=(14, 8))
for text_type in df_results["Текст"].unique():
    subset = df_results[df_results["Текст"] == text_type]
    plt.plot(subset["Алгоритм"], subset["Час виконання (сек)"], marker='o', label=text_type)

plt.title("Порівняння часу виконання алгоритмів пошуку підрядка")
plt.xlabel("Алгоритм")
plt.ylabel("Час виконання (сек)")
plt.legend(title="Тип підрядка")
plt.grid(True)
plt.show()

# Визначення найшвидшого алгоритму в цілому
total_times = {"Boyer-Moore": 0, "KMP": 0, "Rabin-Karp": 0}
for _, alg, time in results:
    total_times[alg] += time

overall_fastest = min(total_times, key=total_times.get)
print(f"\nНайшвидший алгоритм в цілому: {overall_fastest} з загальним часом {total_times[overall_fastest]}")