import os
import json
import re
import logging
from typing import List, Dict, Any, Optional

try:
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
except ImportError:
    # Graceful fallback if langchain_core is not installed in the environment
    class BaseMessage:
        def __init__(self, content="", **kwargs):
            self.content = content
    class SystemMessage(BaseMessage): pass
    class HumanMessage(BaseMessage): pass
    class AIMessage(BaseMessage): pass

from database import crud
from services.gemini_service import get_llm_client, invoke_direct_llm
from services.culture_service import get_festivals_for_language, get_festival_by_id
from services.youtube_service import get_festival_youtube_videos
from services.news_service import is_current_affairs_query, fetch_india_live_news

logger = logging.getLogger("ammachi.langgraph_culture")

def scrub_response_text(text: str) -> str:
    """Removes any leaked technical function tags, XML tags, or raw tool calls and normalizes clean bullets."""
    if not text:
        return ""
    cleaned = re.sub(r'<function.*?>.*?</function>', '', text, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'<function.*?>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'</function>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'\{[^{]*"function":\s*"[^"]*"[^{]*\}', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'\[IMAGE:\s*[^\]]+\]', '', cleaned)
    cleaned = re.sub(r'\[VIDEO:\s*[^\]]+\]', '', cleaned)
    # Normalize bullet points: convert '* **' or '- **' or '* ' to clean '• '
    cleaned = re.sub(r'(?m)^\s*[\*\-]\s+', '• ', cleaned)
    return cleaned.strip()

