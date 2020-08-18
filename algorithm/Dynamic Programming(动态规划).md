---
tags: [Algorithm]
title: Dynamic Programming(动态规划)
created: '2020-02-24T02:45:14.847Z'
modified: '2020-02-24T05:23:09.667Z'
---

# Dynamic Programming(动态规划)

### 动态规划解题四部曲
- 判断是否可用递归方式解题
  - 先定义一个函数，明确这个函数的功能
  - 寻找问题与子问题之间的关系（递推公式）
  - 将第二步的递推公式套用到第一步定义的函数中
  - 根据问题与子问题的关系，推导时间复杂度，并进行后续优化
  - > **青蛙跳台阶**  
    > 解释：一只青蛙可以一次跳一级台阶或者一次跳2级台阶，求上N级台阶有多少种跳法。
    > 1. 定义一个函数，代表跳上n级台阶的方法
    > ```Python
    >  def f(n: int):
    >    pass
    >  ```
    > 2. 寻找问题与子问题之间的关系：
    > 跳上n级台阶可以转化为从n-1级跳上n级，和从n-2级跳上n级，即跳上n-1和n-2的方法：
    > f(n) = f(n-1) + f(n-2), 还有第一次的两种跳法 1 n=1, 2 n=2
    > 3. 将第二步得分关系套用到第一步定义的函数中
    > ```
    > def f(n: int):
    >   if n == 1: return 1
    >   if n == 2: return 2
    >   return f(n-1) + f(n-2)    
    > ```
    > 4. 计算时间复杂度并优化
    > 详细的计算涉及到高等代数知识，直接上结果：ƒ(n) = 1/√5[((1+√5)/2)ˆn - ((1-√5)/2)ˆn]
    > 由公式可知，时间复杂度是指数级别，所以结果并不能接受，接下来优化：
    > 设定n=6，公式可以转化为f(6) = f(4) + f(5),f(4) = f(2) + f(3), f(5) = f(4) + f(3)...
    > 由公式可以看到，递推计算中，存在着大量的重复计算，我们可以在一个hash列表中将结果保存，
    > 每次在进行计算时，就查询一遍hash列表，这样可以减少不必要的计算，即新的函数为：
    > ```Python
    > def f(n: int):
    >   if n == 1: return 1
    >   if n == 2: return 2
    >   if map.get(n):
    >     return map.get(n)
    >   return f(n-1) + f(n-2) 
    > ```
    > 改造过后，发现现在的时间复杂度，已经下降到O(n)， 然后用到了一个hash表来存储中间结果，
    > 所以空间复杂度为O(n)
    > 到这里基本这个问题就可以算是解决了，但是如果细究，发现还是可以再一步的降低空间复杂度，
    > 我们把之前n=6的公式如果继续分解，就可以发现，我们只需要知道f(1)-f(4)就可以计算出值了，
    > 而f(1) = 1, f(2) = 2，f(3)之后的值都是通过1和2计算出来的，所以改造后的函数为：
    > ```Python
    > def f(n: int):
    >   if n == 1: return 1
    >   if n == 2: return 2
    >   result = 0
    >   pre = 1
    >   next = 2
    >   for idx in range(3, n+1):
    >     result = pre + next
    >     pre = next
    >     next = result
    >   return result 
    > ```
    > 改造后的时间复杂度还是O(n), 而空间复杂度则为O(1)。
- 分析在递归的过程中是否存在大量的重叠子问题
- 采用备忘录的方式来存子问题的解，以避免大量的重复计算（剪枝）
- 改用自底向上的方式来递推，即动态规划

### 案例分析
> 给定不同面额的硬币 coins 和一个总金额 amount。编写一个函数来计算可以凑成总金额所需的最少的硬币个数。
如果没有任何一种硬币组合能组成总金额，返回 -1。
输入: coins = [1, 2, 5], amount = 11，输出: 3  解释: 11 = 5 + 5 + 1 
输入: coins = [2], amount = 3，输出: -1

来套用一下我们的动态规划解题四步曲

