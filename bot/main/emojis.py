import json

with open('./data/emojis.json', 'r', encoding='utf-8') as f:
    emojis = json.load(f)

class _Emoji(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __repr__(self):
        return "<Emoji "+ dict.__repr__(self)+">"

Emoji = _Emoji(emojis)