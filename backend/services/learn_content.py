"""
Ammachi Learn-Path content: seed corpus + AI lesson generation.

Every exercise follows the Duolingo-style shapes observed on duolingo.com/learn:
- multiple_choice  : pick the right translation from 3-4 tiles
- translate        : word-bank sentence building (tap tiles in order)
- listen           : hear the native phrase (TTS), choose what you heard
- match            : tap pairs (word -> meaning)
- speak            : say the native phrase (voice module grades; skippable)
"""
import os
import json
import random
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("ammachi.learn_content")

# ============================================================
# SEED CORPUS  (works with zero API keys)
# ============================================================

SEED_CORPUS = {
    "Tamil": {
        "greeting": "Vanakkam",
        "words": [
            ["வணக்கம்", "Vanakkam", "Greeting / Hello"],
            ["நன்றி", "Nandri", "Thank you"],
            ["தண்ணீர்", "Thanneer", "Water"],
            ["அம்மா", "Amma", "Mother"],
            ["அப்பா", "Appa", "Father"],
            ["பாட்டி", "Paatti", "Grandmother"],
            ["சாப்பாடு", "Saapaadu", "Food / Meal"],
            ["பால்", "Paal", "Milk"],
            ["வீடு", "Veedu", "House"],
            ["புத்தகம்", "Puthagam", "Book"],
            ["பள்ளி", "Palli", "School"],
            ["நண்பா", "Nanba", "Friend"],
            ["ஒன்று", "Onru", "One"],
            ["இரண்டு", "Irantu", "Two"],
            ["மூன்று", "Moonru", "Three"],
            ["மலை", "Malai", "Mountain"],
            ["கடல்", "Kadal", "Sea"],
            ["மரம்", "Maram", "Tree"],
            ["பூ", "Poo", "Flower"],
            ["சூரியன்", "Sooriyan", "Sun"],
        ],
        "phrases": [
            ["வணக்கம், எப்படி இருக்கிறீர்கள்?", "Vanakkam, eppadi irukkeergal?", "Hello, how are you?"],
            ["என் பெயர் குமார்", "En peyar Kumar", "My name is Kumar"],
            ["இது தண்ணீர்", "Idhu thanneer", "This is water"],
            ["நன்றி அம்மா", "Nandri Amma", "Thank you, mother"],
            ["எனக்கு பசிக்கிறது", "Enakku pasikkiradhu", "I am hungry"],
            ["வருகிறேன்", "Varugiren", "I am coming"],
        ],
    },
    "Telugu": {
        "greeting": "Namaskaram",
        "words": [
            ["నమస్కారం", "Namaskaram", "Greeting / Hello"],
            ["ధన్యవాదాలు", "Dhanyavaadaalu", "Thank you"],
            ["నీరు", "Neeru", "Water"],
            ["అమ్మ", "Amma", "Mother"],
            ["నాన్న", "Naanna", "Father"],
            ["అమ్మమ్మ", "Ammamma", "Grandmother"],
            ["భోజనం", "Bhojanam", "Food / Meal"],
            ["పాలు", "Paalu", "Milk"],
            ["ఇల్లు", "Illu", "House"],
            ["పుస్తకం", "Pustakam", "Book"],
            ["పాఠశాల", "Paathashaala", "School"],
            ["స్నేహితుడు", "Snehitudu", "Friend"],
            ["ఒకటి", "Okati", "One"],
            ["రెండు", "Rendu", "Two"],
            ["మూడు", "Moodu", "Three"],
            ["కొండ", "Konda", "Mountain"],
            ["సముద్రం", "Samudram", "Sea"],
            ["చెట్టు", "Chettu", "Tree"],
            ["పువ్వు", "Puvvu", "Flower"],
            ["సూర్యుడు", "Sooryudu", "Sun"],
        ],
        "phrases": [
            ["నమస్కారం, మీరు ఎలా ఉన్నారు?", "Namaskaram, meeru ela unnaaru?", "Hello, how are you?"],
            ["నా పేరు కుమార్", "Naa peru Kumar", "My name is Kumar"],
            ["ఇది నీరు", "Idi neeru", "This is water"],
            ["ధన్యవాదాలు అమ్మా", "Dhanyavaadaalu Amma", "Thank you, mother"],
            ["నాకు ఆకలిగా ఉంది", "Naaku aakaligaa undi", "I am hungry"],
        ],
    },
    "Hindi": {
        "greeting": "Namaste",
        "words": [
            ["नमस्ते", "Namaste", "Greeting / Hello"],
            ["धन्यवाद", "Dhanyavaad", "Thank you"],
            ["पानी", "Paani", "Water"],
            ["माँ", "Maa", "Mother"],
            ["पिता", "Pita", "Father"],
            ["दादी", "Daadi", "Grandmother"],
            ["खाना", "Khaana", "Food / Meal"],
            ["दूध", "Doodh", "Milk"],
            ["घर", "Ghar", "House"],
            ["किताब", "Kitaab", "Book"],
            ["स्कूल", "School", "School"],
            ["दोस्त", "Dost", "Friend"],
            ["एक", "Ek", "One"],
            ["दो", "Do", "Two"],
            ["तीन", "Teen", "Three"],
            ["पहाड़", "Pahaad", "Mountain"],
            ["समुद्र", "Samudra", "Sea"],
            ["पेड़", "Ped", "Tree"],
            ["फूल", "Phool", "Flower"],
            ["सूरज", "Sooraj", "Sun"],
        ],
        "phrases": [
            ["नमस्ते, आप कैसे हैं?", "Namaste, aap kaise hain?", "Hello, how are you?"],
            ["मेरा नाम कुमार है", "Mera naam Kumar hai", "My name is Kumar"],
            ["यह पानी है", "Yah paani hai", "This is water"],
            ["धन्यवाद माँ", "Dhanyavaad Maa", "Thank you, mother"],
            ["मुझे भूख लगी है", "Mujhe bhookh lagi hai", "I am hungry"],
        ],
    },
    "Malayalam": {
        "greeting": "Namaskaram",
        "words": [
            ["നമസ്കാരം", "Namaskaram", "Greeting / Hello"],
            ["നന്ദി", "Nandi", "Thank you"],
            ["വെള്ളം", "Vellam", "Water"],
            ["അമ്മ", "Amma", "Mother"],
            ["അച്ഛൻ", "Achchan", "Father"],
            ["അമ്മൂമ്മ", "Ammoomma", "Grandmother"],
            ["ഭക്ഷണം", "Bhakshanam", "Food / Meal"],
            ["പാൽ", "Paal", "Milk"],
            ["വീട്", "Veedu", "House"],
            ["പുസ്തകം", "Pusthakam", "Book"],
            ["സ്കൂൾ", "School", "School"],
            ["സുഹൃത്ത്", "Suhrid", "Friend"],
            ["ഒന്ന്", "Onnu", "One"],
            ["രണ്ട്", "Randu", "Two"],
            ["മൂന്ന്", "Moonnu", "Three"],
            ["മല", "Mala", "Mountain"],
            ["കടൽ", "Kadal", "Sea"],
            ["മരം", "Maram", "Tree"],
            ["പൂവ്", "Poovu", "Flower"],
            ["സൂര്യൻ", "Sooryan", "Sun"],
        ],
        "phrases": [
            ["നമസ്കാരം, സുഖമാണോ?", "Namaskaram, sukhamaano?", "Hello, how are you?"],
            ["എന്റെ പേര് കുമാർ", "Ente peru Kumar", "My name is Kumar"],
            ["ഇത് വെള്ളമാണ്", "Ithu vellamaanu", "This is water"],
            ["നന്ദി അമ്മ", "Nandi Amma", "Thank you, mother"],
        ],
    },
    "Kannada": {
        "greeting": "Namaskara",
        "words": [
            ["ನಮಸ್ಕಾರ", "Namaskara", "Greeting / Hello"],
            ["ಧನ್ಯವಾದ", "Dhanyavaada", "Thank you"],
            ["ನೀರು", "Neeru", "Water"],
            ["ಅಮ್ಮ", "Amma", "Mother"],
            ["ಅಪ್ಪ", "Appa", "Father"],
            ["ಅಜ್ಜಿ", "Ajji", "Grandmother"],
            ["ಊಟ", "Oota", "Food / Meal"],
            ["ಹಾಲು", "Haalu", "Milk"],
            ["ಮನೆ", "Mane", "House"],
            ["ಪುಸ್ತಕ", "Pusthaka", "Book"],
            ["ಶಾಲೆ", "Shaale", "School"],
            ["ಸ್ನೇಹಿತ", "Snehita", "Friend"],
            ["ಒಂದು", "Ondu", "One"],
            ["ಎರಡು", "Eradu", "Two"],
            ["ಮೂರು", "Moonu", "Three"],
            ["ಬೆಟ್ಟ", "Betta", "Mountain"],
            ["ಸಮುದ್ರ", "Samudra", "Sea"],
            ["ಮರ", "Mara", "Tree"],
            ["ಹೂವು", "Hoovu", "Flower"],
            ["ಸೂರ್ಯ", "Soorya", "Sun"],
        ],
        "phrases": [
            ["ನಮಸ್ಕಾರ, ಹೇಗಿದ್ದೀರಾ?", "Namaskara, hegiddira?", "Hello, how are you?"],
            ["ನನ್ನ ಹೆಸರು ಕುಮಾರ್", "Nanna hesaru Kumar", "My name is Kumar"],
            ["ಇದು ನೀರು", "Idu neeru", "This is water"],
            ["ಧನ್ಯವಾದ ಅಮ್ಮ", "Dhanyavaada Amma", "Thank you, mother"],
        ],
    },
}

