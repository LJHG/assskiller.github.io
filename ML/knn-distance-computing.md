---
title: 计算欧式距离的三种姿势
date: 2020-11-02 15:58:46
tags: [机器学习, machine learning, numpy]
---
最近在看cs231n，第一个作业里的第一个就是KNN，总所周知，KNN中距离矩阵的计算是非常重要的，这个作业里列举了三种距离的计算方式，当时就震惊了，这里来记录一下。

<!-- more -->

# 双重循环

emmm，最显而易见的方式，不多说，直接上代码。
ps: 突然发现typora里面的插入代码方式hexo也可以认识，终于可以不用写那个啥奇怪的codeblock了。

```python
def compute_distances_two_loops(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using a nested loop over both the training data and the 
    test data.
    Inputs:
    - X: A numpy array of shape (num_test, D) containing test data.
    - num_test是测试集里样本的数量，D是像素点的个数(这里是3072,3*32*32)
    Returns:
    - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
      is the Euclidean distance between the ith test point and the jth training
      point.
    """
    num_test = X.shape[0]
    num_train = self.X_train.shape[0]
    dists = np.zeros((num_test, num_train))
    for i in xrange(num_test):
      for j in xrange(num_train):
        #####################################################################
        # TODO:                                                             #
        # Compute the l2 distance between the ith test point and the jth    #
        # training point, and store the result in dists[i, j]. You should   #
        # not use a loop over dimension.                                    #
        #####################################################################
        dists[i][j] =  np.linalg.norm(X[i] - self.X_train[j])  #求欧式距离
        pass
        #####################################################################
        #                       END OF YOUR CODE                            #
        #####################################################################
    return dists
```

呃，这里要说一下，计算距离时不是一定要写成np.linalg.norm(X[i] - self.X_train[j])，其实写成和下面的单重循环那种形式一样也可以，没区别。

# 单重循环
单重循环应该说是很好的利用了numpy的特性吧，等于就是让numpy来帮你做了循环，这里举个例子。

假设有代码如下：

```python
a = np.array([[1,2,3]])
b = np.array([1])
print(a+b)
```

这种相加在numpy中是可行的，结果为：

```python
[[2 3 4]]
```

既然可以这样操作，那么如果将其运用于距离计算中，便可以少写一重循环了。

代码如下：

```python
 def compute_distances_one_loop(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using a single loop over the test data.
    Input / Output: Same as compute_distances_two_loops
    """
    num_test = X.shape[0]
    num_train = self.X_train.shape[0]
    dists = np.zeros((num_test, num_train))
    for i in xrange(num_test):
      #######################################################################
      # TODO:                                                               #
      # Compute the l2 distance between the ith test point and all training #
      # points, and store the result in dists[i, :].                        #
      #######################################################################
      dists[i] = np.sqrt(np.sum(np.square(self.X_train-X[i]),axis=1))
      pass
      #######################################################################
      #                         END OF YOUR CODE                            #
      #######################################################################
    return dists
```



# 不用循环

这个方法超级叼，将计算欧式距离完全转换为了矩阵运算

推导过程可以见[这一篇博文](https://blog.csdn.net/IT_forlearn/article/details/100022244)，公式写的很详细。

具体代码如下：

```python
def compute_distances_no_loops(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using no explicit loops.
    Input / Output: Same as compute_distances_two_loops
    """
    num_test = X.shape[0]
    num_train = self.X_train.shape[0]
    dists = np.zeros((num_test, num_train)) 
    #########################################################################
    # TODO:                                                                 #
    # Compute the l2 distance between all test points and all training      #
    # points without using any explicit loops, and store the result in      #
    # dists.                                                                #
    #                                                                       #
    # You should implement this function using only basic array operations; #
    # in particular you should not use functions from scipy.                #
    #                                                                       #
    # HINT: Try to formulate the l2 distance using matrix multiplication    #
    #       and two broadcast sums.                                         #
    #########################################################################
    d1 = np.sum(np.square(X),axis=1,keepdims=True) #shape(num_test,1)
    d2 = np.sum(np.square(self.X_train),axis=1) #shape(1,num_train)
    d3 = np.multiply(np.dot(X,self.X_train.T),-2) #shape(num_test,num_train)
    dists = np.sqrt(d1+d2+d3)
    #numpy真的神奇，d1和d2居然可以加，一个是 num_test*1 一个是 1*num_train，两个一加变成了num_test*num_train 而每一行就是num_test里的每一个元素加上num_train的一行的那个元素
    pass
    #########################################################################
    #                         END OF YOUR CODE                              #
    #########################################################################
    return dists
```



# 三种方法的耗时比较

```python
# Let's compare how fast the implementations are
def time_function(f, *args):
    """
    Call a function f with args and return the time (in seconds) that it took to execute.
    """
    import time
    tic = time.time()
    f(*args)
    toc = time.time()
    return toc - tic

two_loop_time = time_function(classifier.compute_distances_two_loops, X_test)
print('Two loop version took %f seconds' % two_loop_time)

one_loop_time = time_function(classifier.compute_distances_one_loop, X_test)
print('One loop version took %f seconds' % one_loop_time)

no_loop_time = time_function(classifier.compute_distances_no_loops, X_test)
print('No loop version took %f seconds' % no_loop_time)

# you should see significantly faster performance with the fully vectorized implementation

--------
Two loop version took 37.711502 seconds
One loop version took 96.402259 seconds
No loop version took 0.381577 seconds
```





最后吐槽一下，hexo写博客插图片真的太蠢了，居然不能插相对路径，别人github都可以，搞得我在typora上写起来及其不友好，只好不插图片了唉。