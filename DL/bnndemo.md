---
title: 使用larq对BNN从训练到部署
date: 2021-05-29 20:30:04
tags: [二值神经网络]
---

由于一些机缘巧合，接触到了二值神经网络，于是它就成为了我毕业设计的选题。经过一番挣扎过后，也算是简单做了一点东西，在此记录一下。

<!-- more -->

## 1. 模型的搭建以及训练

目前的二值神经网络的搭建与部署一般有两种方法：

1. 使用pytorch搭建模型，训练后转为onnx，然后使用**dabnn**或者**bolt**进行部署。这种方法的好处在于Pytorch框架本身比较好用，也比较自由。但是在部署时常常会出现dabnn或者bolt转换模型失败的情况，有时还是比较头疼。尤其是在dabnn不再维护，bolt的二值网络仅支持armv7.2指令集以上的手机时，这种方法让我直接走不下去了。
2. 使用[**larq**](https://github.com/larq/larq)进行搭建并且使用LCE进行部署。这种方法的好处在于模型搭建简单以及模型转换以及部署的简单，这也是我最后使用的方法，唯一的缺点可能在于tensorflow相较于pytorch没那么好用，而且这边的模型搭建一般推荐使用Sequential的方式，总之最好不要用Model子类的方式来搭建模型，因为larq对那种方法支持不是很好。

在这里我使用了Bi-Real Net18来进行训练，使用了larq以及tensorflow来搭建模型。模型的搭建大致是参考larq_zoo里的代码，因为我是在CIFAR100数据集上进行训练，所以我对网络的开头做了一点修改，把卷积核以及步长改小了一点，去掉了池化层，这样效果会好一些。模型训练完毕后，将模型保存为.h5格式。



## 2. 模型转换

如果使用larq的话，模型转换这一步就比较简单，通过调用以下几行代码，直接将模型转换为tflite格式即可。

```python
import larq as lq
import larq_compute_engine as lce
import tensorflow as tf

m = tf.keras.models.load_model("mobilev1.h5")
lq.models.summary(m)
with open("mobilenetV1.tflite", "wb") as flatbuffer_file:
    flatbuffer_bytes = lce.convert_keras_model(m)
    flatbuffer_file.write(flatbuffer_bytes)
```



## 3. 模型部署

模型部署需要使用到LCE，因为最后需要将模型在app中跑起来，所以在这一步中我们的目标是编写相关的C++代码实现推理，将代码使用JNI进行封装，并且最后将代码编译成为.so文件，即动态链接库，然后最后将这个.so文件放入Android Studio来进行调用。详细的流程如下所示。

### 3.1 安装LCE

模型推理的过程，使用了[LCE](https://github.com/larq/compute-engine)，直接去github页面看安装过程就好了，他们的文档写得很详细。

### 3.2 编写推理代码并编译

LCE安装好后，我们在LCE根目录下新建一个文件夹叫做jni_lce，里面用来存放我们即将编写的代码。在该文件夹下编写lce.cc文件。这里截取部分代码这个文件很简单，实现了两个函数，一个是loadModel，一个是predict。此处要注意JNI编程的函数命名规范。举个例子，Java_com_ljh_bnndemo_Net_loadModel这个函数对应的就是com.ljh.bnndemo包下的Net类的loadModel方法。此外，还要注意的是，我这里直接使用了一个全局变量来保存读取的模型(interpreter)，这种写法其实很烂，但我也不知道怎么写才能更好了2333。

```c++

//use a interpreter as a global variable
std::unique_ptr<Interpreter> interpreter;

extern "C" JNIEXPORT jboolean JNICALL
Java_com_ljh_bnndemo_Net_loadModel(
        JNIEnv* env,
        jobject thiz,
        jobject model_buffer) {

  char* buffer = static_cast<char*>(env->GetDirectBufferAddress(model_buffer));
  size_t buffer_size = static_cast<size_t>(env->GetDirectBufferCapacity(model_buffer));

  // Load model
  std::unique_ptr<tflite::FlatBufferModel> model =
      tflite::FlatBufferModel::BuildFromBuffer(buffer,buffer_size);
  TFLITE_MINIMAL_CHECK(model != nullptr);

  // Build the interpreter
  tflite::ops::builtin::BuiltinOpResolver resolver;
  compute_engine::tflite::RegisterLCECustomOps(&resolver);

  InterpreterBuilder builder(*model, resolver);
  builder(&interpreter);
  TFLITE_MINIMAL_CHECK(interpreter != nullptr);

  // Allocate tensor buffers.
  TFLITE_MINIMAL_CHECK(interpreter->AllocateTensors() == kTfLiteOk);

  LOGI("model load succeed!!!");
    
   return true;
}

extern "C" JNIEXPORT jfloatArray JNICALL
Java_com_ljh_bnndemo_Net_predict(
        JNIEnv* env,
        jobject thiz,
        jfloatArray arr) {

    float *jInput;
    jInput = env->GetFloatArrayElements(arr, 0);
    const jint length = env->GetArrayLength(arr);

  LOGI(".................start to predict....................");
    //   // Fill input buffers
  // TODO(user): Insert code to fill input tensors
  float* input = interpreter->typed_input_tensor<float>(0);

  for(int i=0;i<1024;i++)
  {
    input[i*3 + 0] = jInput[i*3 + 0];
    input[i*3 + 1] = jInput[i*3 + 1];
    input[i*3 + 2] = jInput[i*3 + 2];
  }

  // Run inference
  TFLITE_MINIMAL_CHECK(interpreter->Invoke() == kTfLiteOk);

  // Read output buffers
  float* output = interpreter->typed_output_tensor<float>(0);

  //输出
  //CIFAR100对应100分类
  float *log_mel = new float[100];
  for(int i=0;i<100;i++){
    log_mel[i] = output[i];
  }
  jfloatArray result = env->NewFloatArray(100);
  env -> SetFloatArrayRegion(result,0,100,log_mel);

  LOGI("predict over \n");
    
  return result;
}

```

代码编写完毕后，需要编写build文件来进行编译，LCE使用的是bazel来进行管理项目，所以build文件的编写如下

```
load("@org_tensorflow//tensorflow/lite:build_def.bzl", "tflite_linkopts")

package(
    default_visibility = ["//visibility:public"],
    licenses = ["notice"],  # Apache 2.0
)

cc_binary(
    name = "liblce.so",
    srcs = [
        "lce.cc",
    ],
    linkopts = tflite_linkopts() + select({
        "@org_tensorflow//tensorflow:android": [
            "-pie",  # Android 5.0 and later supports only PIE
            "-lm",  # some builtin ops, e.g., tanh, need -lm
        ],
        "//conditions:default": [],
    }),
    deps = [
        "//larq_compute_engine/tflite/kernels:lce_op_kernels",
        "@org_tensorflow//tensorflow/lite:framework",
        "@org_tensorflow//tensorflow/lite/kernels:builtin_ops",
    ],
    linkshared=True,
)
```

随后需要对项目进行编译：

在LCE根目录下使用bazel对该项目进行编译。如下：

   ```shell
   bazel build  --config=android_arm64 //jni_lce:liblce.so
   ```

编译后会生成一个LCE/bazel-bin文件夹。LCE/bazel-bin/jni_lce文件夹下找到**liblce.so**动态链接库文件，得到这个文件后，就可以将该文件添加到Android Studio中的工程项目中，并使用相关java进行调用了。



### 3.3 在Android Studio中调用

首先，需要将动态链接库添加到android studio中，此处需要在项目的**main**文件夹下创建**jniLibs**文件夹，随后在jniLibs文件夹下创建**arm64-v8a**文件夹，随后将liblce.so文件放在arm64-v8a文件夹内。

然后需要为创建相关的类以及方法来实现对于C++编写的函数的调用。在这里我们在com.ljh.bnndemo包下创建Net类，并且类中相关的代码编写如下：

   ```java
   package com.ljh.bnndemo;
   
   import java.nio.ByteBuffer;
   
   public class Net {
       static {
           System.loadLibrary("lce");
       }
   
       public native boolean loadModel(ByteBuffer modelBuffer);
       public native float[] predict(float[] input);
   }
   ```

接下来只需要对这两个方法进行调用就可以了。

至此就完成了从BNN的训练到部署啦。关于app的详细代码可以见https://github.com/LJHG/BNNDemo

