import json
from collections import Counter

with open('/Users/wangx/我的/github/vscode/shuimo-theme/themes/shuimo-shijie-theme.json', 'r') as f:
    data = json.load(f)

colors = []

def extract_colors(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            extract_colors(v)
    elif isinstance(obj, str) and obj.startswith('#'):
        colors.append(obj)

extract_colors(data)

c = Counter(colors)
for color, count in c.most_common(30):
    print(f"{color}: {count}")
