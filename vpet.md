# 虚拟桌宠模拟器使用本工具的配置教程
## 1.安装并运行本工具
### 不多说了,去看[readme.md](https://github.com/huangdihd/hypocrisy/blob/main/README.md)
## 2.打开虚拟桌宠模拟器的设置面板
### 右键桌宠,点击系统,点击设置面板
## 3. 打开ChatGPT设置
### 点击设置面板中上方的系统按钮,找到聊天设置,选择`使用从ChatGPT申请的的API`(多了个字,但是上面就是这么写的)
### 点击下方的`打开 ChatGPT API 设置`按钮
## 4. 配置ChatGPT设置
### 将API URL填写为日志中`* Running on `后面的地址加上`/v1/chat/completions`
### 比如`http://127.0.0.1:34322/v1/chat/completions`
### API Key你设置的token名称,如果忘了可以去项目文件夹下的`token.json`看,里面的结构是这样的:
```json
{"token名称": "token的值(不要泄露)"}
```
## 5. 保存设置
### 点击最下方的`保存设置`按钮就可以了