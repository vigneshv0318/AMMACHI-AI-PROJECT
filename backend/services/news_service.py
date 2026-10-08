import urllib.parse
import xml.etree.ElementTree as ET
import requests
import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger("ammachi.news_service")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def clean_html(raw_html: str) -> str:
    """Strips HTML tags and escapes from RSS descriptions."""
    if not raw_html:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', raw_html)
    clean = re.sub(r'&nbsp;', ' ', clean)
    clean = re.sub(r'&amp;', '&', clean)
    clean = re.sub(r'&quot;', '"', clean)
    clean = re.sub(r'&#39;', "'", clean)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()

def is_current_affairs_query(query: str) -> bool:
    """Detects if query is asking about current affairs, modern news, politics, technology, economy, or recent events."""
    if not query:
        return False
    q = query.lower()
    trigger_words = [
        "news", "current", "affairs", "today", "latest", "recent", "update", "happening",
        "politics", "minister", "prime minister", "chief minister", "government", "parliament", "election",
        "isro", "space", "chandrayaan", "gaganyaan", "satellite", "rocket", "aditya",
        "technology", "ai", "artificial intelligence", "upi", "semiconductor", "digital india", "software",
        "agriculture", "farming", "farmer", "crops", "drone", "monsoon",
        "economy", "industry", "industries", "manufacturing", "gdp", "market", "startup",
        "vande bharat", "railway", "bullet train", "highway", "infrastructure", "smart city",
        "stalin", "modi", "tamil nadu government", "india 2026", "india today"
    ]
    return any(w in q for w in trigger_words)

def fetch_india_live_news(query: str, language: str = "Tamil") -> List[Dict[str, str]]:
    """
    Fetches real-time live Indian news, politics, technology, agriculture, and industry updates
    from verified real-time news aggregation feeds.
    """
    clean_q = query.strip()
    # Enhance query context for India
    search_term = f"{clean_q} India {language}" if "india" not in clean_q.lower() else clean_q
    encoded = urllib.parse.quote(search_term)
    
    # Google News India Real-time RSS Feed
    rss_url = f"https://news.google.com/rss/search?q={encoded}&hl=en-IN&gl=IN&ceid=IN:en"
    
    results = []
    try:
        r = requests.get(rss_url, headers=HEADERS, timeout=6)
        if r.status_code == 200:
            root = ET.fromstring(r.text)
            items = root.findall(".//item")
            for item in items[:6]:
                title_elem = item.find("title")
                desc_elem = item.find("description")
                date_elem = item.find("pubDate")
                source_elem = item.find("source")

                title = title_elem.text if title_elem is not None else ""
                desc = clean_html(desc_elem.text) if desc_elem is not None else ""
                date = date_elem.text if date_elem is not None else ""
                source = source_elem.text if source_elem is not None else "Indian News"

                if title:
                    results.append({
                        "title": title,
                        "snippet": desc[:200],
                        "date": date[:16] if date else "",
                        "source": source
                    })
    except Exception as e:
        logger.warning("Google News fetch warning: %s. Using fallback.", e)

    # Fallback to national topic queries if specific search had 0 results
    if not results:
        try:
            general_encoded = urllib.parse.quote(f"{clean_q} India latest")
            r = requests.get(f"https://news.google.com/rss/search?q={general_encoded}&hl=en-IN&gl=IN&ceid=IN:en", headers=HEADERS, timeout=6)
            if r.status_code == 200:
                root = ET.fromstring(r.text)
                for item in root.findall(".//item")[:4]:
                    t = item.find("title")
                    d = item.find("description")
                    if t is not None and t.text:
                        results.append({
                            "title": t.text,
                            "snippet": clean_html(d.text)[:200] if d is not None else "",
                            "date": "",
                            "source": "India Updates"
                        })
        except Exception:
            pass

    return results
