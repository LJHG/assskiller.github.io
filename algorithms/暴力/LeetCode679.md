---
title: 24点---LeetCode679
date: 2020-08-22 15:05:37
tags: [暴力]
---
## 题目描述：  
你有 4 张写有 1 到 9 数字的牌。你需要判断是否能通过 *，/，+，-，(，) 的运算得到 24。

## 示例：   
```cpp
示例 1:
输入: [4, 1, 8, 7]
输出: True
解释: (8-4) * (7-1) = 24

示例 2:
输入: [1, 2, 1, 2]
输出: False

注意:
除法运算符 / 表示实数除法，而不是整数除法。例如 4 / (1 - 2/3) = 12 。
每个运算符对两个数进行运算。特别是我们不能用 - 作为一元运算符。例如，[1, 1, 1, 1] 作为输入时，表达式 -1 - 1 - 1 - 1 是不允许的。
你不能将数字连接在一起。例如，输入为 [1, 2, 1, 2] 时，不能写成 12 + 12 。
```
<!-- more -->

## 解题思路:  
这道题一看数据量不大，所以暴力算是很自然的想法吧()。  
首先你要判断出这道题该怎么去穷举出所有情况，正确的做法应该是 C42 * 8* C32* 8 * 8,C42就是从4个数里先选出两个数来做运算，乘8就是这两个数有8种运算情况，然后把结果和剩下的两个数组合为一个3个数的向量，然后再从中选出2个来运算，然后。。。。。。  
需要注意的点是选出两个数做完运算的结果应该和剩下没有做运算的数字一起加入到新的数组中，然后套娃，这样一想其实是可以dfs的，但是我用的暴力，都差不多吧，就懒得写了。  
代码如下:

```cpp
class Solution {
public:
    bool judgePoint24(vector<int>& nums) {
        //可能性不多，直接穷举
        vector<double> doubleNums;
        for(int i=0;i<4;i++){
            doubleNums.push_back(double(nums[i]));
        }
        for(int i=0;i<4;i++){
            for(int j=0;j<4;j++){
                if(i == j) continue;
                double num1 = doubleNums[i];
                double num2 = doubleNums[j];
                double res1 =0;
                for(int k=0;k<4;k++){
                    if(k==0) res1 = num1*num2;
                    if(k==1 && fabs(num2-0) < 0.00001) continue;
                    if(k==1) res1 = num1/num2;
                    if(k==2) res1 = num1+num2;
                    if(k==3) res1 = num1-num2;
                    //从剩下的两个数里选择一个与res1做运算(才怪了，谁说一定要先和res1运算)
                    //正确的做法是把res1和剩下两个数加入新的数组
                    vector<double> numsHas3Elements;
                    numsHas3Elements.push_back(res1);
                    for(int kkk=0;kkk<4;kkk++){
                        if(kkk==i || kkk==j) continue;
                        numsHas3Elements.push_back(doubleNums[kkk]);
                    }
                    for(int m=0;m<3;m++){
                        for(int n=0;n<3;n++){
                            if(m==n) continue;
                            double newNum1 = numsHas3Elements[m];
                            double newNum2 = numsHas3Elements[n];
                            double res2 = 0;
                            for(int p=0;p<4;p++){
                                if(p==0) res2 = newNum1+newNum2;
                                if(p==1) {
                                    res2 = newNum1-newNum2;
                                    // if(res1 == 0.75)
                                    // cout<<newNum1<<" "<<newNum2<<" "<<res2<<endl;
                                }
                                if(p==2) res2 = newNum1*newNum2;
                                if(p==3 && fabs(newNum2-0)<0.00001) continue;
                                if(p==3) res2 = newNum1/newNum2;
                                double finalNum = numsHas3Elements[3-m-n];
                            double res3 = 0;
                            for(int f=0;f<6;f++){
                                if(f==0) res3 = res2+finalNum;
                                if(f==1) res3 = res2-finalNum;
                                if(f==2) res3 = res2*finalNum;
                                if(f==3 && fabs(finalNum-0) < 0.00001) continue;
                                if(f==3) res3 = res2/finalNum;
                                if(f==4) res3 = finalNum-res2;
                                if(f==5 && fabs(res2-0) < 0.00001) continue;
                                if(f==5) res3 = finalNum/res2;
                                if(fabs(res3-24) < 0.00001) return true;
                                
                            }
                            }
                            
                        }
                    }
                    
                }

            }
        }
        return false;
    }
};
```

要注意一下浮点数绝对值是fabs

这里要列一个我傻逼的地方，可能是写High了，在写循环时，我写成了
```cpp
for(int m=0;m<4&&m!=i&&m!=j;m++)
```
其实我想表达的意思是
```cpp
 for(int m=0;m<4;m++){
    if(m==i || m==j) continue;
 }
```
草，太搞笑了

## 题目链接：  
https://leetcode-cn.com/problems/24-game/