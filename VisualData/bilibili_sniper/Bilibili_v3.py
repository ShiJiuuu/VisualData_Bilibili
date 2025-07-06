import requests
import pandas as pd
import time
import os

HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/122.0.0.0 Safari/537.36'),
    'Referer': 'https://www.bilibili.com/',
    'Origin': 'https://www.bilibili.com',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site'
}

# 保存目录
SAVE_DIR = "bilibili_data"
os.makedirs(SAVE_DIR, exist_ok=True)

TYPE_MAP = {
    1: "动画", 3: "音乐", 4: "游戏", 5: "娱乐",
    36: "知识", 160: "生活", 119: "鬼畜", 129: "舞蹈"
}
def get_rank_videos():
    print("\n[!] 正在获取排行榜数据...")
    all_dfs = []

    for rid, typename in TYPE_MAP.items():
        url = "https://api.bilibili.com/x/web-interface/ranking/v2"
        params = {'rid': rid, 'type': 'all'}

        try:
            res = requests.get(url, headers=HEADERS, params=params, timeout=30)

            #Dubugging for Empty Data
            print(f"[调试] rid={rid} 状态码：{res.status_code}")
            #print(f"[调试] 内容摘要（前500字符）：\n{res.text[:500]}\n")

            res.raise_for_status()
            data = res.json()

            if 'data' not in data or 'list' not in data['data']:
                print(f"[-] 分类【{typename}】数据为空")
                continue

            result = []
            for item in data['data']['list']:
                stat = item.get('stat', {})
                result.append({
                    'title': item['title'],
                    'author': item['owner']['name'],
                    'type': typename,
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

            df = pd.DataFrame(result)
            df.to_csv(os.path.join(SAVE_DIR, f"rank_{typename}.csv"), index=False)
            all_dfs.append(df)
            print(f"[+] 分类【{typename}】完成，{len(df)} 条")
            time.sleep(1)

        except Exception as e:
            print(f"[-] 分类【{typename}】失败：{e}")

    # 合并所有排行榜数据
    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df.to_csv(os.path.join(SAVE_DIR, "rank_all.csv"), index=False)
    print(f"\n[!] 排行榜总计 {len(final_df)} 条，已保存为 rank_all.csv")
    return final_df

def get_rcmd_videos(pages=100):
    print("\n[+] 正在获取推荐流视频（分页）...")
    result = []

    for page in range(1, pages + 1):
        url = "https://api.bilibili.com/x/web-interface/wbi/index/top/feed/rcmd"
        params = {
            'ps': 20,
            'pn': page,
            'fresh_type': 4,
            'feed_version': 'V2',
            'platform': 'web'
        }

        try:
            res = requests.get(url, headers=HEADERS, params=params, timeout=30)
            data = res.json()

            if data['code'] != 0:
                print(f"[-] 第 {page} 页请求失败，code={data['code']}")
                continue

            for item in data['data']['item']:
                stat = item.get('stat', {})
                result.append({
                    'title': item['title'],
                    'author': item['owner']['name'],
                    'view': stat.get('view', 0),
                    'like': stat.get('like', 0),
                    'coin': stat.get('coin', 0),
                    'favorite': stat.get('favorite', 0),
                    'danmaku': stat.get('danmaku', 0),
                    'pubdate': item.get('pubdate', ''),
                    'bvid': item.get('bvid', ''),
                    'arcurl': f"https://www.bilibili.com/video/{item['bvid']}"
                })

            print(f"[+] 第 {page} 页成功，累计：{len(result)} 条")
            time.sleep(1)

        except Exception as e:
            print(f"[-] 第 {page} 页失败：{e}")
            continue

    df = pd.DataFrame(result)
    df.to_csv(os.path.join(SAVE_DIR, "rcmd_all.csv"), index=False)
    print(f"\n[!] 推荐流共采集 {len(df)} 条，已保存为 rcmd_all.csv")
    return df

if __name__ == "__main__":
    #rank_df = get_rank_videos()
    rank_df = 0
    rcmd_df = get_rcmd_videos(pages=100)

    print(f"\n[!] 数据采集完成，共采集：{len(rank_df) + len(rcmd_df)} 条视频信息")
    print(f"[!] 所有文件保存在：{SAVE_DIR}/")