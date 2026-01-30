import requests
import os

# 配置
UID = "1671203508"  # 洪洪火火复盘的UID
FEISHU_URL = os.environ.get("FEISHU_URL") # 自动读取你刚才复制的那个地址

def get_latest_comments():
    try:
        # 获取最新视频
        video_api = f"https://api.bilibili.com/x/space/wbi/arc/search?mid={UID}&ps=5"
        v_data = requests.get(video_api).json()
        videos = v_data['data']['list']['vlist']
        
        for v in videos:
            aid = v['aid']
            # 获取评论
            reply_api = f"https://api.bilibili.com/x/v2/reply?type=1&oid={aid}&sort=0"
            r_data = requests.get(reply_api).json()
            replies = r_data.get('data', {}).get('replies', [])
            
            if not replies: continue
            
            for r in replies:
                # 如果是UP主本人发的
                if str(r['mid']) == UID:
                    content = r['content']['message']
                    # 发送给飞书
                    msg = {
                        "msg_type": "text",
                        "content": {"text": f"📢 洪洪火火复盘出新评论了！\n\n内容：{content}\n\n链接：https://www.bilibili.com/video/{v['bvid']}"}
                    }
                    requests.post(FEISHU_URL, json=msg)
                    return # 每次只报最新的
    except Exception as e:
        print(f"检查出错: {e}")

if __name__ == "__main__":
    get_latest_comments()
