---
title: batch的并行
date: 2021-09-24 15:53:27
tags: [deep learning, cuda]
---

最近研究了一下深度学习中一个batch的数据到底是不是并行计算的(这个问题可能有点蠢)，这里说一下结论，是的。
<!-- more -->
具体是怎么得出这个结论的呢，简单写了下代码测试了一下：
使用的网络是CIFAR100数据集上的[VGG19](https://github.com/weiaicunzai/pytorch-cifar100/blob/master/models/vgg.py)

```python
def run_cpu(input):
    model = vgg19_bn()
    start = time.time()
    output = model(input)
    end = time.time()
    print("cpu耗时:{}".format(end-start))

def run_gpu(input):
    model = vgg19_bn().cuda()
    input = input.cuda()
    start = time.time()
    output = model(input)
    end = time.time()
    print("gpu耗时:{}".format(end-start))

if __name__ == '__main__':
    input = torch.zeros((64,3,32,32))
    run_cpu(input)
    run_gpu(input)
```

运行结果：

```
# batch_size 为16
cpu耗时:0.1640024185180664
gpu耗时:1.0924582481384277
```

```
# batch_size 为64
耗时:0.4629640579223633
耗时:0.943659782409668
```

```
# batch_size 为256
耗时:1.5650031566619873
耗时:0.9624972343444824
```

```
# batch_size 为512
耗时:3.0149896144866943
耗时:1.581861972808838
```

随着batch_size的上升，使用cpu计算的时间自然是一直在增加。
但是gpu的计算时间在batch_size为256之前并没有增加，而是直到512才开始增加。
由此我们可以得出结论：**在GPU算力能够承受的范围内，一个batch的计算是并行的。**

