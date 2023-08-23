import json
import sys
import uuid
import os

import requests
from flask import Flask, request

app = Flask(__name__)

config = None


def init():
    global config
    if not os.path.exists('config.json'):
        print('未找到配置文件,请添加(往后版本会做创建向导)')
        sys.exit()
    else:
        config = json.load(open('config.json', 'r'))
        if config['pandora'][-1] != '/':
            config['pandora'] += '/'


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
    gpt = requests.post(url=config['pandora'] + '/api/conversation/talk', headers=headers, json=data)
    if gpt.status_code == 200:
        config[token] = {
            'conversation_id': gpt.json()['conversation_id'],
            'message_id': str(gpt.json()['message']['id'])
        }
        with open('config.json', 'w') as f:
            f.write(json.dumps(config, indent=4))
        return gpt.json()['message']['content']['parts'][0]
    elif gpt.headers.get('Content-Type') == 'application/json':
        if 'detail' in gpt.json():
            return '发生错误' + str(gpt.json()['detail'])
        else:
            return '发生错误,错误码:' + str(gpt.status_code)
    else:
        return gpt.text


@app.route('/v1/chat/completions', methods=["POST"])
def talk():
    message = request.json['messages'][-1]['content']
    return {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": chat(message, request.headers.get("Authorization")[7:]),
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
    }


if __name__ == '__main__':
    init()
    app.run(port=34322)
