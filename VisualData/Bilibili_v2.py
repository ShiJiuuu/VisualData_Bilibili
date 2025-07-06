import requests
import pandas as pd
import time
import os

headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/122.0.0.0 Safari/537.36'),
    'Referer': 'https://www.bilibili.com'
}

# 分类名与rid的映射（官方）
type_map = {
    1: "动画",
    3: "音乐",
    4: "游戏",
    5: "娱乐",
    36: "知识",
    160: "生活",
    119: "鬼畜",
    129: "舞蹈"
}

def get_ranking_videos(rid):
    url = f"https://api.bilibili.com/x/web-interface/ranking/v2"
    params = {'rid': rid, 'type': 'all'}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        result = []
        for item in data['data']['list']:
            stat = item.get('stat', {})
            result.append({
                'title': item['title'],
                'author': item['owner']['name'],
                'type': type_map.get(rid, str(rid)),
                'view': stat.get('view', 0),
                'like': stat.get('like', 0),
                'coin': stat.get('coin', 0),
                'favorite': stat.get('favorite', 0),
                'share': stat.get('share', 0),
                'danmaku': stat.get('danmaku', 0),
                'pubdate': item.get('pubdate', ''),
                'bvid': item.get('bvid', ''),
                'arcurl': f"https://www.bilibili.com/video/{item['bvid']}"
            })

        return pd.DataFrame(result)

    except Exception as e:
        print(f"[-] 获取 rid={rid} 失败：{e}")
        return pd.DataFrame()

# 多分类爬取
save_dir = "bilibili_rank_data"
os.makedirs(save_dir, exist_ok=True)

for rid in type_map.keys():
    df = get_ranking_videos(rid)
    df.to_csv(os.path.join(save_dir, f"{type_map[rid]}.csv"), index=False)
    print(f"[!] 已保存 {type_map[rid]}.csv，{len(df)} 条")
    time.sleep(30)

print("\n[!] 所有排行榜数据获取完成！")