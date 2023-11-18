import os
import json
import asyncio
import subprocess
from hashlib import md5
from pathlib import Path
from typing import Literal

import yaml
import uvicorn
import pyperclip
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

LangList = Literal['zh_CN', 'zh_TW', 'en_US', 'ja_JP']


class Config:
    class Server:
        def __init__(self, data: dict):
            self.host: str = data.get('host', '127.0.0.1')
            self.port: int = data.get('port', 33940)

    def __init__(self, data: dict):
        self.server: Config.Server = Config.Server(data.get('server', {}))


if os.path.exists('config.yaml'):
    with open('config.yaml', mode='rt', encoding='utf-8') as f:
        config: Config = Config(yaml.safe_load(f) or {})
else:
    config: Config = Config({})

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)
server = uvicorn.Server(uvicorn.Config(
    app,
    host=config.server.host,
    port=config.server.port
))

base_dir = Path('../')


def split():
    subprocess.run('python .github/scripts/split.py', cwd='../')


@app.get('/translation/{lang}.json')
async def get_translation(lang: LangList) -> dict:
    split()
    with (base_dir / 'translation' / lang).with_suffix('.json').open(mode='rt', encoding='utf-8') as f:
        return json.load(f)


@app.get('/version/translation/{lang}.txt')
async def get_version(lang: LangList) -> str:
    split()
    return md5((base_dir / 'translation' / lang).with_suffix('.json').read_bytes()).hexdigest()


if __name__ == '__main__':
    print('server url copied')
    pyperclip.copy(f'http://{config.server.host}:{config.server.port}/')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(server.serve())
    split()
    subprocess.run('python generate_empty.py')
