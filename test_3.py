import timeit

# Читання текстів з файлів
with open('стаття 1.txt', 'r', encoding='utf-8', errors='ignore') as file:
    text1 = file.read()

with open('стаття 2.txt', 'r', encoding='utf-8', errors='ignore') as file:
    text2 = file.read()


# Алгоритми пошуку

def bad_char_heuristic(pattern):
    bad_char = {}
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i
    return bad_char

def good_suffix_heuristic(pattern):
    m = len(pattern)
    good_suffix = [0] * (m + 1)
    border_pos = [-1] * (m + 1)
    i = m
    j = m + 1
    border_pos[i] = j

    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if good_suffix[j] == 0:
                good_suffix[j] = j - i
            j = border_pos[j]
        i -= 1
        j -= 1
        border_pos[i] = j

    j = border_pos[0]
    for i in range(m + 1):
        if good_suffix[i] == 0:
            good_suffix[i] = j
        if i == j:
            j = border_pos[j]

    return good_suffix

def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)

    bad_char = bad_char_heuristic(pattern)
    good_suffix = good_suffix_heuristic(pattern)

    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            return s
            s += good_suffix[0]
        else:
            bad_char_shift = bad_char.get(text[s + j], -1)
            if bad_char_shift == -1:
                bad_char_shift = j + 1
            else:
                bad_char_shift = j - bad_char_shift

            good_suffix_shift = good_suffix[j + 1]
            s += max(bad_char_shift, good_suffix_shift)
    return -1

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
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

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1

def rabin_karp_search(text, pattern, prime=101):
    m = len(pattern)
    n = len(text)
    d = 256
    h = 1
    p = 0
    t = 0

    for i in range(m-1):
        h = (h * d) % prime

    for i in range(m):
        p = (d * p + ord(pattern[i])) % prime
        t = (d * t + ord(text[i])) % prime

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % prime
            if t < 0:
                t = t + prime

    return -1


# Вибір підрядків
existing_substring = "jumpStep += (int)(Math.sqrt(arrayLength))"
non_existing_substring = "вигаданий підрядок"

# Вимірювання часу для статті 1
time_boyer_moore_existing_1 = timeit.timeit(lambda: boyer_moore_search(text1, existing_substring), number=10)
time_boyer_moore_non_existing_1 = timeit.timeit(lambda: boyer_moore_search(text1, non_existing_substring), number=10)

time_kmp_existing_1 = timeit.timeit(lambda: kmp_search(text1, existing_substring), number=10)
time_kmp_non_existing_1 = timeit.timeit(lambda: kmp_search(text1, non_existing_substring), number=10)

time_rabin_karp_existing_1 = timeit.timeit(lambda: rabin_karp_search(text1, existing_substring), number=10)
time_rabin_karp_non_existing_1 = timeit.timeit(lambda: rabin_karp_search(text1, non_existing_substring), number=10)

# Вимірювання часу для статті 2
time_boyer_moore_existing_2 = timeit.timeit(lambda: boyer_moore_search(text2, existing_substring), number=10)
time_boyer_moore_non_existing_2 = timeit.timeit(lambda: boyer_moore_search(text2, non_existing_substring), number=10)

time_kmp_existing_2 = timeit.timeit(lambda: kmp_search(text2, existing_substring), number=10)
time_kmp_non_existing_2 = timeit.timeit(lambda: kmp_search(text2, non_existing_substring), number=10)

time_rabin_karp_existing_2 = timeit.timeit(lambda: rabin_karp_search(text2, existing_substring), number=10)
time_rabin_karp_non_existing_2 = timeit.timeit(lambda: rabin_karp_search(text2, non_existing_substring), number=10)

# Виведення результатів в консоль
print("\n=== Час виконання для статті 1 ===")
print(f"Boyer-Moore (існуючий підрядок): {time_boyer_moore_existing_1:.6f} секунд")
print(f"Boyer-Moore (неіснуючий підрядок): {time_boyer_moore_non_existing_1:.6f} секунд")
print(f"KMP (існуючий підрядок): {time_kmp_existing_1:.6f} секунд")
print(f"KMP (неіснуючий підрядок): {time_kmp_non_existing_1:.6f} секунд")
print(f"Rabin-Karp (існуючий підрядок): {time_rabin_karp_existing_1:.6f} секунд")
print(f"Rabin-Karp (неіснуючий підрядок): {time_rabin_karp_non_existing_1:.6f} секунд")

print("\n=== Час виконання для статті 2 ===")
print(f"Boyer-Moore (існуючий підрядок): {time_boyer_moore_existing_2:.6f} секунд")
print(f"Boyer-Moore (неіснуючий підрядок): {time_boyer_moore_non_existing_2:.6f} секунд")
print(f"KMP (існуючий підрядок): {time_kmp_existing_2:.6f} секунд")
print(f"KMP (неіснуючий підрядок): {time_kmp_non_existing_2:.6f} секунд")
print(f"Rabin-Karp (існуючий підрядок): {time_rabin_karp_existing_2:.6f} секунд")
print(f"Rabin-Karp (неіснуючий підрядок): {time_rabin_karp_non_existing_2:.6f} секунд")
