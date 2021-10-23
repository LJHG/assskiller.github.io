---
title: spring-boot-maven-plugin爆红
date: 2020-05-08 18:18:29
tags: [java, springboot, maven]
---
问题来源居然是maven的settings没配好，要重新装一下阿里的源，之前我装那个居然有问题，服了。  
```xml
<mirror>  
    <id>alimaven</id>  
    <name>aliyun maven</name>  
    <url>http://maven.aliyun.com/nexus/content/groups/public/</url>  
    <mirrorOf>central</mirrorOf>          
</mirror> 
```

xml没高亮是什么鬼