# Per-unit blueprints: title, description + ordered nodes (order, node_type, topic)
UNIT_BLUEPRINTS = [
    {
        "title": "Basics 1",
        "description": "Say hello, thank you and the words you meet every day.",
        "nodes": [
            (1, "lesson", "greetings"), (2, "lesson", "greetings"), (3, "story", "greetings"),
            (4, "lesson", "family"), (5, "practice", "greetings"), (6, "chest", "greetings"),
            (7, "lesson", "family"), (8, "lesson", "family"), (9, "practice", "family"),
            (10, "chest", "family"), (11, "unit_review", "greetings"),
        ],
    },
    {
        "title": "Basics 2",
        "description": "Talk about your family and the people you love.",
        "nodes": [
            (1, "lesson", "family"), (2, "lesson", "family"), (3, "story", "family"),
            (4, "lesson", "food"), (5, "practice", "family"), (6, "chest", "family"),
            (7, "lesson", "food"), (8, "practice", "food"), (9, "story", "family"),
            (10, "chest", "food"), (11, "unit_review", "family"),
        ],
    },
    {
        "title": "Everyday Words",
        "description": "Names for things around you — home, school and friends.",
        "nodes": [
            (1, "lesson", "everyday"), (2, "lesson", "everyday"), (3, "practice", "everyday"),
            (4, "chest", "everyday"), (5, "lesson", "everyday"), (6, "story", "everyday"),
            (7, "lesson", "nature"), (8, "practice", "nature"), (9, "chest", "nature"),
            (10, "story", "everyday"), (11, "unit_review", "everyday"),
        ],
    },
    {
        "title": "Food & Favorites",
        "description": "Meals, milk, fruits — the yum words.",
        "nodes": [
            (1, "lesson", "food"), (2, "lesson", "food"), (3, "practice", "food"),
            (4, "chest", "food"), (5, "story", "food"), (6, "lesson", "food"),
            (7, "lesson", "everyday"), (8, "practice", "food"), (9, "story", "food"),
            (10, "chest", "food"), (11, "unit_review", "food"),
        ],
    },
    {
        "title": "Numbers & Nature",
        "description": "Count one-two-three and meet the sun, sea and mountains.",
        "nodes": [
            (1, "lesson", "nature"), (2, "lesson", "nature"), (3, "story", "nature"),
            (4, "chest", "nature"), (5, "practice", "nature"), (6, "lesson", "nature"),
            (7, "lesson", "everyday"), (8, "practice", "everyday"), (9, "chest", "everyday"),
            (10, "story", "nature"), (11, "unit_review", "nature"),
        ],
    },
]

