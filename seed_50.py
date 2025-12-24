import streamlit as st
from supabase import create_client

# 1. 設定與連線
st.set_page_config(page_title="AI.ORG 批量匯入工具")
st.title("🚀 AI.ORG: 50 筆熱門 AI 工具批量匯入")

# 連線 Supabase
try:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase = create_client(url, key)
    st.success("✅ Supabase 連線成功！準備匯入資料...")
except Exception as e:
    st.error(f"❌ 連線失敗，請檢查 secrets.toml: {e}")
    st.stop()

# 2. 準備好的 50 筆資料 (包含分類對應)
# 注意：這裡的 'category' 對應資料庫欄位，實際上存的是子分類 (如 'Developers', 'Creators')
# app.py 會根據這些子分類自動歸類到 'Start Here', 'Explore', 'Learn' 等主分類
tools_list = [
    # --- Start Here / Beginners (入門必備) ---
    {"title": "ChatGPT (OpenAI)", "category": "Beginners", "tags": ["chatbot", "llm", "popular"], "link": "https://chat.openai.com", "image_url": "https://images.unsplash.com/photo-1675271591211-126ad94e495d?w=800", "summary": "全球最知名的 AI 聊天機器人，能處理寫作、分析與創意任務。"},
    {"title": "Claude 3.5 Sonnet", "category": "Beginners", "tags": ["chatbot", "writing", "coding"], "link": "https://claude.ai", "image_url": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800", "summary": "以自然流暢的寫作與強大的邏輯能力著稱，是寫作與程式開發的強力助手。"},
    {"title": "Perplexity AI", "category": "Beginners", "tags": ["search", "research", "real-time"], "link": "https://www.perplexity.ai", "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800", "summary": "結合搜尋引擎與 AI 的問答工具，提供即時資訊並附上引用來源。"},
    {"title": "Google Gemini", "category": "Beginners", "tags": ["google", "multimodal", "assistant"], "link": "https://gemini.google.com", "image_url": "https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?w=800", "summary": "Google 的多模態 AI 模型，深度整合 Google 生態系，擅長處理文字與圖像。"},
    {"title": "Microsoft Copilot", "category": "Beginners", "tags": ["microsoft", "productivity", "office"], "link": "https://copilot.microsoft.com", "image_url": "https://images.unsplash.com/photo-1633419461186-7d75e443362e?w=800", "summary": "微軟的 AI 助手，整合於 Windows 與 Office 365 中，提升工作效率。"},

    # --- Start Here / Developers (開發者神器) ---
    {"title": "GitHub Copilot", "category": "Developers", "tags": ["coding", "vscode", "microsoft"], "link": "https://github.com/features/copilot", "image_url": "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=800", "summary": "最受歡迎的 AI 結對程式設計師，直接在 IDE 中提供程式碼建議。"},
    {"title": "Cursor", "category": "Developers", "tags": ["ide", "coding", "agent"], "link": "https://cursor.sh", "image_url": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800", "summary": "新一代 AI 程式碼編輯器，深度整合 AI 功能，能理解整個專案庫。"},
    {"title": "Bolt.new", "category": "Developers", "tags": ["web-dev", "stackblitz", "rapid"], "link": "https://bolt.new", "image_url": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800", "summary": "在瀏覽器中直接開發、執行與部署全端網頁應用的 AI 工具。"},
    {"title": "Replit", "category": "Developers", "tags": ["cloud-ide", "collaboration", "coding"], "link": "https://replit.com", "image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800", "summary": "強大的線上 IDE，內建 Ghostwriter AI 助手，適合快速構建與協作。"},
    {"title": "Windsurf", "category": "Developers", "tags": ["ide", "agent", "coding"], "link": "https://codeium.com/windsurf", "image_url": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=800", "summary": "由 Codeium 推出的 AI 編輯器，專注於上下文理解與流暢的開發體驗。"},
    {"title": "v0.dev", "category": "Developers", "tags": ["ui", "frontend", "vercel"], "link": "https://v0.dev", "image_url": "https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?w=800", "summary": "Vercel 推出的 AI 工具，能透過文字描述生成 React/Tailwind UI 介面。"},
    {"title": "Lovable", "category": "Developers", "tags": ["no-code", "web-app", "gpt-4"], "link": "https://lovable.dev", "image_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800", "summary": "將創意轉化為完整網頁應用的 AI 工具，適合快速原型製作。"},
    {"title": "Tabnine", "category": "Developers", "tags": ["privacy", "enterprise", "coding"], "link": "https://www.tabnine.com", "image_url": "https://images.unsplash.com/photo-1555099962-4199c345e5dd?w=800", "summary": "強調隱私與企業安全的 AI 程式碼補全工具，支援多種 IDE。"},
    {"title": "Amazon Q", "category": "Developers", "tags": ["aws", "cloud", "enterprise"], "link": "https://aws.amazon.com/q/", "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800", "summary": "AWS 專用的生成式 AI 助手，協助開發者管理雲端架構與程式碼。"},
    {"title": "Aider", "category": "Developers", "tags": ["cli", "python", "coding"], "link": "https://aider.chat", "image_url": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800", "summary": "在終端機 (CLI) 運行的 AI 結對程式工具，能直接修改 git repo 中的程式碼。"},

    # --- Start Here / Creators (創作者與設計) ---
    {"title": "Midjourney", "category": "Creators", "tags": ["image-gen", "art", "discord"], "link": "https://www.midjourney.com", "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800", "summary": "目前公認品質最高的 AI 圖像生成工具，透過 Discord 進行操作。"},
    {"title": "Runway", "category": "Creators", "tags": ["video-gen", "editor", "creative"], "link": "https://runwayml.com", "image_url": "https://images.unsplash.com/photo-1536240478700-b869070f9279?w=800", "summary": "強大的 AI 影片生成與編輯平台，著名的 Gen-3 模型即源自於此。"},
    {"title": "Canva Magic Studio", "category": "Creators", "tags": ["design", "social-media", "easy"], "link": "https://www.canva.com", "image_url": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=800", "summary": "Canva 的 AI 套件，包含文字生圖、魔術編輯與自動去背等功能。"},
    {"title": "Adobe Firefly", "category": "Creators", "tags": ["adobe", "photoshop", "copyright-safe"], "link": "https://firefly.adobe.com", "image_url": "https://images.unsplash.com/photo-1626785774573-4b799314348d?w=800", "summary": "Adobe 的生成式 AI，整合於 Photoshop 中，強調版權安全與高品質。"},
    {"title": "Suno", "category": "Creators", "tags": ["music", "audio", "song-gen"], "link": "https://suno.com", "image_url": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=800", "summary": "革命性的 AI 音樂生成器，能創作出完整且高品質的歌曲與歌詞。"},
    {"title": "Udio", "category": "Creators", "tags": ["music", "audio", "high-fidelity"], "link": "https://www.udio.com", "image_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800", "summary": "另一款頂尖的 AI 音樂工具，以極高的音質與音樂性著稱。"},
    {"title": "ElevenLabs", "category": "Creators", "tags": ["voice", "tts", "dubbing"], "link": "https://elevenlabs.io", "image_url": "https://images.unsplash.com/photo-1589903308904-1010c2294adc?w=800", "summary": "最逼真的 AI 語音合成與複製工具，支援多語言與情感表達。"},
    {"title": "HeyGen", "category": "Creators", "tags": ["avatar", "video", "marketing"], "link": "https://www.heygen.com", "image_url": "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=800", "summary": "製作 AI 虛擬人影片的最佳工具，適合行銷、教學與簡報影片。"},
    {"title": "Descript", "category": "Creators", "tags": ["video-editor", "podcast", "transcription"], "link": "https://www.descript.com", "image_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800", "summary": "像編輯文件一樣編輯影片與音訊，擁有強大的 AI 語音複製與降噪功能。"},
    {"title": "InVideo", "category": "Creators", "tags": ["video-gen", "youtube", "text-to-video"], "link": "https://invideo.io", "image_url": "https://images.unsplash.com/photo-1626544827763-d516dce335ca?w=800", "summary": "透過文字指令快速生成完整的 YouTube 或社交媒體影片。"},

    # --- Start Here / Business (商業與生產力) ---
    {"title": "Zapier", "category": "Business", "tags": ["automation", "workflow", "integration"], "link": "https://zapier.com", "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800", "summary": "自動化工作流程的王者，現在整合了強大的 AI 功能來連接不同應用程式。"},
    {"title": "Notion AI", "category": "Business", "tags": ["notes", "productivity", "docs"], "link": "https://www.notion.so", "image_url": "https://images.unsplash.com/photo-1664575602276-acd073f104c1?w=800", "summary": "直接整合在 Notion 中的 AI 助手，協助筆記整理、摘要與內容生成。"},
    {"title": "Otter.ai", "category": "Business", "tags": ["meeting", "transcription", "notes"], "link": "https://otter.ai", "image_url": "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=800", "summary": "AI 會議記錄助手，能自動轉錄語音並生成會議摘要。"},
    {"title": "Fireflies.ai", "category": "Business", "tags": ["meeting", "analysis", "crm"], "link": "https://fireflies.ai", "image_url": "https://images.unsplash.com/photo-1553877607-13e5b06860ce?w=800", "summary": "自動加入會議並錄音、轉錄、分析對話內容的 AI 助理。"},
    {"title": "Jasper", "category": "Business", "tags": ["marketing", "copywriting", "seo"], "link": "https://www.jasper.ai", "image_url": "https://images.unsplash.com/photo-1432888498266-38ffec3eaf0a?w=800", "summary": "專為行銷人員打造的 AI 寫作工具，能生成符合品牌語氣的文案。"},
    {"title": "Beautiful.ai", "category": "Business", "tags": ["presentation", "slides", "design"], "link": "https://www.beautiful.ai", "image_url": "https://images.unsplash.com/photo-1544531586-fde5298cdd40?w=800", "summary": "智慧型簡報製作工具，自動排版讓你的投影片永遠保持美觀。"},
    {"title": "Gamma", "category": "Business", "tags": ["presentation", "web", "docs"], "link": "https://gamma.app", "image_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800", "summary": "透過文字描述快速生成簡報、文件與網頁，介面精美且靈活。"},
    {"title": "Grammarly", "category": "Business", "tags": ["writing", "grammar", "email"], "link": "https://www.grammarly.com", "image_url": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=800", "summary": "不僅是拼字檢查，現在更是強大的 AI 寫作教練，改善語氣與清晰度。"},
    {"title": "Copy.ai", "category": "Business", "tags": ["copywriting", "marketing", "sales"], "link": "https://www.copy.ai", "image_url": "https://images.unsplash.com/photo-1542435503-956c469947f6?w=800", "summary": "快速生成電子郵件、社交媒體貼文與廣告文案的 AI 工具。"},
    {"title": "HubSpot AI", "category": "Business", "tags": ["crm", "marketing", "sales"], "link": "https://www.hubspot.com/ai", "image_url": "https://images.unsplash.com/photo-1560472355-536de3962603?w=800", "summary": "整合於 HubSpot CRM 中的 AI 功能，協助內容生成與客戶分析。"},

    # --- Explore / Demos (新奇有趣的應用) ---
    {"title": "Hugging Face", "category": "Demos", "tags": ["models", "community", "opensource"], "link": "https://huggingface.co", "image_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800", "summary": "AI 界的 GitHub，擁有海量開源模型與即時 Demo 試玩。"},
    {"title": "Leonardo.ai", "category": "Demos", "tags": ["art", "assets", "game"], "link": "https://leonardo.ai", "image_url": "https://images.unsplash.com/photo-1633265486064-084b228ad802?w=800", "summary": "生成高品質遊戲資產與藝術圖的平台，模型微調功能強大。"},
    {"title": "Ideogram", "category": "Demos", "tags": ["image-gen", "text-rendering", "typography"], "link": "https://ideogram.ai", "image_url": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=800", "summary": "擅長在圖片中精準生成文字與排版的 AI 繪圖工具。"},
    {"title": "Krea.ai", "category": "Demos", "tags": ["real-time", "upscale", "video"], "link": "https://www.krea.ai", "image_url": "https://images.unsplash.com/photo-1558655146-d09347e0b7a9?w=800", "summary": "提供即時繪圖與畫質修復增強功能的創意工具。"},
    {"title": "Luma Dream Machine", "category": "Demos", "tags": ["video-gen", "3d", "fast"], "link": "https://lumalabs.ai", "image_url": "https://images.unsplash.com/photo-1617791160505-6f00504e3519?w=800", "summary": "Luma Labs 推出的影片生成模型，速度快且物理效果逼真。"},
    
    # --- Learn / Models (模型與知識) ---
    {"title": "Llama 3 (Meta)", "category": "Models", "tags": ["opensource", "meta", "llm"], "link": "https://llama.meta.com", "image_url": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800", "summary": "Meta 推出的最強開源大型語言模型，推動了本地端 AI 的發展。"},
    {"title": "Mistral AI", "category": "Models", "tags": ["opensource", "europe", "efficient"], "link": "https://mistral.ai", "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800", "summary": "來自法國的 AI 新星，提供高效能且強大的開源模型。"},
    {"title": "Grok (xAI)", "category": "Models", "tags": ["twitter", "x", "fun"], "link": "https://grok.x.ai", "image_url": "https://images.unsplash.com/photo-1611162616475-46b635cb6868?w=800", "summary": "馬斯克旗下 xAI 開發的模型，具有即時存取 X (Twitter) 資訊的能力。"},
    {"title": "Poe", "category": "Models", "tags": ["aggregator", "chat", "bot"], "link": "https://poe.com", "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800", "summary": "Quora 推出的 AI 聚合平台，讓你一站式使用 GPT-4, Claude 等多種模型。"},
    {"title": "HuggingChat", "category": "Models", "tags": ["chat", "opensource", "free"], "link": "https://huggingface.co/chat", "image_url": "https://images.unsplash.com/photo-1535378437323-dd95916940d3?w=800", "summary": "Hugging Face 的開源聊天介面，可免費體驗各種最新的開源模型。"}
]

# 3. 執行匯入
st.subheader("批次寫入資料庫")
st.write(f"清單中共有 {len(tools_list)} 筆工具資料。")

if st.button("🚀 開始匯入 50 筆資料"):
    progress_bar = st.progress(0)
    success_count = 0
    
    for i, tool in enumerate(tools_list):
        try:
            # 寫入資料庫
            # 注意: 如果你的資料庫欄位有差異，請在這裡調整
            data = {
                "title": tool["title"],
                "summary": tool["summary"],
                "link": tool["link"],
                "image_url": tool["image_url"],
                "category": tool["category"], # 這裡存入的是子分類名稱
                "country": "Global",          # 預設為 Global
                "tags": tool["tags"],
                "is_verified": True
            }
            supabase.table("ai_resources").insert(data).execute()
            success_count += 1
        except Exception as e:
            st.error(f"⚠️ 匯入失敗 ({tool['title']}): {e}")
        
        # 更新進度條
        progress_bar.progress((i + 1) / len(tools_list))
    
    if success_count > 0:
        st.success(f"🎉 成功匯入 {success_count} 筆資料！")
        st.balloons()
        st.info("請回到終端機按 Ctrl+C 停止此程式，然後執行 `streamlit run app.py` 查看成果。")