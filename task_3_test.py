import numpy as np
import timeit
with open('стаття 1.txt', 'r', encoding='utf-8', errors='ignore') as file:
    text1 = file.read()

with open('стаття 2.txt', 'r', encoding='utf-8', errors='ignore') as file:
    text2 = file.read()


def bad_char_heuristic(pattern):
    bad_char = {}
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i
    # Повертаємо словник для шаблону
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
    steps = []

    while s <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            steps.append((s, f"Substring found at index {s}"))
            s += good_suffix[0]
        else:
            # Якщо символа немає в шаблоні, повертаємо значення -1
            bad_char_shift = bad_char.get(text[s + j], -1)
            if bad_char_shift == -1:
                bad_char_shift = j + 1
            else:
                bad_char_shift = j - bad_char_shift

            good_suffix_shift = good_suffix[j + 1]
            s += max(bad_char_shift, good_suffix_shift)

        steps.append((s, f"Index: {s}, Bad char: {bad_char_shift}, Good char: {good_suffix_shift}"))
    return steps



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


existing_substring = "jumpStep += (int)(Math.sqrt(arrayLength))"
non_existing_substring = "вигаданий підрядок"


time_boyer_moore_existing_1 = timeit.timeit(lambda: boyer_moore_search(text1, existing_substring), number=10)
time_boyer_moore_non_existing_1 = timeit.timeit(lambda: boyer_moore_search(text1, non_existing_substring), number=10)

time_kmp_existing_1 = timeit.timeit(lambda: kmp_search(text1, existing_substring), number=10)
time_kmp_non_existing_1 = timeit.timeit(lambda: kmp_search(text1, non_existing_substring), number=10)

time_rabin_karp_existing_1 = timeit.timeit(lambda: rabin_karp_search(text1, existing_substring), number=10)
time_rabin_karp_non_existing_1 = timeit.timeit(lambda: rabin_karp_search(text1, non_existing_substring), number=10)


time_boyer_moore_existing_2 = timeit.timeit(lambda: boyer_moore_search(text2, existing_substring), number=10)
time_boyer_moore_non_existing_2 = timeit.timeit(lambda: boyer_moore_search(text2, non_existing_substring), number=10)

time_kmp_existing_2 = timeit.timeit(lambda: kmp_search(text2, existing_substring), number=10)
time_kmp_non_existing_2 = timeit.timeit(lambda: kmp_search(text2, non_existing_substring), number=10)

time_rabin_karp_existing_2 = timeit.timeit(lambda: rabin_karp_search(text2, existing_substring), number=10)
time_rabin_karp_non_existing_2 = timeit.timeit(lambda: rabin_karp_search(text2, non_existing_substring), number=10)


import matplotlib.pyplot as plt
import numpy as np

labels = ['Boyer-Moore', 'KMP', 'Rabin-Karp']

existing_times_1 = [time_boyer_moore_existing_1, time_kmp_existing_1, time_rabin_karp_existing_1]
non_existing_times_1 = [time_boyer_moore_non_existing_1, time_kmp_non_existing_1, time_rabin_karp_non_existing_1]

existing_times_2 = [time_boyer_moore_existing_2, time_kmp_existing_2, time_rabin_karp_existing_2]
non_existing_times_2 = [time_boyer_moore_non_existing_2, time_kmp_non_existing_2, time_rabin_karp_non_existing_2]

x = np.arange(len(labels))
width = 0.2

fig, ax = plt.subplots(figsize=(14, 8))
rects1 = ax.bar(x - width, existing_times_1, width, label='Existing Substring (Article 1)')
rects2 = ax.bar(x, non_existing_times_1, width, label='Non-Existing Substring (Article 1)')
rects3 = ax.bar(x + width, existing_times_2, width, label='Existing Substring (Article 2)')
rects4 = ax.bar(x + 2 * width, non_existing_times_2, width, label='Non-Existing Substring (Article 2)')

ax.set_ylabel('Time (seconds)')
ax.set_title('Algorithm Performance Comparison')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()
plt.show()