TOPIC_TITLE = {
    "greetings": "Introduce yourself",
    "family": "Meet the family",
    "food": "Food & Favorites",
    "everyday": "Everyday words",
    "nature": "Numbers & Nature",
}


def _default_units(language: str) -> List[Dict[str, Any]]:
    return [
        {
            "language": language,
            "order": idx + 1,
            "title": bp["title"],
            "description": bp["description"],
            "nodes": [{"order": o, "node_type": t, "topic": topic} for (o, t, topic) in bp["nodes"]],
        }
        for idx, bp in enumerate(UNIT_BLUEPRINTS)
    ]


# ============================================================
# EXERCISE GENERATORS (seed-based)
# ============================================================

def _corpus_for(language: str) -> Dict[str, Any]:
    return SEED_CORPUS.get(language) or SEED_CORPUS["Tamil"]


def _exercise_multiple_choice(word: List, distractors: List[List]) -> Dict[str, Any]:
    options = [d[2] for d in distractors[:3]] + [word[2]]
    random.shuffle(options)
    answer_index = options.index(word[2])
    return {
        "id": f"mc_{word[1]}_{random.randint(1000, 9999)}",
        "type": "multiple_choice",
        "prompt": "What does this mean?",
        "native_text": word[0],
        "transliteration": word[1],
        "options": options,
        "answer_index": answer_index,
        "explanation": f"{word[0]} ({word[1]}) means “{word[2]}”.",
    }


