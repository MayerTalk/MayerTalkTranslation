# MayerTalkTranslation

[English README](README.EN.md)

[MayerTalk](https://github.com/MayerTalk/MayerTalk) 翻译文本

目前，翻译文本由AI翻译提供，欢迎通过pr提交更准确的翻译文本

翻译请提交至[translation.json](translation.json)，其他文件会自动同步

## 目录说明

```text
.
├─.github
│  ├─scripts                # scripts for action
│  └─workflows              # github action
├─scripts
│  ├─generate_empty.py      # 生成emptyTranslation.js，供MayerTalk使用
│  └─server.py              # 本地调试服务端，配合src/lib/dev.js使用
├─translation           # 聚合后的翻译
├─version               # 翻译数据版本
└─translation.json      # 全部翻译
```