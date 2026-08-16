import re
from pathlib import Path

def parse_list(path):
    followings = {}
    text = Path(path).read_text(encoding='utf-8')
    for line in text.splitlines():
        match = re.search(r'^\d+\.\s*(.+?)\s+-\s+https://space\.bilibili\.com/(\d+)', line)
        if match:
            name, uid = match.groups()
            followings[uid] = name.strip()
    return followings

beginning = parse_list('BeginningAll_bilibili_followingsList_New.txt')
wally = parse_list('WallyVibe_bilibili_followings_List_New.txt')

only_in_beginning = {uid: name for uid, name in beginning.items() if uid not in wally}

print(f"BeginningAll 共关注: {len(beginning)}")
print(f"WallyVibe 共关注: {len(wally)}")
print(f"仅在 BeginningAll 中: {len(only_in_beginning)}")
print()
for i, (uid, name) in enumerate(only_in_beginning.items(), 1):
    print(f"{i}. {name} - https://space.bilibili.com/{uid}")
