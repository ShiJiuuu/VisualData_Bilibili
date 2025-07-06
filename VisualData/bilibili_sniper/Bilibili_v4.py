import requests
import csv
import time
import random

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com/',
    'Cookie': "_uuid=DA6289104-4AED-D6B8-9F39-510102B61BF7D531364infoc; SESSDATA=9601659c%2C1757173810%2C2bdee%2A32CjDNrJSobl5jcfy9ARW_TFD35GMaHma7mybQEqGrfEjtgu_6lLagkUpDzb4gs2hG_MUSVnhWU0RXQ25nekdGMmNpanNZN0VMVFRQMklBNENjMTItcUFWTTF1UWgwcGpfVkdLYktsZGpkU2dSM1FmNWdDajhybWlTbFY0MUdqbGYxUXhObWptblZnIIEC; bili_jct=61fc6ede8bc31cf0914d72a4c1abd0f7; DedeUserID=417084428",
    'Origin': 'https://www.bilibili.com',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site'
}

def search_videos(keyword, max_pages=20):
    all_results = []
    for page in range(1, max_pages + 1):
        url = "https://api.bilibili.com/x/web-interface/search/type"
        params = {
            "search_type": "video",
            "keyword": keyword,
            "page": page
        }
        try:
            res = requests.get(url, headers=HEADERS, params=params, timeout=30)
            res.raise_for_status()
            data = res.json()

            videos = data.get('data', {}).get('result', [])
            if not videos:
                print(f"[!] 第 {page} 页无结果，提前结束")
                break

            for v in videos:
                all_results.append({
                    "标题": v.get("title", "").replace("<em class=\"keyword\">", "").replace("</em>", ""),
                    "UP主": v.get("author"),
                    "播放数": v.get("play"),
                    "弹幕数": v.get("video_review"),
                    "评论数": v.get("review"),
                    "时长": v.get("duration"),
                    "发布时间": v.get("pubdate"),
                    "BV号": v.get("bvid"),
                    "链接": f"https://www.bilibili.com/video/{v.get('bvid')}"
                })

            print(f"[√] 第 {page} 页获取成功，共 {len(videos)} 条")
            time.sleep(1)  # 防止被ban

        except Exception as e:
            print(f"[×] 第 {page} 页出错：{e}")
            continue

    return all_results


def save_to_csv(data, filename):
    if not data:
        print("无数据可保存")
        return
    keys = data[0].keys()
    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"[√] 已保存到 {filename}，共 {len(data)} 条")

if __name__ == "__main__":
    keywords = ["动画", "音乐", "游戏", "生活", "知识", "Vlog", "娱乐", "鬼畜", "科普", "电影", "纪录片", "舞蹈"]
    for kw in keywords:
        print(f"\n=== 正在爬取关键词：{kw} ===")
        results = search_videos(keyword=kw, max_pages=20)  # 每个关键词爬10页（约200条）
        save_to_csv(results, f"{kw}_search.csv")