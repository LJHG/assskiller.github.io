# Assignment6

光线追踪之BVH加速

## 1. 运行结果

运行结果：

<img src="https://gitee.com/ljh112233/whatisthis/raw/master/static/image-20220306213926220.png" alt="image-20220306213926220" style="zoom:33%;" />

## 2. 实现细节

[详细代码](https://github.com/LJHG/GAMES101-assignments)

这次作业使用了BVH来对光线追踪实现了加速，其中有两个地方比较重要：

1. 如何实现光线和**A**xis-**A**ligned **B**ounding **B**ox(AABB)求交。
2. 如何实现光线和BVH的一个node求交。



## 2.1 光线与AABB求交

这个的具体做法在GAMES101课程里已经讲的很清楚了：

使用六个平面来定义出一个box：

<img src="https://gitee.com/ljh112233/whatisthis/raw/master/static/image-20220307092826919.png" alt="image-20220307092826919" style="zoom:33%;" />

然后计算光线与这六个平面相交的时间，因为是axis-aligned的，所以可以采用正视图/侧视图/俯视图的方式来简易计算求交的时间。

<img src="https://gitee.com/ljh112233/whatisthis/raw/master/static/image-20220307092721269.png" alt="image-20220307092721269" style="zoom:33%;" />

对于每一个axis，可以计算出两个平面的求交时间分别为t_min和t_max，于是最后我们可以得到三组t_min, t_max。

最后取一个交集，就能够计算出光线进入这个box的t_min, t_max：

<img src="https://gitee.com/ljh112233/whatisthis/raw/master/static/image-20220307093155285.png" alt="image-20220307093155285" style="zoom: 33%;" />

具体的代码如下所示：

```python
inline bool Bounds3::IntersectP(const Ray& ray, const Vector3f& invDir,
                                const std::array<int, 3>& dirIsNeg) const
{
    // invDir: ray direction(x,y,z), invDir=(1.0/x,1.0/y,1.0/z), use this because Multiply is faster that Division
    // dirIsNeg: ray direction(x,y,z), dirIsNeg=[int(x>0),int(y>0),int(z>0)], use this to simplify your logic
    // TODO test if ray bound intersects
    
    /**
     * 包围盒的元素：Vector3f pMin, pMax;
     * 由 location = origin + time * direction --> time = (location - origin)/direction
     */
    float t1,t2 = 0;
    //这里不能在最后直接乘一个+-1来改变time的正负，不然要出事
    t1 = (pMin.x - ray.origin.x) * invDir.x;
    t2 = (pMax.x - ray.origin.x) * invDir.x;
    float x_tmin = (dirIsNeg[0] > 0) ? t1 : t2;
    float x_tmax = (dirIsNeg[0] > 0) ? t2 : t1; 
    t1 = (pMin.y - ray.origin.y) * invDir.y;
    t2 = (pMax.y - ray.origin.y) * invDir.y;
    float y_tmin = (dirIsNeg[1] > 0) ? t1 : t2;
    float y_tmax = (dirIsNeg[1] > 0) ? t2 : t1;
    t1 = (pMin.z - ray.origin.z) * invDir.z;
    t2 = (pMax.z - ray.origin.z) * invDir.z;
    float z_tmin = (dirIsNeg[2] > 0) ? t1 : t2;
    float z_tmax = (dirIsNeg[2] > 0) ? t2 : t1;

    float t_enter = std::max(x_tmin,std::max(y_tmin,z_tmin));
    float t_exit = std::min(x_tmax,std::min(y_tmax,z_tmax));

    if(t_enter < t_exit && t_exit >= 0){
        return true;
    }
    return false; 
}
```

注意这里是通过判断光线的方向是否为正/负来判断为每一个轴的t_min和t_max来赋什么值，这里不能直接给t直接乘一个正负号，因为后面要判断t_exit >=0 ，如果正负号改变了，那么后面应该也要改，就比较复杂了。



## 2.2 光线与BVH的一个node求交

这就是一个简单的递归：

1. 首先让光线与node对应的bounding box求交，如果没有交点，那么返回空。
2. 如果光线与node的bounding box 有交点而且node是叶子节点，那么让光线与叶子节点里的物体求交，并且返回 intersection。(根据这个项目其他部分的代码可以看出，每一个叶子只有一个物体，不会包含多个物体)
3. 如果光线和node的bounding box 有交点而且node不是叶子节点，那么与左右儿子分别相交获取交点，并且返回比较近的那个。

```cpp
Intersection BVHAccel::getIntersection(BVHBuildNode* node, const Ray& ray) const
{
    Intersection _intersection;
    // TODO Traverse the BVH to find intersection
    Vector3f invDir = ray.direction_inv;
    std::array<int, 3> dirIsNeg = {int(ray.direction.x > 0), int(ray.direction.y > 0), int(ray.direction.z) > 0};

    if(!node->bounds.IntersectP(ray,invDir,dirIsNeg) || node == nullptr){
        return _intersection;
    }
    if(node->left == nullptr && node->right == nullptr){
        //如果是叶节点，与叶节点的objects相交，并且返回intersection
        return node->object->getIntersection(ray);
    }
    Intersection hit1 = getIntersection(node->left,ray);
    Intersection hit2 = getIntersection(node->right,ray);

    return (hit1.distance < hit2.distance)?hit1:hit2;
}
```

