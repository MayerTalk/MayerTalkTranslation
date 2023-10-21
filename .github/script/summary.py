import json
from pathlib import Path

prefix = '# 总览  \n  \n'

translation_fmt = '`%s` %s  \n'

total_data: dict[str, dict] = {}
lang_seq: list[str] = []

for path in Path('translation').glob('*.json'):
    lang_seq.append(path.stem)
    total_data[path.stem] = json.loads(path.read_text('utf-8'))

lang_seq.sort()
lang_seq.remove('zh_CN')
lang_seq.insert(0, 'zh_CN')


def get_part(model_data: dict | list, full_data: dict[str, dict] | dict[str, list], root: str = '') -> (
        tuple)[str, tuple[tuple[str, str]]]:
    for k, v in (model_data.items() if isinstance(model_data, dict) else enumerate(model_data)):
        if isinstance(v, str):
            yield f'{root}{k}', tuple((lang, full_data[lang][k]) for lang in lang_seq)
        else:
            yield from get_part(model_data[k], {lang: data[k] for lang, data in full_data.items()}, f'{root}{k}.')


with open('summary.md', mode='wt', encoding='utf-8') as f:
    f.write(prefix)
    for item, translations in get_part(total_data['zh_CN'], total_data):
        f.write(f'### {item}  \n')
        for translation in translations:
            f.write(translation_fmt % translation)
        f.write('  \n')
