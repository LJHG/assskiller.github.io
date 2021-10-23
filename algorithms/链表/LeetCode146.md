---
title: LRU缓存机制---LeetCode146(链表好像变香了)
date: 2020-05-25 21:43:13
tags: [哈希, 链表]
---
## 题目描述：  
运用你所掌握的数据结构，设计和实现一个  LRU (最近最少使用) 缓存机制。它应该支持以下操作： 获取数据 get 和 写入数据 put 。
获取数据 get(key) - 如果密钥 (key) 存在于缓存中，则获取密钥的值（总是正数），否则返回 -1。
写入数据 put(key, value) - 如果密钥已经存在，则变更其数据值；如果密钥不存在，则插入该组「密钥/数据值」。当缓存容量达到上限时，它应该在写入新数据之前删除最久未使用的数据值，从而为新的数据值留出空间。
进阶:
你是否可以在 O(1) 时间复杂度内完成这两种操作？

## 示例：   
```cpp
LRUCache cache = new LRUCache( 2 /* 缓存容量 */ );
cache.put(1, 1);
cache.put(2, 2);
cache.get(1);       // 返回  1
cache.put(3, 3);    // 该操作会使得密钥 2 作废
cache.get(2);       // 返回 -1 (未找到)
cache.put(4, 4);    // 该操作会使得密钥 1 作废
cache.get(1);       // 返回 -1 (未找到)
cache.get(3);       // 返回  3
cache.get(4);       // 返回  4
```
<!-- more -->
## 解题思路:  
这道题注意要各种分类讨论的细节，即先分为Key是否在当前缓存中，如果在，就直接改，如果不在，还要看当前是否已经到达了最大capacity，没到就直接加，到了就要加+删。  
这道题我还是说两个解法吧，虽然第一个不是O1，但也是我第一个想到的方法，第二方法就是O1了。
### 不是O(1)的做法
用两个map，一个就是直接存键值对，另一个存键-时间对，然后每次去遍历看哪个键的时间最小。
```cpp
class LRUCache {
public:
    map<int,int> record; //使用一个map来记录键值
    map<int,int> key_time; //记录键进入的时间
    int time;
    int curNum;
    int size;


    LRUCache(int capacity) {
        time = 0;
        curNum = 0;
        size = capacity;
    }
    
    int get(int key) {
        time++;
        if(record[key] != 0)
        {
            key_time[key] = time;
            return record[key];
        }
            
        return -1;
    }
    
    void put(int key, int value) {
        time++;
        //如果key存在,直接更新
        if(record[key] != 0)
        {
            record[key] = value;
            key_time[key] = time;
        }
        
        else
        {
            //如果不存在，先找出最小的
           map<int,int>::iterator iter = key_time.begin();
           int minKey = 0;
           int minTime = 999999;
           while(iter != key_time.end()) {
                if(iter->second < minTime)
                {
                    minTime = iter->second;
                    minKey = iter->first;
                }
                iter++;
            }

            //cout<<"当前Minkey"<<minKey<<" minTime为"<<minTime<<endl;
            //如果最小的就是这个key，直接改
            if(minKey == key)
            {
                record[key] = value;
                key_time[key] = time;
            }
            //如果最小的不是这个key
            else
            {
                //如果没到capacity，直接更新
                if(curNum < size)
                {
                    record[key] = value;
                    key_time[key] = time;
                    curNum++;
                }
                //不然就删去最小的再更新
                else
                {
                    record[minKey] = 0;
                    record[key] = value;
                    key_time[key] = time;
                    key_time[minKey] = 99999;
                }
                
            }
        }
        
    }
};

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache* obj = new LRUCache(capacity);
 * int param_1 = obj->get(key);
 * obj->put(key,value);
 */
```

</br>

### O(1)做法
O(1)做法使用的是哈希表+双向链表，这次的双向链表比起以前写链表感觉要简单了许多，主要是要先把虚拟节点创好，这样就十分方便。  
在这个方法中，哈希表存得是key-节点指针，双向链表可以用来表示一个key的优先度，最近被使用的在表头，最久不被使用的在表尾巴，双向链表将一个节点移动到表头，添加节点到表头，从表尾删除节点都是O(1)，就非常适合这道题。
```cpp
struct Node{
    int key;
    int val;
    Node* prev;
    Node* next; 
    Node(int k,int v): key(k),val(v), prev(NULL), next(NULL) {} 
};
class LRUCache {
public:
    Node* head;
    Node* tail;
    int size;
    int curSize;
    map<int,Node*>  record; //哈希表里存key与对应在链表里的地址

    LRUCache(int capacity) {
        size = capacity;
        curSize = 0;
        head = new Node(0,0);
        tail = new Node(0,0);
        head->next = tail;
        tail->prev = head;
    }
    
    int get(int key) {
        if(record[key] != NULL)
        {
            moveToFront(record[key]);//把它放到前面去
            //printList();
            return record[key]->val;
        }
        else
        {
            //printList();
            return -1;
        }
    }
    
    void put(int key, int value) {
        //如果key存在，直接修改值，并把它移动到表头
        if(record[key] != NULL)
        {
            moveToFront(record[key]);
            record[key]->val = value;
        }
        //如果key不存在
        else
        {
            //如果长度小于capacity，直接添加到表头
            if(curSize < size)
            {
                Node* newNode = new Node(key,value);
                addToFront(newNode);
                record[key] = newNode;
                curSize++;
            }
            //添加到表头，删除表尾元素
            else
            {
                Node* newNode = new Node(key,value);
                addToFront(newNode);
                record[key] = newNode;
                deleteFromEnd();
            }
        }
        //printList();
    }

    void addToFront(Node* node)
    {
        node->next = head->next;
        node->prev = head;
        head->next->prev = node;
        head->next = node;
    }

    void moveToFront(Node* node)
    {
        node->prev->next = node->next;
        node->next->prev = node->prev;
        addToFront(node);    
    }

    void deleteFromEnd()
    {
        if(tail->prev == head) return;
        
        record[tail->prev->key] = NULL;
        tail->prev->prev->next = tail;
        tail->prev = tail->prev->prev;
    }
    
    void printList()
    {
        Node* ptr = head;
        while(ptr != NULL)
        {
            cout<<ptr->val<<"->";
            ptr=ptr->next;
        }
        cout<<endl;
    }


   
};

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache* obj = new LRUCache(capacity);
 * int param_1 = obj->get(key);
 * obj->put(key,value);
 */
```

## 题目链接：  
https://leetcode-cn.com/problems/lru-cache/