def _exercise_translate(phrase: List, language: str) -> Dict[str, Any]:
    english_words = phrase[2].split()
    # Word bank: correct words + 2-3 decoys from other phrases
    decoy_pool = []
    for p in _corpus_for(language)["phrases"]:
        for w in p[2].split():
            if w.lower() not in {x.lower() for x in english_words}:
                decoy_pool.append(w)
    random.shuffle(decoy_pool)
    bank = english_words + decoy_pool[:3]
    random.shuffle(bank)
    return {
        "id": f"tr_{random.randint(1000, 9999)}",
        "type": "translate",
        "prompt": "Write this in English",
        "native_text": f"{phrase[0]} ({phrase[1]})",
        "bank": bank,
        "answer_words": english_words,
        "explanation": f"“{phrase[0]}” ({phrase[1]}) means “{phrase[2]}”.",
    }


def _exercise_listen(phrase: List, distractor_phrases: List[List]) -> Dict[str, Any]:
    options = [p[2] for p in distractor_phrases[:2]] + [phrase[2]]
    random.shuffle(options)
    answer_index = options.index(phrase[2])
    return {
        "id": f"li_{random.randint(1000, 9999)}",
        "type": "listen",
        "prompt": "Tap what you hear",
        "native_text": phrase[0],
        "transliteration": phrase[1],
        "options": options,
        "answer_index": answer_index,
        "explanation": f"You heard: “{phrase[2]}” ({phrase[1]}).",
    }


def _exercise_match(language: str, topic: str) -> Dict[str, Any]:
    corpus = _corpus_for(language)
    picked = random.sample(corpus["words"], 4)
    pairs = [
        {"native": w[0], "translit": w[1], "english": w[2]}
        for w in picked
    ]
    return {
        "id": f"mt_{random.randint(1000, 9999)}",
        "type": "match",
        "prompt": "Tap the pairs",
        "pairs": pairs,
        "explanation": "Tap a native word, then its English meaning.",
    }


def _exercise_speak(phrase: List) -> Dict[str, Any]:
    return {
        "id": f"sp_{random.randint(1000, 9999)}",
        "type": "speak",
        "prompt": "Speak this sentence",
        "native_text": phrase[0],
        "transliteration": phrase[1],
        "english": phrase[2],
        "explanation": f"“{phrase[0]}” ({phrase[1]}) means “{phrase[2]}”.",
    }


def build_seed_exercises(node_type: str, topic: str, language: str) -> List[Dict[str, Any]]:
    """Deterministic-ish seed lesson content from the corpus. Used as offline fallback."""
    corpus = _corpus_for(language)
    rng = random.Random(f"{language}-{node_type}-{topic}")
    exercises: List[Dict[str, Any]] = []
    words = corpus["words"]
    phrases = corpus["phrases"] or [[w[0], w[1], f"{w[1]} — {w[2]}"] for w in words[:4]]

    # A stable shuffle driven by topic/node
    words_shuf = words[:]
    phrases_shuf = phrases[:]
    rng.shuffle(words_shuf)
    rng.shuffle(phrases_shuf)

    if node_type == "story":
        # Story = reading: a short phrase chain (translate + listen mix)
        for i, phrase in enumerate(phrases_shuf[:3]):
            exercises.append(_exercise_listen(phrase, [p for j, p in enumerate(phrases_shuf) if j != i][:2] or phrases_shuf[:2]))
            exercises.append(_exercise_translate(phrase, language))
        return exercises

    if node_type in ("practice", "unit_review", "chest") or node_type == "lesson":
        # Mixed lesson: 6 exercises like Duolingo's bite-sized loop
        for i in range(2):
            w = words_shuf[i]
            distractors = [x for x in words_shuf if x[1] != w[1]]
            rng.shuffle(distractors)
            exercises.append(_exercise_multiple_choice(w, distractors[:3]))
        exercises.append(_exercise_match(language, topic))
        exercises.append(_exercise_listen(phrases_shuf[0], phrases_shuf[1:3]))
        exercises.append(_exercise_translate(phrases_shuf[0], language))
        exercises.append(_exercise_speak(phrases_shuf[1] if len(phrases_shuf) > 1 else phrases_shuf[0]))
    return exercises


