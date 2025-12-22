import streamlit as st
from datetime import datetime
import hunter # 引用我們剛剛寫的爬蟲模組

@st.dialog("/// 系統控制台 (COMMAND CENTER)_")
def render_admin_modal(supabase):
    st.markdown("""
        <style>
        div[data-testid="stDialog"] {
            background-color: #0d0d16;
            border: 1px solid #00F0FF;
            box-shadow: 0 0 50px rgba(0, 240, 255, 0.2);
            color: #ddd;
        }
        input, textarea {
            background-color: #1a1a24 !important;
            color: white !important;
            border: 1px solid #333 !important;
        }
        .hunter-card {
            border: 1px solid #333; padding: 10px; margin-bottom: 10px; border-radius: 8px; background: #111;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. 安全驗證 ---
    try:
        ADMIN_PASSWORD = st.secrets["admin"]["password"]
    except:
        ADMIN_PASSWORD = "admin123"

    if 'is_admin_logged_in' not in st.session_state:
        st.session_state['is_admin_logged_in'] = False

    if not st.session_state['is_admin_logged_in']:
        pwd = st.text_input("ACCESS CODE", type="password")
        if st.button("AUTHENTICATE"):
            if pwd == ADMIN_PASSWORD:
                st.session_state['is_admin_logged_in'] = True
                st.rerun()
            return

    # --- 2. 控制台主畫面 ---
    st.success("ACCESS GRANTED.")
    
    # 🌟 分頁切換：手動輸入 vs AI 獵人
    tab1, tab2 = st.tabs(["✍️ 手動輸入 (Manual)", "🤖 AI 獵人 (Auto-Hunter)"])

    # === TAB 1: 手動輸入 (原本的功能) ===
    with tab1:
        with st.form("add_resource_form", clear_on_submit=True):
            st.caption("MANUAL INJECTION")
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title")
                main_cat = st.selectbox("Main Category", ["Explore", "Learn", "Start Here"])
                country = st.selectbox("Region", ["Global", "USA", "Taiwan", "China", "Japan"])
            with col2:
                sub_cat = st.selectbox("Sub Category", ["Demos", "Prompts", "Companies", "Experts", "Models", "Glossary", "Ethics", "Beginners", "Developers", "Business", "Creators"])
                link = st.text_input("Link")
                image_url = st.text_input("Image URL")

            summary = st.text_area("Summary", max_chars=200)
            tags = st.text_input("Tags (comma separated)")
            content = st.text_area("Markdown Content")

            if st.form_submit_button("🚀 INJECT"):
                if not title:
                    st.error("Title required")
                else:
                    new_data = {
                        "title": title, "link": link if link else "#", "summary": summary,
                        "content": content, "image_url": image_url, "country": country,
                        "category": main_cat, "sub_category": sub_cat,
                        "tags": [t.strip() for t in tags.split(",") if t.strip()],
                        "raw_data": {"source": "manual", "editor": "admin"},
                        "created_at": datetime.now().isoformat()
                    }
                    supabase.table("ai_resources").insert(new_data).execute()
                    st.toast("Saved!", icon="💾")

    # === TAB 2: AI 獵人模式 (新功能) ===
    with tab2:
        st.caption("SEARCH & CRAWL PIPELINE")
        
        # 1. 搜尋設定
        c1, c2 = st.columns([3, 1])
        with c1:
            search_query = st.text_input("搜尋關鍵字 (Search Query)", placeholder="例如: 2025 Best AI Video Generators")
        with c2:
            max_results = st.number_input("數量", min_value=1, max_value=5, value=3)

        if st.button("🔍 開始狩獵 (Start Hunt)"):
            with st.status("正在執行 AI 搜索流程...", expanded=True) as status:
                
                # A. SERP 階段
                st.write("📡 連接 SERP 衛星搜索中...")
                raw_results = hunter.search_web(search_query, max_results)
                
                # B. Crawler 階段
                st.write("🕷️ 派出爬蟲抓取 metadata...")
                crawled_data = []
                progress_bar = st.progress(0)
                
                for i, res in enumerate(raw_results):
                    data = hunter.crawl_website(res['link'])
                    if data:
                        crawled_data.append(data)
                    progress_bar.progress((i + 1) / len(raw_results))
                
                # 存入 Session State 供預覽
                st.session_state['hunt_results'] = crawled_data
                status.update(label="✅ 狩獵完成！", state="complete", expanded=False)

        # 2. 顯示搜尋結果並允許一鍵加入
        if 'hunt_results' in st.session_state and st.session_state['hunt_results']:
            st.divider()
            st.caption(f"FOUND {len(st.session_state['hunt_results'])} TARGETS")
            
            for idx, item in enumerate(st.session_state['hunt_results']):
                with st.container():
                    st.markdown(f"""
                    <div class="hunter-card">
                        <div style="color:#00F0FF;font-weight:bold;">{item['title']}</div>
                        <div style="font-size:0.8rem;color:#888;">{item['link']}</div>
                        <div style="font-size:0.9rem;color:#ccc;margin-top:5px;">{item['summary']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 每個結果都有自己的 "加入" 按鈕
                    c_add, c_cat = st.columns([1, 2])
                    with c_cat:
                        # 讓管理員快速選分類
                        target_cat = st.selectbox("分類", ["Demos", "Companies", "Models"], key=f"cat_{idx}")
                    with c_add:
                        if st.button("➕ 加入資料庫", key=f"add_{idx}"):
                            new_data = {
                                "title": item['title'],
                                "link": item['link'],
                                "summary": item['summary'],
                                "image_url": item['image_url'],
                                "category": "Explore", # 預設主分類
                                "sub_category": target_cat,
                                "country": "Global",
                                "tags": ["auto-crawled"],
                                "raw_data": {"source": "ai_hunter", "query": search_query},
                                "created_at": datetime.now().isoformat()
                            }
                            try:
                                supabase.table("ai_resources").insert(new_data).execute()
                                st.toast(f"Captured: {item['title']}", icon="🕸️")
                            except Exception as e:
                                st.error(f"Error: {e}")

    if st.button("LOGOUT"):
        st.session_state['is_admin_logged_in'] = False
        st.rerun()