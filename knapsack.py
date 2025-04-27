def knapsack(weights, values, W):
    n = len(weights)
    dp = [0 for _ in range(W+1)]
    for i in range(n):
        for w in range(W, weights[i] -1, -1):
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
        
        return dp[W]

print(knapsack([1, 2, 3], [10, 15, 40], 6)) # Output: 55