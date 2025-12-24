import streamlit as st
import data
import time

# 1. 頁面基礎設定
st.set_page_config(page_title="AI Nexus | 資源策展平台", page_icon="🧠", layout="wide")

# 2. 注入 CSS 美化 (讓網站變漂亮的魔法)
st.markdown("""
    <style>
    .resource-card {
        background-color: #262730;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #444;
        height: 100%;
        transition: transform 0.3s;
    }
    .resource-card:hover {
        transform: scale(1.02);
        border-color: #ff4b4b;
    }
    .card-img {
        width: 100%;
        height: 150px;
        object-fit: cover;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .card-title {
        font-size: 1.2rem; font-weight: bold; margin-bottom: 5px; color: #fff;
    }
    .card-summary {
        font-size: 0.9rem; color: #ccc; margin-bottom: 15px; height: 60px; overflow: hidden;
    }
    .tag-span {
        background-color: #333; color: #aaa; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem; margin-right: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 載入資料
all_resources = data.get_data()

# 4. 側邊欄
with st.sidebar:
    st.title("🧠 AI Nexus")
    menu = st.radio("前往專區：", ["🏠 首頁 (All)", "🛠️ 工具庫 (Tools)", "📚 學習中心 (Learn Hub)", "🎥 影音專區 (Videos)", "👨‍🏫 專家名錄 (Experts)"])
    st.markdown("---")
    st.subheader("🔍 進階篩選")
    all_tags = sorted(list(set([tag for item in all_resources for tag in item['tags']])))
    selected_tags = st.multiselect("依照標籤過濾：", all_tags)

# 5. 主畫面與搜尋
target_category = menu.split("(")[1].replace(")", "") if "(" in menu else "All"
st.title(f"🚀 {menu}")
search_query = st.text_input("🔎 搜尋資源...", "")

# 6. 過濾邏輯
filtered_data = []
for item in all_resources:
    if target_category != "All" and item['category'] != target_category: continue
    match_search = search_query.lower() in item['title'].lower() or search_query.lower() in item['summary'].lower()
    match_tags = True
    if selected_tags and not set(item['tags']).intersection(set(selected_tags)): match_tags = False
    if match_search and match_tags: filtered_data.append(item)

# 7. 顯示卡片
if not filtered_data:
    st.info("👋 找不到符合條件的資源。")
else:
    cols = st.columns(3)
    for index, item in enumerate(filtered_data):
        with cols[index % 3]:
            tags_html = "".join([f"<span class='tag-span'>#{t}</span>" for t in item['tags']])
            st.markdown(f"""
            <div class="resource-card">
                <img src="{item['image']}" class="card-img">
                <div class="card-title">{item['title']}</div>
                <div class="card-summary">{item['summary']}</div>
                <div style="margin-bottom:10px;">{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)
            st.link_button(f"前往 {item['title']}", item['link'], use_container_width=True)