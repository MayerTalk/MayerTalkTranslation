"""
将项目顶端的translation.json拆分为各语言的json
"""

import json
import copy
from pathlib import Path
from collections import OrderedDict

lang_list = ['zh_CN', 'zh_TW', 'en_US', 'ja_JP']
total_data = json.loads(Path('translation.json').read_text(encoding='utf-8'))
empty_split = OrderedDict({k: {} for k in lang_list})


def split(target_data: dict[str, dict]) -> dict[str, dict]:
    split_data: dict[str, ...] = copy.deepcopy(empty_split)
    for k, v in target_data.items():
        for lang, t in (v if 'zh_CN' in v else split(v)).items():
            split_data[lang][k] = t
    return split_data


def write():
    for lang, data in split(total_data).items():
        with (Path('translation') / lang).with_suffix('.json').open(encoding='utf-8', mode='wt') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    write()
