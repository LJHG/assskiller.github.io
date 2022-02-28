# Assignment4

## 1. 运行结果

运行结果：

<img src="https://gitee.com/ljh112233/whatisthis/raw/master/static/image-20220228220709563.png" alt="image-20220228220709563" style="zoom: 33%;" />

## 2. 实现细节

[详细代码](https://github.com/LJHG/GAMES101-assignments)

这次作业比较简单，写一个递归程序就能实现功能，具体如下所示：

```cpp
cv::Point2f recursive_bezier(const std::vector<cv::Point2f> &control_points, float t) 
{
    // TODO: Implement de Casteljau's algorithm
    //当点数量为1时，返回
    if(control_points.size() == 1){
        return control_points[0];
    }
    std::vector<cv::Point2f> new_control_points; new_control_points.clear();
    cv::Point2f prev_point = control_points[0];
    for(int i=1;i<control_points.size();i++){
        new_control_points.push_back(prev_point*(1-t) + control_points[i]*t);
        prev_point = control_points[i];
    }
    return recursive_bezier(new_control_points,t);
}

void bezier(const std::vector<cv::Point2f> &control_points, cv::Mat &window) 
{
    // TODO: Iterate through all t = 0 to t = 1 with small steps, and call de Casteljau's 
    // recursive Bezier algorithm.
    for(float t = 0; t < 1; t += 0.001){
        cv::Point2f point = recursive_bezier(control_points, t);
        window.at<cv::Vec3b>(point.y, point.x)[1] = 255;
    } 
}
```


