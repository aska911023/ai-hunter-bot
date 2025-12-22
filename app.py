import streamlit as st
from supabase import create_client
import styles
import components
import admin
import auth

# --- 1. 頁面基礎設定 ---
st.set_page_config(
    page_title="AI.ORG | System",
    page_icon="✴️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. Supabase 資料庫連線 ---
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        return None

def main():
    # --- 3. 載入視覺核心 ---
    st.markdown(styles.get_main_style(), unsafe_allow_html=True)

    # --- 4. 讀取資料 ---
    supabase = init_connection()
    raw_resources = []
    bookmarked_ids = [] # 預設空的收藏清單
    
    if supabase:
        try:
            # A. 抓取所有資源
            response = supabase.table("ai_resources").select("*").order("id").execute()
            raw_resources = response.data

            # B. 抓取收藏清單 (如果有登入)
            if 'user' in st.session_state and st.session_state['user']:
                user_id = st.session_state['user'].id
                # 查詢 bookmarks 表格，只抓 resource_id
                bm_response = supabase.table("bookmarks").select("resource_id").eq("user_id", user_id).execute()
                # 轉成一個簡單的 ID 列表 [1, 5, 8...]
                bookmarked_ids = [item['resource_id'] for item in bm_response.data]

        except Exception as e:
            st.toast(f"⚠️ NETWORK ERROR: {e}", icon="🔌")
    
    # --- 5. 資料適配 ---
    all_resources = []
    for item in raw_resources:
        adapted = item.copy()
        if 'category' in item and 'sub_category' not in item:
            adapted['sub_category'] = item['category']
        if 'image_url' in item and 'image' not in item:
            adapted['image'] = item['image_url']
        all_resources.append(adapted)

    # --- 6. Header & Auth 處理 ---
    main_cat, sub_cat, selected_countries, search_query = components.render_fixed_header(all_resources)

    # 處理彈出視窗
    if st.session_state.get('login_trigger'):
        if supabase: auth.render_auth_modal(supabase)
        st.session_state['login_trigger'] = False
        
    if st.session_state.get('logout_trigger'):
        if supabase: auth.logout(supabase)
        st.session_state['logout_trigger'] = False

    # --- 7. Hero 區塊 ---
    if main_cat == "Explore" and sub_cat == "All" and not search_query:
        components.render_hero()
        components.render_section_header("LATEST CURATIONS")
    else:
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        components.render_section_header(f"{main_cat.upper()} <span style='color:#555'>/</span> {sub_cat.upper()}")

    # --- 8. 顯示使用者資訊 ---
    if 'user' in st.session_state:
        st.caption(f"🟣 NEURAL LINK ACTIVE: {st.session_state['user'].email}")

    # --- 9. 篩選邏輯 ---
    taxonomy = {
        "Start Here": ["Beginners", "Developers", "Business", "Creators"],
        "Explore": ["Demos", "Prompts", "Companies", "Experts"],
        "Learn": ["Models", "Glossary", "Ethics", "FAQ"]
    }

    filtered_data = []
    for item in all_resources:
        item_sub = item.get('sub_category')
        valid_subs = taxonomy.get(main_cat, [])
        is_valid_main = item_sub in valid_subs
        is_valid_sub = (sub_cat == "All") or (sub_cat == item_sub)
        is_valid_country = (not selected_countries) or (item.get('country') in selected_countries)
        
        is_valid_search = True
        if search_query:
            q = search_query.lower()
            text = (item.get('title', '') + item.get('summary', '')).lower()
            tags = item.get('tags', [])
            tag_text = " ".join(tags).lower() if isinstance(tags, list) else ""
            if q not in text and q not in tag_text: is_valid_search = False
        
        if is_valid_main and is_valid_sub and is_valid_country and is_valid_search:
            filtered_data.append(item)

    # --- 10. 渲染結果 (傳入收藏清單) ---
    # 這裡是最重要的改變：我們把 bookmarked_ids 傳進去
    components.render_cards(supabase, filtered_data, bookmarked_ids)

    # --- 11. 頁尾 & Admin ---
    components.render_footer()
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, c_admin, _ = st.columns([10, 1, 10])
    with c_admin:
        if st.button("🔒", key="admin_trigger", help="Admin Access"):
            if supabase: admin.render_admin_modal(supabase)
            else: st.error("Offline")

if __name__ == "__main__":
    main()