# ============================================================
# AI GENERATION (Gemini / Groq) with seed fallback
# ============================================================

async def generate_lesson_exercises(node_type: str, topic: str, language: str) -> List[Dict[str, Any]]:
    """
    Try AI generation first (when keys are configured); validate strictly and
    fall back to seed content otherwise. Mirrors challenge_ai.py patterns.
    """
    if os.getenv("AMMACHI_DISABLE_AI_LESSONS", "").lower() in {"1", "true", "yes"}:
        return build_seed_exercises(node_type, topic, language)

    try:
        from services.gemini_service import get_llm_client, invoke_direct_llm, GEMINI_API_KEY, GROQ_API_KEY
    except Exception:
        return build_seed_exercises(node_type, topic, language)

    corpus = _corpus_for(language)
    sample_words = "\n".join(f"- {w[0]} ({w[1]}) = {w[2]}" for w in corpus["words"][:12])
    sample_phrases = "\n".join(f"- {p[0]} ({p[1]}) = {p[2]}" for p in corpus["phrases"])

    system_prompt = (
        "You create Duolingo-style language lesson exercises for children learning "
        f"{language} from English. Reply ONLY with a JSON array. Each item is an object with type "
        "one of 'multiple_choice' | 'translate' | 'listen' | 'match' | 'speak' and these fields: "
        "id (unique string), prompt (short instruction in English), native_text, transliteration, "
        "options (list of 3-4 English strings, for multiple_choice/listen), answer_index (int), "
        "bank (list of words incl. decoys, for translate), answer_words (correct English words list), "
        "pairs (for match: list of {native, translit, english}), english (for speak), "
        "explanation (one short friendly sentence). "
        "Use ONLY simple vocabulary suitable for children. Keep native_text consistent with the corpus below.\n"
        f"Corpus words:\n{sample_words}\nCorpus phrases:\n{sample_phrases}"
    )
    user_prompt = (
        f"Create a {node_type} lesson about '{TOPIC_TITLE.get(topic, topic)}' ({topic}) in {language}. "
        "Return exactly 6 exercises mixing all exercise types."
    )

    raw_text = None
    try:
        client = get_llm_client()
        if client is not None:
            from langchain_core.messages import SystemMessage, HumanMessage
            resp = client.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
            raw_text = getattr(resp, "content", None)
        elif (GROQ_API_KEY or GEMINI_API_KEY):
            raw_text = invoke_direct_llm(system_prompt, user_message=user_prompt)
    except Exception as e:
        logger.warning("AI lesson generation failed: %s", e)

    exercises = _parse_ai_exercises(raw_text)
    if exercises and len(exercises) >= 3:
        return exercises
    return build_seed_exercises(node_type, topic, language)


def _parse_ai_exercises(raw_text: Optional[str]) -> List[Dict[str, Any]]:
    if not raw_text:
        return []
    try:
        text = raw_text.strip()
        if text.startswith("```"):
            text = text.split("```")[1] if "```" in text[3:] else text
            if text.startswith("json"):
                text = text[4:]
        start, end = text.find("["), text.rfind("]")
        if start == -1 or end == -1:
            return []
        data = json.loads(text[start:end + 1])
        valid = []
        for ex in data:
            etype = ex.get("type")
            if etype not in {"multiple_choice", "translate", "listen", "match", "speak"}:
                continue
            if not str(ex.get("native_text", "")).strip():
                continue
            if etype in {"multiple_choice", "listen"} and ("options" not in ex or "answer_index" not in ex):
                continue
            if etype == "translate" and ("bank" not in ex or "answer_words" not in ex):
                continue
            if etype == "match" and not ex.get("pairs"):
                continue
            ex.setdefault("id", f"ai_{random.randint(1000, 999999)}")
            ex.setdefault("explanation", "")
            ex.setdefault("prompt", {
                "multiple_choice": "What does this mean?",
                "translate": "Write this in English",
                "listen": "Tap what you hear",
                "match": "Tap the pairs",
                "speak": "Speak this sentence",
            }[etype])
            valid.append(ex)
        return valid
    except Exception as e:
        logger.warning("AI exercise parse failed: %s", e)
        return []
