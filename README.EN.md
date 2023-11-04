# MayerTalkTranslation

MayerTalk translation text

Currently, the translation text is provided by AI translation, and you are welcome to submit more accurate translation text through pr

Please submit the translation to [translation.json](translation.json), and other files will be automatically synchronized

## Directory description

```text
.
├─.github
│  ├─scripts                # scripts for action
│  └─workflows              # github action
├─scripts
│  ├─generate_empty.py      # generate emptyTranslation.js for MayerTalk use
│  └─server.py              # local debug server, used with src/lib/dev.js
├─translation           # aggregated translation
├─version               # translation data version
└─translation.json      # all translation
```