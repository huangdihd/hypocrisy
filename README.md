# hypocrisy
## 将pandora提供的免费GPTAPI伪装成官方API的工具
# 项目简介
## 你是否还在为了一些只用了ChatGPT聊天功能的工具在调用官方付费API耗费大量金钱而烦恼?
## 那就快来试试hypocrisy吧!
# 使用前声明: 
## **此项目不能在任何程度上完美平替官方API**
# 使用教程
## 1. 安装并启动pandra项目的server模式
### 可以去[这里](https://github.com/pengzhile/pandora/blob/master/doc/wiki.md)查看pandora开发者写的教程
## 2. 克隆仓库
### 使用`git clone https://github.com/huangdihd/hypocrisy` 来克隆本仓库
## 3. 填写配置文件
```json
{
    //你要使用的模型
    "model": "gpt-3.5",
    //pandora的server模式下的地址
    "pandora": "https://api.gpt.dicloud.vip/"
}
```
## 4. 启动
### 直接 `python3 main.py`就行了,~~比原神启动还简单~~
## 再次声明,**此项目不能在任何程度上完美平替官方API**