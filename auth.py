import streamlit as st
from supabase import Client

# 🌟 使用 Dialog 做出浮動登入視窗
@st.dialog("/// IDENTITY_VERIFICATION")
def render_auth_modal(supabase: Client):
    st.markdown("""
        <style>
        div[data-testid="stDialog"] {
            background-color: #0d0d16;
            border: 1px solid #BC13FE; /* 紫色邊框代表使用者 */
            box-shadow: 0 0 40px rgba(188, 19, 254, 0.2);
        }
        input {
            background-color: #1a1a24 !important;
            color: white !important;
            border: 1px solid #333 !important;
        }
        input:focus {
            border-color: #BC13FE !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 頁籤切換：登入 vs 註冊
    tab1, tab2 = st.tabs(["LOGIN (現有帳號)", "REGISTER (新註冊)"])

    # --- 登入區塊 ---
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("🔓 ACCESS SYSTEM")
            
            if submitted:
                try:
                    response = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })
                    # 登入成功，寫入 Session
                    st.session_state['user'] = response.user
                    st.toast(f"WELCOME BACK, {email.split('@')[0]}", icon="🟢")
                    st.rerun() # 重新整理頁面
                except Exception as e:
                    st.error(f"LOGIN FAILED: {e}")

    # --- 註冊區塊 ---
    with tab2:
        with st.form("signup_form"):
            new_email = st.text_input("New Email")
            new_password = st.text_input("Set Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submitted_signup = st.form_submit_button("📝 CREATE IDENTITY")

            if submitted_signup:
                if new_password != confirm_password:
                    st.error("PASSWORDS DO NOT MATCH.")
                else:
                    try:
                        response = supabase.auth.sign_up({
                            "email": new_email,
                            "password": new_password
                        })
                        st.success("REGISTRATION SUCCESSFUL! PLEASE LOGIN.")
                        # 如果你有開啟 Email 驗證，這裡要提示去收信
                    except Exception as e:
                        st.error(f"ERROR: {e}")

def logout(supabase):
    supabase.auth.sign_out()
    if 'user' in st.session_state:
        del st.session_state['user']
    st.rerun()