def run_culture_chat(
    message: str,
    raw_history: List[Dict[str, str]],
    username: str,
    language: str = "Tamil"
) -> Dict[str, Any]:
    """
    Context-aware, live news & current affairs enabled cultural conversation engine.
    Equipped with real-time news retrieval across Indian politics, technology, space, agriculture, and industries.
    Works 100% reliably with multi-tiered LLM execution and zero-dependency fallback.
    """
    # 1. Check if user is asking about current affairs, news, modern developments, space, tech, politics, or agriculture
    live_news_context = ""
    if is_current_affairs_query(message):
        try:
            news_items = fetch_india_live_news(message, language)
            if news_items:
                live_news_context = "\n\n📰 REAL-TIME VERIFIED LIVE NEWS & DEVELOPMENTS IN INDIA (Use these factual details in your explanation):\n"
                for item in news_items[:4]:
                    live_news_context += f"• Headline: {item['title']}\n  Snippet: {item['snippet']}\n  Source: {item['source']} ({item['date']})\n\n"
        except Exception as e:
            logger.warning("Error fetching live news: %s", e)

    sys_content = (
        f"You are Ammachi (அம்மாச்சி), a warm, loving, and highly knowledgeable Indian grandmother talking to an NRI child.\n"
        f"You are deeply proud of both India's ancient cultural heritage ({language} roots, traditions, history) and MODERN INDIA'S ACHIEVEMENTS (ISRO space missions, cutting-edge technology & AI, UPI, modern agriculture, governance, green energy, and industries).\n\n"
        f"{live_news_context}"
        f"RESPONSE STRUCTURE (MANDATORY):\n"
        f"1. 🌟 **Warm Opening**: Start with an affectionate grandmother greeting addressing the child as 'Kanna' or 'Chellam' and enthusiastically introduce the topic.\n"
        f"2. 📌 **Detailed Points & Modern/Cultural Realities**: Provide 3 to 4 comprehensive, well-explained bullet points using bold headers and relevant modern/cultural emojis (🚀, 💻, 🌾, 🏭, 🏛️, 📈, 🪔, 🇮🇳, 💡). Include real factual names, projects, technologies, and achievements.\n"
        f"3. 💡 **Insight & National/Cultural Pride**: A short paragraph explaining why this progress is exciting, how it connects to our roots, and why children should be proud of India's growth.\n"
        f"4. 👵 **Interactive Closing Question**: End with an encouraging, affectionate question inviting the child to share their thoughts.\n\n"
        f"GUIDELINES:\n"
        f"• LANGUAGE: Write primarily in clear, engaging English so the NRI child can read effortlessly, including authentic native {language} vocabulary in brackets where appropriate (e.g., Vanakkam Kanna, Sakkarai Pongal, Agal Vilakku).\n"
        f"• LENGTH: Detailed and educational (around 140 to 220 words). Do NOT give brief 2-line answers.\n"
        f"• REAL-TIME ACCURACY: If the child asks about current affairs, space, politics, technology, or recent events, utilize the live news context above to give 100% up-to-date, non-hallucinated facts.\n"
        f"• NO IMAGES, NO CODE, NO XML: Output clean markdown only."
    )

    response_text = ""

    # Strategy A: Try LangChain Chat Model if available
    llm = get_llm_client()
    if llm:
        try:
            system_prompt = SystemMessage(content=sys_content)
            messages: List[BaseMessage] = [system_prompt]
            for msg in raw_history[-4:]:
                c = msg.get("content", "")
                if msg.get("role") == "user":
                    messages.append(HumanMessage(content=c))
                elif msg.get("role") == "assistant":
                    messages.append(AIMessage(content=c))
            messages.append(HumanMessage(content=message))

            res = llm.invoke(messages)
            raw_text = res.content if hasattr(res, "content") else str(res)
            response_text = scrub_response_text(raw_text)
        except Exception as e:
            logger.warning("LangChain invoke exception: %s. Falling back to direct REST LLM.", e)

    # Strategy B: Zero-Dependency Direct REST API (Groq / Gemini)
    if not response_text:
        try:
            raw_direct = invoke_direct_llm(sys_content, raw_history[-4:], message)
            if raw_direct:
                response_text = scrub_response_text(raw_direct)
        except Exception as e:
            logger.warning("Direct REST LLM exception: %s", e)

    # Strategy C: Rich, structured fallback if offline
    if not response_text:
        msg_lower = message.lower()
        if "isro" in msg_lower or "space" in msg_lower or "chandrayaan" in msg_lower:
            response_text = (
                f"Kanna! India's space program ISRO is reaching incredible heights and making our motherland so proud across the globe! 🚀🇮🇳\n\n"
                f"• **Chandrayaan Moon Missions**: India made history as the very first nation to land successfully on the Moon's South Pole with Chandrayaan-3, proving indigenous technological excellence.\n\n"
                f"• **Gaganyaan Human Spaceflight**: ISRO is preparing to send Indian astronauts (*Vyomanauts*) into Earth's orbit on our own indigenous rocket system, marking a giant leap for Indian human space exploration.\n\n"
                f"• **Aditya-L1 Solar Mission**: Our first dedicated space observatory studying the Sun from the Lagrange point L1, sending vital scientific data back to Earth.\n\n"
                f"💡 These achievements show that with hard work, scientific curiosity, and dedication, Indian scientists can achieve the impossible. Would you like to build space rockets or study astronomy when you grow up, Chellam?"
            )
        elif "tech" in msg_lower or "ai" in msg_lower or "upi" in msg_lower:
            response_text = (
                f"Kanna! India has become a global powerhouse in technology, digital innovation, and artificial intelligence! 💻✨\n\n"
                f"• **UPI & Digital Public Infrastructure**: Unified Payments Interface (UPI) developed in India now processes billions of real-time transactions instantly from small roadside coconut vendors to huge shopping malls!\n\n"
                f"• **IndiaAI Mission & Semiconductors**: India is investing thousands of crores to build indigenous AI compute chips, semiconductor fabrication plants, and supercomputers.\n\n"
                f"• **Global Startup Ecosystem**: India is home to the world's 3rd largest startup ecosystem, creating innovative apps in healthcare, education, and clean energy.\n\n"
                f"💡 Modern technology helps us preserve our native culture while solving global challenges. What kind of technology or video game do you love creating, Kanna?"
            )
        elif "king" in msg_lower or "chola" in msg_lower:
            response_text = (
                f"Kanna! Let Ammachi tell you the glorious stories of our legendary Tamil kings who ruled with immense bravery and wisdom! 👑✨\n\n"
                f"• **Raja Raja Chola I**: Built the magnificent 1,000-year-old Brihadeeswara Temple (Thanjavur Periya Kovil) with brilliant acoustics and towering granite architecture.\n\n"
                f"• **Karikala Cholan**: Built the Kallanai Dam on the Kaveri river over 2,000 years ago, which is the world's oldest functional water-diversion dam!\n\n"
                f"• **Rajendra Chola I**: Expanded the Chola maritime empire all the way to Southeast Asia with a formidable naval fleet.\n\n"
                f"💡 Our kings taught us that true leadership lies in serving the people and preserving our cultural roots. Which king's story excites you most, Chellam?"
            )
        else:
            response_text = (
                f"Kanna! In modern India, our ancient culture and forward-looking progress in technology, agriculture, and science go hand in hand! 🌟🇮🇳\n\n"
                f"• **Modern Agriculture**: Combining traditional crop wisdom with drone technology and organic farming.\n"
                f"• **Infrastructure**: High-speed Vande Bharat trains and green energy solar parks connecting every state.\n"
                f"• **Cultural Roots**: Keeping our languages, classical arts, and festivals vibrant in every home.\n\n"
                f"What specific topic about India's modern news, space, or traditions would you like Ammachi to explain next, Chellam?"
            )

    # No images attached as per user request
    media_items = []

    # Attach relevant video if festival is mentioned
    videos = get_festival_youtube_videos(message, message, language)

    # Retrieve user profile
    user = crud.get_user_by_username(None, username)
    points = user.points if user else 0
    stamps = [s.stamp_name for s in user.stamps] if user else []

    return {
        "response": response_text,
        "points": points,
        "stamps": stamps,
        "media": media_items,
        "videos": videos
    }
