def get_main_style() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700&display=swap');

    :root {
        --bg-core: #050508;
        --neon-cyan: #00F0FF;
        --neon-purple: #BC13FE;
    }

    .stApp {
        background-color: var(--bg-core);
        background-image: 
            linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(188, 19, 254, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        font-family: 'Rajdhani', sans-serif;
    }

    header[data-testid="stHeader"] { display: none; }

    /* --- 導覽列容器 --- */
    .nav-menu-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        width: 100%;
        height: 100%;
    }

    .nav-item {
        position: relative;
        padding: 10px 0;
        cursor: pointer;
    }

    .nav-link {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1rem;
        color: #ddd;
        font-weight: 700;
        letter-spacing: 1px;
        transition: 0.3s;
        padding: 8px 16px;
        border: 1px solid transparent;
        border-radius: 50px;
        background: rgba(255,255,255,0.02);
    }
    
    .nav-item:hover .nav-link {
        color: var(--neon-cyan);
        background: rgba(0, 240, 255, 0.1);
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
    }

    /* --- [關鍵修改] 外層容器變成透明且包含 Padding --- */
    .nav-dropdown {
        display: none; 
        position: absolute;
        top: 100%; 
        left: 50%;
        transform: translateX(-50%);
        width: 300px;
        z-index: 999999;
        
        /* 這裡不設背景色，只負責佔位 */
        background: transparent;
        border: none;
        box-shadow: none;
        
        /* 🌟 這是重點：用 padding 創造出 20px 的「安全緩衝區」 */
        /* 滑鼠經過這裡時，依然算是在選單內，所以選單不會消失 */
        padding-top: 20px; 
    }

    /* --- [新 class] 真正的視覺盒子 --- */
    /* 顏色和邊框移到這裡 */
    .nav-dropdown-box {
        background: rgba(10, 12, 18, 0.95);
        border: 1px solid var(--neon-cyan);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.2);
        backdrop-filter: blur(10px);
    }

    .nav-item:hover .nav-dropdown {
        display: block;
        animation: hologram-open 0.3s ease-out forwards;
    }

    .dropdown-caption {
        font-family: 'Orbitron';
        font-size: 0.8rem;
        color: var(--neon-purple);
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 5px; margin-bottom: 10px;
    }
    .dropdown-desc {
        color: #ccc; font-size: 0.9rem; margin-bottom: 15px; line-height: 1.4;
    }
    
    .sub-link {
        display: block;
        padding: 8px 12px;
        margin-bottom: 5px;
        color: var(--neon-cyan);
        text-decoration: none;
        background: rgba(0, 240, 255, 0.05);
        border-radius: 6px;
        transition: 0.2s;
        font-weight: 700; text-align: center;
    }
    .sub-link:hover {
        background: var(--neon-cyan);
        color: #000;
        box-shadow: 0 0 10px var(--neon-cyan);
    }

    @keyframes hologram-open {
        from { opacity: 0; transform: translateX(-50%) translateY(-10px); }
        to { opacity: 1; transform: translateX(-50%) translateY(0); }
    }
    
    @keyframes text-rgb {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
    
    .resource-card {
        background: #0B0C15; border: 1px solid #333; border-radius: 16px;
        position: relative; overflow: hidden; transition: 0.4s;
    }
    .resource-card:hover {
        transform: translateY(-5px); border-color: var(--neon-cyan);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
    }
    .card-hover-reveal {
        max-height: 0; opacity: 0; transition: 0.4s;
        color: var(--neon-cyan); font-weight: 700; font-size: 0.8rem;
        margin-top: 5px; border-top: 1px solid rgba(0,240,255,0.3); padding-top: 5px;
    }
    .resource-card:hover .card-hover-reveal { max-height: 50px; opacity: 1; }
    </style>
    """