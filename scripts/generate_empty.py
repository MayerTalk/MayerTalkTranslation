"""
生成emptyTranslation.js 供MayerTalk使用 (https://github.com/MayerTalk/MayerTalk/blob/main/src/lib/lang/emptyTranslation.js)
"""

import re
import json
from pathlib import Path
from collections import OrderedDict

total_data = json.loads(Path('../translation.json').read_text(encoding='utf-8'))


def split(target_data: dict[str, dict]) -> OrderedDict[str, ...]:
    split_data: OrderedDict[str, ...] = OrderedDict()
    for k, v in target_data.items():
        if 'zh_CN' in v:
            split_data[k] = '' if isinstance(v['zh_CN'], str) else ['']
        else:
            split_data[k] = split(v)
    return split_data


data = OrderedDict(empty=True)
data.update(split(total_data))
data = json.dumps(data, ensure_ascii=False, indent=4)
data = re.sub(r'"(.+)":', r'\1:', data).replace('"', '\'')

template = """const emptyTranslation = %s

export default emptyTranslation
"""

with open('emptyTranslation.js', mode='wt', encoding='utf-8') as f:
    f.write(template % data)
