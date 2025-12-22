import time
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

# 模擬瀏覽器 Header，避免被擋
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def search_web(query, max_results=5):
    """
    對應圖片中的 [SERP] 區塊：去搜尋引擎找資料
    """
    results = []
    print(f"🕵️‍♂️ Searching for: {query}...")
    
    with DDGS() as ddgs:
        # 使用 DuckDuckGo 搜尋
        ddgs_gen = ddgs.text(query, max_results=max_results)
        for r in ddgs_gen:
            results.append({
                "title": r['title'],
                "link": r['href'],
                "snippet": r['body']
            })
            
    return results

def crawl_website(url):
    """
    對應圖片中的 [Crawler] 區塊：深入網頁抓取 HTML
    """
    try:
        # 對應圖片中的 [Rate Limit]：休息一下，避免太快被封鎖
        time.sleep(1.5) 
        
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. 抓標題 (og:title > title)
        title = soup.find("meta", property="og:title")
        title = title["content"] if title else soup.title.string if soup.title else ""
        
        # 2. 抓描述 (og:description > description)
        desc = soup.find("meta", property="og:description")
        if not desc:
            desc = soup.find("meta", attrs={"name": "description"})
        summary = desc["content"] if desc else ""
        
        # 3. 抓圖片 (og:image)
        image = soup.find("meta", property="og:image")
        image_url = image["content"] if image else ""

        return {
            "title": title.strip(),
            "summary": summary.strip()[:200], # 限制長度
            "image_url": image_url,
            "link": url
        }
    except Exception as e:
        print(f"❌ Crawl failed for {url}: {e}")
        return None