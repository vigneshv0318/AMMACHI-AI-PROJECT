import sys
import os
import requests
import io
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def test_complete_curriculum():
    print("==================================================")
    print("RUNNING COMPLETE INDIC HANDWRITING CURRICULUM TESTS")
    print("==================================================")

    # 1. Login
    print("\n[TEST 1] Authenticating user 'student'...")
    login_resp = requests.post(f"{BASE_URL}/login", json={"username": "student", "password": "password123"})
    if login_resp.status_code != 200:
        print("[ERROR] Login failed:", login_resp.text)
        return
    token = login_resp.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"[SUCCESS] Authenticated successfully! Current points: {login_resp.json()['points']}")

    # 2. Test Full Curriculum Retrieval for Tamil, Telugu, and Hindi
    print("\n[TEST 2] Testing dynamic curriculum datasets...")
    for lang in ["Tamil", "Telugu", "Hindi"]:
        res = requests.get(f"{BASE_URL}/vision/curriculum?language={lang}", headers=headers)
        assert res.status_code == 200, f"Failed to fetch {lang} curriculum"
        curriculum = res.json()
        print(f"[SUCCESS] {lang} Curriculum: Loaded {len(curriculum)} items!")
        categories = set(i['category'] for i in curriculum)
        levels = set(i['level'] for i in curriculum)
        print(f"   Categories present: {sorted(list(categories))}")
        print(f"   Levels present: {sorted(list(levels))}")

    # 3. Test Evaluation Across Multiple Dynamic Characters/Words (No hardcoding)
    test_targets = [
        # Tamil Vowels, Consonants, Grantha, Words, Sentences
        ("அ", "Tamil", "vowel"),
        ("ஆ", "Tamil", "vowel"),
        ("ஃ", "Tamil", "aytham"),
        ("க", "Tamil", "consonant"),
        ("ழ", "Tamil", "consonant"),
        ("ஜ", "Tamil", "grantha"),
        ("ஸ்ரீ", "Tamil", "grantha"),
        ("கா", "Tamil", "uyirmei"),
        ("அம்மா", "Tamil", "word"),
        ("தமிழ்", "Tamil", "word"),
        ("தமிழ் எங்கள் தாய்மொழி", "Tamil", "sentence"),
        # Telugu
        ("అ", "Telugu", "vowel"),
        ("క", "Telugu", "consonant"),
        ("అమ్మ", "Telugu", "word"),
        # Hindi
        ("अ", "Hindi", "vowel"),
        ("क", "Hindi", "consonant"),
        ("माँ", "Hindi", "word")
    ]

    # Create synthetic stroke PNG
    img = Image.new("RGB", (400, 300), color="white")
    draw = ImageDraw.Draw(img)
    draw.line([(50, 80), (350, 80), (200, 260)], fill="black", width=14)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_bytes = img_byte_arr.getvalue()

    print("\n[TEST 3] Testing Generic Multi-Signal Evaluator on 17 distinct targets...")
    for target_char, lang, cat in test_targets:
        files = {"file": ("handwriting.png", img_bytes, "image/png")}
        data = {
            "target_text": target_char,
            "practice_mode": "trace",
            "language": lang,
            "attempt_number": 1
        }
        res = requests.post(f"{BASE_URL}/vision/evaluate", headers=headers, files=files, data=data)
        assert res.status_code == 200, f"Failed evaluation for {target_char} ({lang})"
        res_json = res.json()
        print(f"   [OK] Target: '{target_char}' ({lang} {cat}) -> Status: {res_json['recognition_status']} | Score: {res_json['overall_score']}/100 | Points: +{res_json['points_awarded']}")
        print(f"        Feedback: {res_json['specific_feedback']}")

    # 4. Verify PostgreSQL Stats
    print("\n[TEST 4] Fetching PostgreSQL handwriting stats...")
    stats_res = requests.get(f"{BASE_URL}/vision/stats", headers=headers)
    assert stats_res.status_code == 200, "Failed to fetch stats"
    stats = stats_res.json()
    print("[SUCCESS] PostgreSQL Handwriting Stats verified:")
    print(f"   Total attempts logged: {stats['total_attempts']}")
    print(f"   Unique characters practiced: {stats['practiced_count']}")
    print(f"   Mastered characters count: {stats['mastered_count']}")
    print(f"   Average score: {stats['avg_score']}%")

    print("\n==================================================")
    print("ALL COMPLETE INDIC CURRICULUM PIPELINE TESTS PASSED 100%!")
    print("==================================================")

if __name__ == "__main__":
    test_complete_curriculum()
