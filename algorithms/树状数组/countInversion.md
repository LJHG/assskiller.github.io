---
title: 逆序对
date: 2020-04-24 20:30:04
tags: [树状数组, bit, 归并排序, MergeSort, 逆序对, 二分查找, 离散化]
---
### 题目描述：  
在数组中的两个数字，如果前面一个数字大于后面的数字，则这两个数字组成一个逆序对。输入一个数组，求出这个数组中的逆序对的总数。

### 示例：   
```cpp
示例 1:
输入: [7,5,6,4]
输出: 5
```

### 解题思路:  
这道题用了两种解法，归并排序和树状数组

### 归并排序
看题解之前完全没想到可以用归并排序来做，看了过后发现这么做简直太妙了。  
总之就是在归并排序的并阶段来计算逆序对，维护一个变量叫做currentAdd，用来保存当前要并的右半部分已经处理过的个数，也就是说，左边还没有加入的，每当加入，逆序对就会增加currentAdd这么多  
顺便还复习了一下归并排序，总之就是，先直接调归并来将左右两边先排好，然后再将这一次的来并起来，并好后，要把并好的结果赋给原数组。  


```cpp
class Solution {
public:
    int MergeSort(int l, int r, vector<int>& nums)
    {  
        if(r-l == 0)
        {
            return 0;
        }
        //先求左右两边中先求出来的逆序对
        int middle = (l+r)/2;
        int reversePairNum = MergeSort(l,middle,nums) + MergeSort(middle+1,r,nums);
        //当左右两边的nums都排好序了，可以计算组合时产生的逆序对
        vector<int> temp;
        int lPointer = l;
        int rPointer = middle+1;
        int currentAdd = 0;
        while(!(lPointer>middle && rPointer>r))
        {
            if(lPointer > middle)
            {
               temp.push_back(nums[rPointer]);
               rPointer ++;
            }
            else if(rPointer > r)
            {
                reversePairNum += currentAdd;
                temp.push_back(nums[lPointer]);
                lPointer++;
            }
            else
            {
                if(nums[lPointer] > nums[rPointer] )
                {
                    currentAdd++;
                    temp.push_back(nums[rPointer]);
                    rPointer++;
                }
                else
                {
                    reversePairNum += currentAdd;
                    temp.push_back(nums[lPointer]);
                    lPointer++;
                }
            }
           
        }
        //将num变成排序后的num
        for(int i=0;i<temp.size();i++)
            nums[l+i] = temp[i];

        return reversePairNum;
    }


    int reversePairs(vector<int>& nums) {
        if(nums.size() == 0)
            return 0;
        return MergeSort(0,nums.size()-1,nums);
    }
};

```

<br/>
<br/>
<br/>

### 树状数组
以为这辈子都见不到树状数组了，没想到过了一年多又见面了，不过这次没这么头疼了哈哈哈，不过树状数组这种方法真的太难想了，估计真的碰到这种题我也不会知道可以用树状数组来解，除非是赤裸裸的单点更新+区间查询  
就是一般的树状数组  
ps:我写的树状数组的update函数是 +=这个值，不是 =这个值，被坑惨了。  
如果要求逆序对的话，把数值的大小作为树状数组的下标就好了  
这样，对原数组从后向前update树状数组，且每次加入都求一下当前的sum，就可以了  
需要注意的是，直接这么搞不行，如果原数组中有特别大的数，或者负数，作为树状数组的下标不科学，所以需要对原数组做处理，即排序后，用排序后的位置来代替自己的数值来作为树状数组的下标，即用相对位置来代替数值，相对位置用二分查找来找(直接从头到尾遍历找还会超时)。

```cpp
class Solution {
public:
    int c[50002];
    int lowbit(int x)
    {
        return x&(-x);
    }

    void update(int pos,int changeValue,int n) //单点修改
    {
        for(int i=pos;i<=n;i+=lowbit(i))
        {
            c[i] += changeValue;
        }
    }

    int sum(int pos) // 查询从 1~pos的值
    {
        int ans=0;
        for(int i=pos;i>=1;i-=lowbit(i))
        {
            ans += c[i];
        }
        return ans;
    } 


    //一定要用二分查找，顺序查找会tle
    int binarySerach(int value, vector<int>& nums)
    {
        //nums is a sorted array
        int length = nums.size();
        int left = 0;
        int right = length-1;
        int middle = (left+right)/2;
        while(left<right)
        {
            middle = (left + right)/2;
            if(value > nums[middle])
            {
                left = middle +1;
            }
            else if (value < nums[middle])
            {
                right = middle;
            }
            else
            {
                return middle;
            }
        }
        if(nums[left] == value)
        {
            return left;
        }
        else
            return -1;
    }

    int reversePairs(vector<int>& nums) {

        vector<int> sortedNums = nums;
        //将nums排序并存为一个新的数组，数的大小就可以由位置来体现，解决了数为负数以及数很大的问题
        sort(sortedNums.begin(),sortedNums.end());
        memset(c,0,sizeof(c));
        int length = nums.size();
        int ans=0;
        for(int i=length-1;i>=0;i--)
        {
            int index = binarySerach(nums[i],sortedNums)+1; //这里加个1，防止为0
            ans += sum(index-1);
            update(index,1,50002); //艹啊，这里的第二个参数是增量，不是改变的量，debug了半天，晕
        }
        return ans;
    }
};

```



### 题目链接：  
https://leetcode-cn.com/problems/shu-zu-zhong-de-ni-xu-dui-lcof/  
[一个讲树状数组很好的博客](https://blog.csdn.net/bestsort/article/details/80796531)