import time
import streamlit as st
from supabase import create_client
from datetime import datetime
import hunter # 引用爬蟲模組

# --- 1. 定義狩獵任務清單 (SEARCH MISSIONS) ---
# 這裡對應你截圖中的每一個分類 (Explore, Learn, Start Here)
# 機器人會依序執行這些任務，並自動歸類
MISSIONS = [
    # === EXPLORE 區塊 ===
    {"query": "latest cool ai tool demos 2025", "cat": "Explore", "sub": "Demos"},
    {"query": "best midjourney chatgpt prompts guide", "cat": "Explore", "sub": "Prompts"},
    {"query": "top rising ai startups companies 2025", "cat": "Explore", "sub": "Companies"},
    {"query": "ai thought leaders and experts to follow", "cat": "Explore", "sub": "Experts"},

    # === LEARN 區塊 ===
    {"query": "newest open source llm models huggingface", "cat": "Learn", "sub": "Models"},
    {"query": "artificial intelligence terminology glossary", "cat": "Learn", "sub": "Glossary"},
    {"query": "ai safety and ethics news research", "cat": "Learn", "sub": "Ethics"},

    # === START HERE 區塊 ===
    {"query": "ai tools guide for absolute beginners", "cat": "Start Here", "sub": "Beginners"},
    {"query": "best ai apis and libraries for developers", "cat": "Start Here", "sub": "Developers"},
    {"query": "generative ai use cases for business enterprise", "cat": "Start Here", "sub": "Business"},
    {"query": "ai tools for content creators and artists", "cat": "Start Here", "sub": "Creators"},
]

# 每次執行的冷卻時間 (例如 12 小時跑一輪)
INTERVAL = 43200 

# --- 2. 初始化 Supabase ---
try:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase = create_client(url, key)
    print("✅ Bot connected to Supabase.")
except Exception as e:
    print("❌ Connection failed. Check secrets.toml.")
    exit()

def run_bot_cycle():
    print(f"\n🤖 [Auto-Hunter] Mission Start at {datetime.now().strftime('%H:%M:%S')}...")
    
    total_added = 0
    
    # 遍歷每一個任務
    for mission in MISSIONS:
        query = mission["query"]
        target_cat = mission["cat"]
        target_sub = mission["sub"]
        
        print(f"   🎯 Target Locked: [{target_cat}/{target_sub}] Searching: '{query}'...")
        
        # A. 搜尋
        try:
            # 每個分類只抓前 2 個結果，避免資料庫爆炸
            raw_results = hunter.search_web(query, max_results=2)
        except Exception as e:
            print(f"      ⚠️ Search error: {e}")
            continue

        # B. 爬取與過濾
        for res in raw_results:
            link = res['link']
            
            # 去重複檢查
            existing = supabase.table("ai_resources").select("id").eq("link", link).execute()
            if existing.data:
                print(f"      ⏭️  Skipped (Exists): {res['title'][:15]}...")
                continue
            
            # C. 爬取內容
            print(f"      🕷️  Crawling: {link}...")
            data = hunter.crawl_website(link)
            
            if data:
                # D. 寫入資料庫 (使用任務指定的分類)
                new_resource = {
                    "title": data['title'],
                    "link": data['link'],
                    "summary": data['summary'],
                    "image_url": data['image_url'],
                    
                    # 🌟 這裡會自動填入正確的分類！
                    "category": target_cat,
                    "sub_category": target_sub,
                    
                    "country": "Global",
                    "tags": ["auto-hunter", target_sub.lower()],
                    "raw_data": {"source": "bot_v2", "query": query},
                    "created_at": datetime.now().isoformat()
                }
                
                try:
                    supabase.table("ai_resources").insert(new_resource).execute()
                    print(f"      ✅ CAPTURED to [{target_sub}]: {data['title'][:30]}")
                    total_added += 1
                except Exception as e:
                    print(f"      ❌ Insert failed: {e}")
            
            time.sleep(2) # 禮貌性暫停

    print(f"💤 Mission Complete. Added {total_added} new resources. Sleeping for {INTERVAL}s.")

if __name__ == "__main__":
    print("🚀 Cloud AI Hunter Initialized.")
    
    # 雲端版不需要 while True，也不需要 sleep
    # GitHub 會負責每天叫它起床，它只要跑一次就下班
    run_bot_cycle()
    
    print("✅ Mission Complete. Shutting down.")