一、判断是否可用递归来解
对于 amount 来说，如果我们选择了 coins 中的任何一枚硬币，则问题的规模(amount)是不是缩小了,再对缩小的 amount 也选择 coins 中的任何一枚硬币,直到再也不能选择（amount <= 0, amount = 0 代表有符合条件的解，小于0代表没有符合条件的解），从描述中我们可以看出问题可以分解成子问题，子问题与原问题具有相同的解决问题的思路，同时也有临界条件，符合递归的条件，由此可证可以用递归求解，接下来我们来看看，如何套用递归四步曲来解题
1、定义这个函数，明确这个函数的功能,函数的功能显然是给定一个 amount，用定义好的 coins 来凑，于是我们定义函数如下
```Python
def f(amount: int, coins: list):
  pass
```
2、寻找问题与子问题的关系，即递推公式 这题的递推关系比较难推导，我们一起看下，假设 f(amount, coins) 为零钱 amount 的所需要的最少硬币数，当选中了coins 中的第一枚硬币之后（即为 coins[0]），则需再对剩余的 amount - coins[0] 金额求最少硬币数，即调用 f(amount - coins[0], coins)  ,由此可知当选了第一枚硬币后的递推公式如下
```Shell
f(amount, coins) = f(amount-coins[0]) + 1 (这里的 1 代表选择了第一枚硬币)
如果选择了第二，第三枚呢，递推公式如下

f(amount, coins) = f(amount-coins[1]) + 1 (这里的 1 代表选择了第二枚硬币)
f(amount, coins) = f(amount-coins[2]) + 1 (这里的 1 代表选择了第三枚硬币)
我们的目标是求得所有以上 f(amount, coins) 解的的最小值，于是可以得到我们的总的递推公式如下

f(amount, coins) = min{ f(amount - coins[i]) + 1) }, 其中 i 的取值为 0 到 coins 的大小，coins[i] 表示选择了此硬币, 1 表示选择了coins[i]  这一枚硬币
```
3、将第二步的递推公式用代码表示出来补充到步骤 1 定义的函数中

得出了递推公式用代码实现就简单了，来简单看一下

```Python
def exchange(amount: int, coins: list):
  if amount == 0: return 0
  if amount < 0: return -1
  result = 2 ** 31;
  for idx in range(0, len(coins)):
    submin = exchange(amount - coins[idx], coins)
    if submin == -1: continue
    result = min(submin + 1, result)
  if result == 0: return -1
  return result

if __name__ == "__main__":
  print(exchange(11, [1, 2, 5])) # result: 3
```

4、计算时间复杂度 这道题的时间复杂度很难看出来，一般看不出来的时候我们可以画递归树来分析，针对 amount = 11 的递归树 如下
```Shell
          11
   /       |    \
  10       9*    6
 / | \    / | \    
9* 8* 5  8* 7  4  
```
前文我们说到斐波那契的递归树是一颗二叉树，时间复杂度是指数级别，而凑零钱的递归树是一颗三叉树 ，显然时间复杂度也是指数级别!

二、分析在递归的过程中是否存在大量的重叠子问题（动态规划第二步）

由上一节的递归树可知，存在重叠子问题，上一节中的 9， 8，都重复算了,所以存在重叠子问题！

三、采用备忘录的方式来存子问题的解以避免大量的重复计算（剪枝）

既然我们知道存在重叠子问题，那么就可以用备忘录来存储中间结果达到剪枝的目的
```Python
class Solution:
    def __init__(self):
        self.map = {}
    def exchangeRecursive(self, amount: int, coins: list):
        if self.map.get(amount, None) != None:
            return self.map.get(amount)
        if amount == 0: return 0
        if amount < 0: return -1
        result = 2 ** 31
        for idx in range(0, len(coins)):
            submin = self.exchangeRecursive(amount - coins[idx], coins)
            if submin == -1: continue
            result = min(submin + 1, result)
        if result == 2 ** 31:
            return -1
        self.map[amount] = result
        return result

if __name__ == "__main__":
    st = Solution()
    print(st.exchangeRecursive(11, [1, 2, 5]))
```

四、改用自底向上的方式来递推，即动态规划

前面我们推导出了如下递归公式
```Shell
f(amount, coins) = min{ f(amount - coins[i]) + 1) }, 其中 i 的取值为 0 到 coins 的大小，coins[i] 表示选择了此硬币, 1 表示选择了coins[i]  这一枚硬币
```
从以上的递推公式中我们可以获取 DP 的解题思路，我们定义 DP(i) 为凑够零钱 i 需要的最小值，状态转移方程如下
```Shell
DP[i] =  min{ DP[ i - coins[j] ] + 1 } = min{ DP[ i - coins[j] ]} + 1,  其中 j 的取值为 0 到 coins 的大小，i 代表取了 coins[j] 这一枚硬币。
```
于是我们只要自底向上根据以上状态转移方程依次求解 DP[1], DP[2],DP[3].,....DP[11]，最终的 DP[11]，即为我们所求的解
```Python
# 动态规划求解
def exchangeDP(amount: int, coins: list):
  dp = []
  for idx in range(0, amount+1):
    dp.append(amount + 1)
  dp[0] = 0
  for idx in range(0, amount+1):
    for idy in range(0, len(coins)):
      if idx >= coins[idy]:
        dp[idx] = min(dp[idx-coins[idy]], dp[idx]) + 1
  if dp[amount] == amount + 1:
    return -1
  
  return dp[amount]

```

