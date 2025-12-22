import time
import streamlit as st # 借用 streamlit 的 secrets 读取功能
from supabase import create_client
from datetime import datetime
import hunter # 引用我們寫好的爬蟲模組

# --- 1. 設定機器人參數 ---
# 你希望它搜尋什麼關鍵字？
TARGET_KEYWORDS = [
    "best new ai tools 2025",
    "latest generative ai startups",
    "free ai coding assistants",
    "new text to video ai models"
]

# 你希望它多久跑一次？ (單位：秒)
# 建議設定 24 小時 (86400秒) 或 12 小時 (43200秒)
# 測試時可以設短一點，例如 60 秒
INTERVAL = 43200 

# --- 2. 初始化 Supabase ---
# 為了讓這個腳本能獨立運作，我們需要這裡也連線一次
try:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase = create_client(url, key)
    print("✅ Bot connected to Supabase.")
except Exception as e:
    print("❌ Bot failed to connect. Check secrets.toml.")
    exit()

def run_bot_cycle():
    print(f"\n🤖 [Auto-Hunter] Waking up at {datetime.now().strftime('%H:%M:%S')}...")
    
    total_added = 0
    
    for query in TARGET_KEYWORDS:
        print(f"   🔎 Scouting sector: '{query}'...")
        
        # A. 搜尋 (SERP)
        try:
            # 每次關鍵字只找前 3 個結果，避免太貪心被封鎖
            raw_results = hunter.search_web(query, max_results=3)
        except Exception as e:
            print(f"      ⚠️ Search error: {e}")
            continue

        # B. 爬取與過濾 (Crawl & Filter)
        for res in raw_results:
            link = res['link']
            
            # [重要] 檢查是否已存在資料庫 (去重複)
            # 我們去資料庫查一下這個 link 是否已經有了
            existing = supabase.table("ai_resources").select("id").eq("link", link).execute()
            
            if existing.data:
                print(f"      ⏭️  Skipping (Already exists): {res['title'][:20]}...")
                continue
            
            # C. 爬取詳細資料
            print(f"      🕷️  Crawling new target: {link}...")
            data = hunter.crawl_website(link)
            
            if data:
                # D. 寫入資料庫
                new_resource = {
                    "title": data['title'],
                    "link": data['link'],
                    "summary": data['summary'],
                    "image_url": data['image_url'],
                    "category": "Explore",     # 機器人抓的一律先丟 Explore
                    "sub_category": "Demos",   # 或新建一個 "Auto-Crawled" 分類
                    "country": "Global",
                    "tags": ["bot-hunter", "auto"],
                    "raw_data": {"source": "bot_v1", "query": query},
                    "created_at": datetime.now().isoformat()
                }
                
                try:
                    supabase.table("ai_resources").insert(new_resource).execute()
                    print(f"      ✅ CAPTURED: {data['title']}")
                    total_added += 1
                except Exception as e:
                    print(f"      ❌ Insert failed: {e}")
            
            # 休息一下，當個有禮貌的機器人
            time.sleep(2)

    print(f"💤 Cycle finished. Added {total_added} new resources. Sleeping for {INTERVAL}s.")

# --- 3. 主循環 (Main Loop) ---
if __name__ == "__main__":
    print("🚀 AI Hunter Bot initialized. Press Ctrl+C to stop.")
    
    while True:
        run_bot_cycle()
        time.sleep(INTERVAL)