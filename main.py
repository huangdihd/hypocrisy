import json
import sys
import uuid
import os
import threading
from datetime import datetime

try:
    import requests
except ModuleNotFoundError:
    print('检测到缺少库:requests,正在安装')
    os.system(sys.executable + ' -m pip install requests')
try:
    from flask import Flask, request
except ModuleNotFoundError:
    print('检测到缺少库:flask,正在安装')
    os.system(sys.executable + ' -m pip install flask')

app = Flask(__name__)

config = None

pandora_services = None


def pandora_starter(command):
    os.system(command)


def config_guide():
    pandora = input('输入pandora项目的地址(如没有就直接回车):')
    pandora_command = ""
    if pandora == "":
        print('没有检测到输入,正在安装pandora!')
        os.system(sys.executable + ' -m pip install pandora-chatgpt')
        pandora_port = input('pandora的运行端口:')
        pandora = "http://127.0.0.1:" + pandora_port + '/'
        pandora_command = f'pandora -s 127.0.0.1:{pandora_port} --tokens_file token.json'
        pandora_token = {}
        for i in range(
                int(input(f'你准备输入几个token?(可以去https://ai-{datetime.now().strftime("%Y%m%d")}.fakeopen.com/auth1获取):'))):
            pandora_token[input('token的名称:')] = input('token的值:')
        with open('token.json', 'w') as f:
            f.write(json.dumps(pandora_token))
    model = input('使用的模型:')
    ip = input('监听的ip(一般写127.0.0.1):')
    port = int(input('监听的端口:'))
    with open('config.json', 'w') as f:
        f.write(json.dumps({
            "model": model,
            "pandora": pandora,
            "port": port,
            "ip": ip,
            "pandora_command": pandora_command
        }))


def init():
    global config, pandora_services
    if not os.path.exists('config.json'):
        print('未检测到配置文件,创建向导启动!')
        config_guide()
    config = json.load(open('config.json', 'r'))
    if config['pandora'][-1] != '/':
        config['pandora'] += '/'
    if config['pandora_command'] != '':
        pandora_services = threading.Thread(target=pandora_starter, args=(config['pandora_command'],))
        pandora_services.start()


def chat(prompt, token):
    global config
    headers = {
        'X-Use-Token': token
    }
    if token not in config:
        data = {
            'model': config['model'],
            "prompt": prompt,
            "message_id": str(uuid.uuid4()),
            "parent_message_id": str(uuid.uuid4()),
            'stream': False
        }
    else:
        data = {
            'conversation_id': config[token]['conversation_id'],
            'model': config['model'],
            "prompt": prompt,
            "message_id": str(uuid.uuid4()),
            "parent_message_id": config[token]['message_id'],
            'stream': False
        }
    gpt = requests.post(url=config['pandora'] + 'api/conversation/talk', headers=headers, json=data)
    if gpt.status_code == 200:
        config[token] = {
            'conversation_id': gpt.json()['conversation_id'],
            'message_id': str(gpt.json()['message']['id'])
        }
        with open('config.json', 'w') as f:
            f.write(json.dumps(config, indent=4))
        return gpt.json()['message']['content']['parts'][0], True, gpt.status_code
    elif gpt.headers.get('Content-Type') == 'application/json':
        return gpt.json()['detail'], False, gpt.status_code
    else:
        return gpt.text, False, gpt.status_code


@app.route('/v1/chat/completions', methods=["POST"])
def talk():
    message = request.json['messages'][-1]['content']
    gpt, status, code = chat(message, request.headers.get("Authorization")[7:])
    if status:
        return {
                   "choices": [
                       {
                           "finish_reason": "stop",
                           "index": 0,
                           "message": {
                               "content": gpt,
                               "role": "assistant"
                           }
                       }
                   ],
                   "created": 0,
                   "id": "",
                   "model": "",
                   "object": "chat.completion",
                   "usage": {
                       "completion_tokens": 0,
                       "prompt_tokens": 0,
                       "total_tokens": 0
                   }
               }, code
    else:
        return gpt, code


if __name__ == '__main__':
    init()
    app.run(ip=config['ip'], port=config['port'])
