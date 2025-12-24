import streamlit as st

def render_fixed_header(all_resources):
    """
    渲染頂部導覽列
    """
    params = st.query_params
    current_main = params.get("main_cat", "Explore")
    current_sub = params.get("sub_cat", "All")

    menu_structure = {
        "EXPLORE": {
            "id": "Explore", "caption": "SYSTEM MODE",
            "desc": "Discover demos, prompts & AI companies.",
            "subs": ["Demos", "Prompts", "Companies", "Experts"]
        },
        "LEARN": {
            "id": "Learn", "caption": "DATABASE",
            "desc": "Access models, research papers & ethics.",
            "subs": ["Models", "Glossary", "Ethics"]
        },
        "START": {
            "id": "Start Here", "caption": "PLAYER CLASS",
            "desc": "Find your path: Beginner to Creator.",
            "subs": ["Beginners", "Developers", "Business", "Creators"]
        }
    }

    nav_html = '<div class="nav-menu-container">'
    for label, info in menu_structure.items():
        # 使用括號串接法 (防呆)
        sub_links = (
            f'<a href="?main_cat={info["id"]}&sub_cat=All" target="_self" class="sub-link" '
            'style="border:1px solid var(--neon-cyan); color:#fff;">View All</a>'
        )
        for sub in info['subs']:
            sub_links += f'<a href="?main_cat={info["id"]}&sub_cat={sub}" target="_self" class="sub-link">{sub}</a>'
        
        active_style = 'color:var(--neon-cyan); border-color:rgba(0,240,255,0.5);' if current_main == info['id'] else ''

        nav_html += (
            f'<div class="nav-item">'
            f'<div class="nav-link" style="{active_style}">{label} ▾</div>'
            f'<div class="nav-dropdown">'
            f'<div class="nav-dropdown-box">'
            f'<div class="dropdown-caption">{info["caption"]}</div>'
            f'<div class="dropdown-desc">{info["desc"]}</div>'
            f'<div class="sub-links-box">{sub_links}</div>'
            f'</div></div></div>'
        )
    nav_html += "</div>"

    st.markdown('<div class="nav-container-wrapper" style="margin-bottom: 20px;">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2.5, 5.0, 2.5], gap="small")
    
    with c1:
        st.markdown((
            '<a href="?" target="_self" style="text-decoration:none;">'
            '<div style="font-family: \'Orbitron\'; font-size: 3.8rem; font-weight: 900; '
            'line-height: 1; letter-spacing: -3px; cursor: pointer; padding-top: 5px;'
            'background: linear-gradient(90deg, #00F0FF, #BC13FE, #00F0FF);'
            'background-size: 200%; -webkit-background-clip: text; -webkit-text-fill-color: transparent;'
            'filter: drop-shadow(0 0 10px rgba(0, 240, 255, 0.3));'
            'animation: text-rgb 3s linear infinite;">AI.ORG</div></a>'
        ), unsafe_allow_html=True)
        
    with c2:
        clean_html = nav_html.replace("\n", "").replace("    ", "")
        st.markdown(clean_html, unsafe_allow_html=True)
        
    with c3:
        r1, r2, r3 = st.columns([2.5, 0.8, 1.2], gap="small")
        with r1:
            # 🌟 [修復點 1] 這裡要把輸入值存回 search_query
            search_query = st.text_input("Search", placeholder="SEARCH...", label_visibility="collapsed")
        with r2:
            with st.popover("🌍", use_container_width=True):
                st.caption("SERVER REGION")
                countries = ["🌍 Global", "🇺🇸 USA", "🇹🇼 Taiwan", "🇨🇳 China", "🇯🇵 Japan", "🇪🇺 Europe"]
                # 🌟 [修復點 2] 這裡要把選單值存回 sel_c 並處理成 cleaned_c
                sel_c = st.multiselect("Region", countries, default=[], label_visibility="collapsed")
                cleaned_c = [c.split(" ")[1] for c in sel_c] if sel_c else []
        with r3:
            if 'user' in st.session_state and st.session_state['user']:
                if st.button("LOGOUT", key="header_logout"):
                    st.session_state['logout_trigger'] = True
            else:
                st.markdown((
                    '<style>'
                    'div[data-testid="stButton"] button {'
                    'border: 1px solid #BC13FE !important; color: #BC13FE !important;'
                    'border-radius: 20px !important; padding: 0px 10px !important;}'
                    'div[data-testid="stButton"] button:hover {'
                    'background: rgba(188, 19, 254, 0.2) !important; box-shadow: 0 0 10px #BC13FE !important;'
                    'color: white !important;}'
                    '</style>'
                ), unsafe_allow_html=True)
                if st.button("LOGIN", key="header_login"):
                    st.session_state['login_trigger'] = True
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 🌟 [修復點 3] 補回原本遺失的 return，這是最關鍵的一行！
    return current_main, current_sub, cleaned_c, search_query

# --- KNOWLEDGE BASE READER ---
@st.dialog("/// KNOWLEDGE_BASE_READER")
def show_reader(item):
    st.markdown((
        '<style>'
        'div[data-testid="stDialog"] {background-color: #0B0C15; border: 1px solid #00F0FF; width: 80vw !important; max-width: 1000px;}'
        '.reader-title {font-family: \'Orbitron\'; font-size: 2rem; color: #fff; margin-bottom: 10px;}'
        '.reader-meta {color: #BC13FE; font-family: \'Rajdhani\'; font-size: 0.9rem; margin-bottom: 30px; border-bottom: 1px solid #333; padding-bottom: 10px;}'
        '</style>'
    ), unsafe_allow_html=True)
    
    st.markdown(f"<div class='reader-title'>{item['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='reader-meta'>CATEGORY: {item.get('sub_category', 'GENERAL')} // REGION: {item.get('country', 'GLOBAL')}</div>", unsafe_allow_html=True)
    
    fallback_img = "https://placehold.co/800x500/050508/00F0FF?text=NO+SIGNAL"
    img_url = item.get('image') or fallback_img
    
    st.markdown((
        f'<img src="{img_url}" '
        'style="width:100%; border-radius:10px; margin-bottom:20px;" '
        f'onerror="this.onerror=null; this.src=\'{fallback_img}\';">'
    ), unsafe_allow_html=True)
    
    content = item.get('content')
    if content:
        st.markdown(content)
    else:
        st.info("NO DATA CONTENT.")
        if item.get('link') and item.get('link') != '#':
             st.markdown(f"[>> 前往外部連結]({item['link']})")

# --- 輔助函式 ---

def render_hero():
    st.markdown((
        '<div style="text-align: center; padding: 80px 0 60px 0;">'
        '<h1 style="font-size: 5rem; line-height: 0.9; color: #fff; text-shadow: 0 0 30px rgba(188, 19, 254, 0.8); font-family: \'Orbitron\';">'
        'SYSTEM <span style="color: #00F0FF;">ONLINE</span></h1>'
        '<p style="font-family: \'Rajdhani\'; font-size: 1.2rem; color: #888; margin-top: 20px; letter-spacing: 3px;">'
        'THE ULTIMATE AI DATABASE // ACCESS GRANTED</p></div>'
    ), unsafe_allow_html=True)

def render_section_header(title):
    st.markdown((
        f'<div style="display: flex; align-items: center; margin: 40px 0 30px 0;">'
        f'<div style="width: 4px; height: 25px; background: #00F0FF; margin-right: 15px; box-shadow: 0 0 10px #00F0FF;"></div>'
        f'<h2 style="font-family: \'Orbitron\'; margin: 0; font-size: 2rem; color: #fff;">{title}</h2>'
        f'</div>'
    ), unsafe_allow_html=True)

def render_cards(supabase, data_list, bookmarked_ids=[]):
    if not data_list:
        st.markdown("<div style='text-align:center; padding:50px; color:#666;'>NO SIGNAL DETECTED.</div>", unsafe_allow_html=True)
        return

    st.markdown("""<style>.resource-card { cursor: default; }</style>""", unsafe_allow_html=True)
    fallback_img = "https://placehold.co/800x500/050508/00F0FF?text=NO+SIGNAL"

    cols = st.columns(3)
    for index, item in enumerate(data_list):
        with cols[index % 3]:
            img = item.get('image') or fallback_img
            link = item.get('link', '#')
            resource_id = item.get('id')
            has_content = item.get('content') and len(item.get('content')) > 5
            
            is_bookmarked = resource_id in bookmarked_ids
            heart_icon = "💜" if is_bookmarked else "🤍"
            btn_label = "SAVED" if is_bookmarked else "SAVE"

            st.markdown((
                f'<div class="resource-card">'
                f'<div style="position: relative; height: 180px; overflow: hidden;">'
                f'<img src="{img}" style="width:100%; height:100%; object-fit:cover; filter: grayscale(80%); transition:0.5s;" '
                f'onmouseover="this.style.filter=\'grayscale(0%)\'; this.style.transform=\'scale(1.1)\'" '
                f'onmouseout="this.style.filter=\'grayscale(80%)\'; this.style.transform=\'scale(1)\'" '
                f'onerror="this.onerror=null; this.src=\'{fallback_img}\';">'
                f'<div style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.8); border: 1px solid #00F0FF; color: #00F0FF; padding: 2px 6px; font-size: 0.7rem; font-family:Orbitron;">'
                f'{item.get("sub_category", "APP").upper()}</div></div>'
                f'<div style="padding: 20px 20px 5px 20px;">'
                f'<div style="font-size: 0.7rem; color: #BC13FE; font-weight: 700;">/// {item.get("country", "GLOBAL")}</div>'
                f'<div style="font-family: \'Orbitron\'; font-size: 1.2rem; color: #fff; margin: 5px 0 10px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{item["title"]}</div>'
                f'<div style="font-size: 0.85rem; color: #aaa; height: 3em; overflow: hidden; font-family: \'Rajdhani\'; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">{item["summary"]}</div>'
                f'</div></div>'
            ), unsafe_allow_html=True)

            with st.container():
                c_btn1, c_btn2 = st.columns([1, 1])
                with c_btn1:
                    if st.button(f"{heart_icon} {btn_label}", key=f"fav_{resource_id}", use_container_width=True):
                        if 'user' in st.session_state and st.session_state['user']:
                            user_id = st.session_state['user'].id
                            if is_bookmarked:
                                supabase.table("bookmarks").delete().eq("user_id", user_id).eq("resource_id", resource_id).execute()
                                st.toast("Removed.", icon="🗑️")
                            else:
                                supabase.table("bookmarks").insert({"user_id": user_id, "resource_id": resource_id}).execute()
                                st.toast("Saved.", icon="💜")
                            st.rerun()
                        else:
                            st.session_state['login_trigger'] = True
                            st.rerun()
                with c_btn2:
                    if has_content:
                        if st.button("📖 READ", key=f"read_{resource_id}", use_container_width=True):
                            show_reader(item)
                    else:
                        if link and link != "#":
                            st.link_button("🚀 VISIT", link, use_container_width=True)
                        else:
                            st.button("🚫 NO LINK", disabled=True, key=f"no_{resource_id}", use_container_width=True)
            
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

def render_footer():
    st.markdown("<div style='text-align:center; padding: 50px; color:#444; font-family: Rajdhani;'>AI.ORG SYSTEM // 2025 // SECURE CONNECTION</div>", unsafe_allow_html=True)