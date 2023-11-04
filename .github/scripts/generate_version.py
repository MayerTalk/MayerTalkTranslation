"""
生成供缓存检查的version文件
"""

import json
from pathlib import Path
from hashlib import md5


def sort_data(data: dict[str, ...] | list[str] | str):
    if isinstance(data, dict):
        return {k: sort_data(v) for k, v in sorted(data.items(), key=lambda x: x[0])}
    else:
        return data


for path in Path('translation').glob('*.json'):
    translation = json.loads(path.read_text('utf-8'))

    translation_hash = md5(json.dumps(translation).encode('utf-8')).hexdigest()

    Path('version', *path.parts[1:]).with_suffix('.txt').write_text(translation_hash)
