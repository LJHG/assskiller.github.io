---
title: 和可被 K 整除的子数组---LeetCode974(我数学不太好)
date: 2020-05-27 15:47:56
tags: [前缀和, 哈希优化]
---
## 题目描述：  
给定一个整数数组 A，返回其中元素之和可被 K 整除的（连续、非空）子数组的数目。

## 示例：   
```cpp
示例：
输入：A = [4,5,0,-2,-3,1], K = 5
输出：7
解释：
有 7 个子数组满足其元素之和可被 K = 5 整除：
[4, 5, 0, -2, -3, 1], [5], [5, 0], [5, 0, -2, -3], [0], [0, -2, -3], [-2, -3]
 
提示：
1 <= A.length <= 30000
-10000 <= A[i] <= 10000
2 <= K <= 10000
```
<!-- more -->


## 解题思路:  
一看到子数组就知道是老前缀和了。然后直接写一发最朴素的前缀和超时了，看来是要哈希优化一下了。   
### 数学不好的做法
既然采用了哈希优化，那么就要稍微对公式进行一下变换了。  
目标为： **(prefix[i]-prefix[j-1]) % k = 0** 
稍微变化一下变为: **prefix[j-1] = prefix[i]-nk**  
可以看到，这种变换不好，因为出现了n，所以不能直接定位到哈希表中的某一个数据，那就只有遍历了(那我还用哈希表干嘛) 
```cpp
class Solution {
public:
    int subarraysDivByK(vector<int>& A, int K) {
       map<int,int> m;//m[i]表示前缀和为i的个数
       int length = A.size();
       int ans = 0;
       int curSum = 0;
       m[0] =1;
       for(int i=0;i<length;i++)
       {
            curSum += A[i];
            //只有遍历Map了吧
            for(auto& x:m)
            {
                if((curSum-x.first) % K == 0) ans+=x.second;
                //cout<<x.first<<" "<<x.second<<endl;
            }
            m[curSum]++;
       }
       return ans;
    }
};

```

</br>

### 多推导一下的做法
但是其实如果数学稍微好点，会发现：  
**(prefix[i]-prefix[j-1]) % k = 0**  可以推导为  
**prefix[i]%k = prefix[j-1]%k**  
这个式子可以给我们一个思路，就是hashmap里面都存mod k 过后的结果。 
同时要注意c++的mod可能会为一个负数，所以需要做一下处理，把  **curSum%k**  变为  **(curSum%k+k)%k**
```cpp
class Solution {
public:
    int subarraysDivByK(vector<int>& A, int K) {
       map<int,int> m;//m[i]表示前缀和为i的个数
       int length = A.size();
       int ans = 0;
       int curSum = 0;
       m[0] =1;
       for(int i=0;i<length;i++)
       {
            curSum += A[i];
            ans += m[(curSum%K+K)%K];
            m[(curSum%K+K)%K]++;
       }
       return ans;
    }
};
```


## 题目链接：  
https://leetcode-cn.com/problems/subarray-sums-divisible-by-k/