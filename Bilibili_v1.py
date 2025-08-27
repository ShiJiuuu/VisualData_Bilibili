import requests
import pandas as pd
import time
import random
import os

# 设置 UA
headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/122.0.0.0 Safari/537.36'),
    'Referer': 'https://www.bilibili.com',
    'Accept': 'application/json, text/plain, */*'
}

# 视频爬取函数
def crawl_bilibili_videos(keyword, pages=3):
    base_url = "https://api.bilibili.com/x/web-interface/search/type"
    results = []

    for page in range(1, pages + 1):
        params = {
            'search_type': 'video',
            'keyword': keyword,
            'page': page
        }

        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=10)
            data = response.json()

            if 'data' not in data or 'result' not in data['data']:
                print(f"[!] 数据为空或被限速，关键词：{keyword} 第{page}页")
                continue

            for item in data['data']['result']:
                results.append({
                    'title': item['title'],
                    'author': item['author'],
                    'view': item.get('play', '0'),
                    'danmaku': item.get('video_review', '0'),
                    'description': item.get('description', ''),
                    'pubdate': item.get('pubdate', ''),
                    'type': item.get('typename', ''),
                    'arcurl': item['arcurl']
                })

            print(f"[+] 成功爬取 {keyword} 第{page}页")
            time.sleep(random.uniform(1.5, 3.5))  # 防止被限速
        except Exception as e:
            print(f"[-] 错误：{e}，关键词：{keyword} 第{page}页")
            continue

    return pd.DataFrame(results)

# 多关键词批量爬取
keywords = ['游戏', '知识', '娱乐', '美食', '音乐']  # 可自定义关键词
save_dir = 'bilibili_data'
os.makedirs(save_dir, exist_ok=True)

for kw in keywords:
    df = crawl_bilibili_videos(kw, pages=20)  # 每个关键词爬5页
    save_path = os.path.join(save_dir, f'{kw}.csv')
    df.to_csv(save_path, index=False)
    print(f"[!] 已保存 {kw}.csv，共 {len(df)} 条数据")
    time.sleep(random.uniform(2.5, 4.5))  # 每类间歇防止封IP

print("\n[!] 所有关键词爬取完成！数据保存在 bilibili_data 文件夹。")