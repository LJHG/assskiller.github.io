---
title: 205周赛记录---(学会用map + 并查集太强了)
date: 2020-09-06 15:53:20
tags: [map,并查集,连通,图]
---
随意写了，主要记录一下一些有意义的地方
<!-- more -->
## 第一题
没啥好说的
## 第二题
咳咳，第二题我疯狂超时了五发，说一下我是怎么优化的
第二题其实就是给你两个数组，然后让你看一看一个数组中的平方是不是等于另外一个数组中某两个数的乘积，如果是的话，就+1。  
看起来很简单吧，直接写就是on3，超时妥妥的，不过我还是交了一发。  
思考半天后，我想到了用map来进行优化，也就是我建了4个map，然后分别存自己的乘积，两数相乘，但是还是超时了，代码长这样。
```cpp
class Solution {
public:
    int numTriplets(vector<int>& nums1, vector<int>& nums2) {
        //试一下四个map哈
        //这特么也能超时，我很好奇正解是什么
        map<long long,int> apf;
        map<long long,int> acc;
        map<long long,int> bpf;
        map<long long,int> bcc;
        
        int len1 = nums1.size();
        int len2 = nums2.size();
        
        for(int i=0;i<len1;i++){
            apf[(long long)nums1[i] * (long long)nums1[i]]++; //?
            for(int j=i+1;j<len1;j++){
                acc[(long long)nums1[i] * (long long)nums1[j]]++;
            }
        }
        for(int i=0;i<len2;i++){
            bpf[(long long)nums2[i] * (long long)nums2[i]]++; //?
            for(int j=i+1;j<len2;j++){
                bcc[(long long)nums2[i] * (long long)nums2[j]]++;
            }
        }
        int ans = 0;
        for(auto x : apf){
            for(auto y :bcc){
                if(x.first == y.first){
                    ans += x.second*y.second;
                }
            }
        }
        for(auto x : bpf){
            for(auto y :acc){
                if(x.first == y.first){
                    ans += x.second*y.second;
                }
            }
        }
        
        
        return ans;
    }
};
```
随后我想到对序列进行排序可以少进行很多操作，然后**map是自排序的**，那早一点break不就能过了吗(不知道是不是侥幸，反正过了)。
```cpp
class Solution {
public:
    int numTriplets(vector<int>& nums1, vector<int>& nums2) {
        //试一下四个map哈
        //这特么也能超时，我很好奇正解是什么
        map<long long,int> apf;
        map<long long,int> acc;
        map<long long,int> bpf;
        map<long long,int> bcc;
        
        int len1 = nums1.size();
        int len2 = nums2.size();
        
        for(int i=0;i<len1;i++){
            apf[(long long)nums1[i] * (long long)nums1[i]]++; //?
            for(int j=i+1;j<len1;j++){
                acc[(long long)nums1[i] * (long long)nums1[j]]++;
            }
        }
        for(int i=0;i<len2;i++){
            bpf[(long long)nums2[i] * (long long)nums2[i]]++; //?
            for(int j=i+1;j<len2;j++){
                bcc[(long long)nums2[i] * (long long)nums2[j]]++;
            }
        }
        int ans = 0;
        // sort(apf.begin(),apf.end());
        // sort(bpf.begin(),bpf.end());
        // sort(acc.begin(),acc.end());
        // sort(bcc.begin(),bcc.end());
        
        //我再垂死挣扎一波
        for(auto x : bcc){
            for(auto y :apf){
                if(x.first == y.first){
                    ans += x.second*y.second;
                }
                if(x.first < y.first) break;
            }
        }
        for(auto x : acc){
            for(auto y :bpf){
                if(x.first == y.first){
                    ans += x.second*y.second;
                }
                if(x.first < y.first) break;
            }
        }
        //先试一下不用map的
        // int ans =0;
        // int len1 = nums1.size();
        // int len2 = nums2.size();
        // sort(nums1.begin(),nums1.end());
        // sort(nums2.begin(),nums2.end());
        // for(int i=0;i<len1;i++){
        //     for(int j=0;j<len2;j++){
        //         for(int k=j+1;k<len2;k++){
        //             if((long long)nums2[j]*(long long)nums2[k] > (long long)nums1[i]*(long long)nums1[i]) break;
        //             if((long long)nums2[j]*(long long)nums2[k] ==  (long long)nums1[i]*(long long)nums1[i]) ans++;
        //         }
        //     }
        // }
        // for(int i=0;i<len2;i++){
        //     for(int j=0;j<len1;j++){
        //         for(int k=j+1;k<len1;k++){
        //             if((long long)nums1[j]*(long long)nums1[k] > (long long)nums2[i]*(long long)nums2[i]) break;
        //             if((long long)nums1[j]*(long long)nums1[k] ==  (long long)nums2[i]*(long long)nums2[i]) ans++;
        //         }
        //     }
        // }
        //草居然过不了 还是要map
        
        
        return ans;
    }
};
```

