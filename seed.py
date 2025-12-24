import streamlit as st
from supabase import create_client

# 1. 設定頁面 (為了讀取 secrets，我們還是用 streamlit 來執行它)
st.set_page_config(page_title="資料快速匯入工具")
st.title("🌱 AI.ORG 資料快速播種 (Seeding)")

# 2. 連線 Supabase
try:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase = create_client(url, key)
    st.success("✅ Supabase 連線成功！")
except Exception as e:
    st.error(f"❌ 連線失敗，請檢查 secrets.toml: {e}")
    st.stop()

# 3. 準備好的 5 筆資料 (List of Dictionaries)
resources_to_add = [
    {
        "title": "ChatGPT (OpenAI)",
        "summary": "全球最受歡迎的 AI 聊天機器人，由 OpenAI 開發。能處理寫作、翻譯、程式碼撰寫與創意發想等多種任務。",
        "link": "https://chat.openai.com",
        "image_url": "https://images.unsplash.com/photo-1675271591211-126ad94e495d?auto=format&fit=crop&w=800&q=80",
        "category": "Start Here",
        "category": "Beginners",  # 注意：如果您的 DB 欄位是 sub_category，請自行修改 Key 名稱
        "country": "USA",
        "tags": ["chatbot", "llm", "free", "openai"],
        "is_verified": True
    },
    {
        "title": "Claude 3.5 Sonnet",
        "summary": "由 Anthropic 開發的強大模型，以自然流暢的寫作風格與強大的程式碼撰寫能力著稱，上下文視窗極大。",
        "link": "https://claude.ai",
        "image_url": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=800&q=80",
        "category": "Explore",
        "category": "Experts",
        "country": "USA",
        "tags": ["coding", "writing", "anthropic"],
        "is_verified": True
    },
    {
        "title": "Leonardo.ai",
        "summary": "專為遊戲資產與藝術設計打造的 AI 繪圖工具，介面友善，能生成極高品質的角色與場景圖片。",
        "link": "https://leonardo.ai",
        "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80",
        "category": "Explore",
        "category": "Demos",
        "country": "Other",
        "tags": ["image-gen", "art", "game-design"],
        "is_verified": True
    },
    {
        "title": "GitHub Copilot",
        "summary": "你的 AI 結對程式設計師。直接整合在 VS Code 中，協助你自動補全程式碼、寫註解與除錯。",
        "link": "https://github.com/features/copilot",
        "image_url": "https://images.unsplash.com/photo-1555099962-4199c345e5dd?auto=format&fit=crop&w=800&q=80",
        "category": "Start Here",
        "category": "Developers",
        "country": "USA",
        "tags": ["coding", "productivity", "microsoft"],
        "is_verified": True
    },
    {
        "title": "Perplexity AI",
        "summary": "結合了搜尋引擎與 LLM 的優勢，能提供附帶引用來源的即時答案，是替代傳統 Google 搜尋的最佳工具。",
        "link": "https://www.perplexity.ai",
        "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80",
        "category": "Learn",
        "category": "Models",
        "country": "USA",
        "tags": ["search", "research", "citation"],
        "is_verified": True
    }
]

# 4. 執行批次寫入
if st.button("🚀 開始批次匯入 (Bulk Insert)"):
    st.write(f"正在準備匯入 {len(resources_to_add)} 筆資料...")
    
    success_count = 0
    for item in resources_to_add:
        try:
            # 這裡要注意：如果您的 DB 用的是 sub_category 欄位，請將上面字典裡的 Key 改對應
            # 為了保險起見，我們動態調整一下 Key (假設您的 DB 欄位叫 category，存放子分類內容)
            # 如果您的 DB 結構是 category(主) + sub_category(子)，請確保字典 Key 正確
            
            # 執行寫入
            supabase.table("ai_resources").insert(item).execute()
            st.write(f"✅ 成功寫入: {item['title']}")
            success_count += 1
        except Exception as e:
            st.error(f"❌ 寫入失敗 ({item['title']}): {e}")
    
    if success_count == len(resources_to_add):
        st.balloons()
        st.success("🎉 太棒了！全部資料已成功匯入資料庫！")
        st.info("現在請去執行 `app.py` 看看首頁吧！")