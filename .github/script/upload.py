# -*- coding: UTF-8 -*-

import os
import time
import hashlib
import asyncio
from pathlib import Path
from typing import Awaitable

import aiohttp


class Uploader:
    def __init__(self, client: aiohttp.ClientSession, key: str, server):
        self.key = key
        self.server = server
        self.client = client

    @property
    def sign(self) -> dict:
        ts = str(int(time.time()))
        signature = hashlib.sha256(f'{self.key}MTS{ts}'.encode('utf-8')).hexdigest()
        return {'signature': signature, 'timestamp': ts}

    async def upload(self, path: str, file: bytes):
        async with self.client.put(self.server, headers=self.sign, params={'path': path, 'site': 'static'},
                                   data={'file': file}) as r:
            assert r.ok, 'upload %s failed %s' % (path, r.status)
            res = await r.json()
            assert res['code'] == 200, 'upload %s failed [%s]' % (path, res['code'])
            return True

    def __call__(self, path: str, file: bytes) -> Awaitable:
        return self.upload(path, file)


async def run():
    upload = Uploader(aiohttp.ClientSession(), os.environ.get('KEY'), os.environ.get('SERVER'))

    tasks: list[tuple[str, bytes]] = []

    for path in Path('translation').glob('*.json'):
        tasks.append((path.as_posix(), path.read_bytes()))

    for path in Path('version').glob('*.txt'):
        tasks.append((f'version/translation/{path.name}', path.read_bytes()))

    for path, content in tasks:
        if await upload(path, content):
            print('upload %s' % path)

    await upload.client.close()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())