最后，当我看到大佬的做法后，我震惊了，也就是说，其实根本没有必要创建四个map，使用两个map分别保存自己的平方就行了，然后在算两数乘积时，直接和存好的map直接比较不就行了吗？  
嗯。。。是的，所以我这里犯了一个很经典的错误：**明明能够直接比，偏要存下来再来比**

## 第三题
ez
## 第四题
重新温习了并查集，其实也不难。  
这道题的描述自己去看题吧，这里说一下思路。  
要求删除最多的边数，我们有理由认为应该尽量少删公共边，而尽量去删A和B自己的边。  
倒过来，也就是尽量多加公共边，然后尽量少加A和B自己的边。  
具体做法是这样的：  
先对全部公共边做判定，如果一条边对应的两个节点是连通的，那么就没必要加。  
对公共边判定完后，再分别的 A 和 B自己来以类似方法判定。  
代码如下(写得很垃圾，代码重复度高而且好像还很慢，不过过了)：
```cpp
class Solution {
public:
    int pre[100010];
    int preA[100010];
    int preB[100010];
    int find(int k)   //寻找k的根结点 
    {
        if(pre[k]==k)	return k; 
        return pre[k]=find(pre[k]); 
    }
 
    void merge(int a,int b) //合并集合 
    {
        int t1=find(a);  //找到a和b的根结点 
        int t2=find(b);
        if(t1!=t2)	pre[t1]=t2;  //靠右，即把左边的集合变成右边的子集合 
    }
    int findA(int k)   //寻找k的根结点 
    {
        if(preA[k]==k)	return k; 
        return preA[k]=findA(preA[k]); 
    }
 
    void mergeA(int a,int b) //合并集合 
    {
        int t1=findA(a);  //找到a和b的根结点 
        int t2=findA(b);
        if(t1!=t2)	preA[t1]=t2;  //靠右，即把左边的集合变成右边的子集合 
    }
    int findB(int k)   //寻找k的根结点 
    {
        if(preB[k]==k)	return k; 
        return preB[k]=findB(preB[k]); 
    }
 
    void mergeB(int a,int b) //合并集合 
    {
        int t1=findB(a);  //找到a和b的根结点 
        int t2=findB(b);
        if(t1!=t2)	preB[t1]=t2;  //靠右，即把左边的集合变成右边的子集合 
    }
    int maxNumEdgesToRemove(int n, vector<vector<int>>& edges) {
        int ans = 0; //最少需要的边数
        for(int i=1;i<=n;i++) pre[i]=i;
        //先对类型3做处理，然后分别对alice和bob做处理
        int len = edges.size();
        for(int i=0;i<len;i++){
            if(edges[i][0] == 3){
                int fa1 = find(edges[i][1]);
                int fa2 = find(edges[i][2]);
                if(fa1 != fa2){
                    ans++;
                    merge(fa1,fa2);
                }
            }
        }
        //复制两份并查集，一份给alice，一份给bob
        
        for(int i=1;i<=n;i++){
            preA[i] = pre[i];
            preB[i] = pre[i];
        }
        //对alice和bob做处理
        for(int i=0;i<len;i++){
            if(edges[i][0] == 1){ //alice
                int fa1 = findA(edges[i][1]);
                int fa2 = findA(edges[i][2]);
                if(fa1 != fa2){
                    ans++;
                    mergeA(fa1,fa2);
                }
            }
            if(edges[i][0] == 2){ //bob
                int fa1 = findB(edges[i][1]);
                int fa2 = findB(edges[i][2]);
                if(fa1 != fa2){
                    ans++;
                    mergeB(fa1,fa2);
                }
            }
        }
        //判断alice 和 bob是否是连通的
        int fatherA = findA(1);
        int fatherB = findB(1);
        for(int i=2;i<=n;i++){
            if(findA(i) != fatherA) return -1;
            if(findB(i) != fatherB) return -1;
        }
        

        return len-ans;
    }
};
```

## 周赛链接
https://leetcode-cn.com/contest/weekly-contest-205/

