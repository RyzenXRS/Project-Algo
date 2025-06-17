# knapsack.py
import quick_sort
from quick_sort import quick_sort

def knapsack_rating(budget, books):
    sorted_books = quick_sort(books, key='rating', descending=True)

    n = len(sorted_books)
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        harga = int(sorted_books[i - 1]['harga'])
        nilai = float(sorted_books[i - 1].get('rating', 0))
        for w in range(budget + 1):
            if harga <= w:
                dp[i][w] = max(nilai + dp[i - 1][w - harga], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    w = budget
    selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(sorted_books[i - 1])
            w -= int(sorted_books[i - 1]['harga'])

    return selected
