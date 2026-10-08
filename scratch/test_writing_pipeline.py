import sys
import os
import requests
import io
from PIL import Image, ImageDraw

# Set stdout encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def test_writing_pipeline():
    print("==================================================")
    print("RUNNING END-TO-END HANDWRITING PIPELINE TESTS")
    print("==================================================")

    # 1. Login to retrieve token
    print("\n[TEST 1] Authenticating user 'student'...")
    login_resp = requests.post(f"{BASE_URL}/login", json={"username": "student", "password": "password123"})
    if login_resp.status_code != 200:
        print("[ERROR] Login failed:", login_resp.text)
        return
    token = login_resp.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("[SUCCESS] Authenticated successfully! User points:", login_resp.json()["points"])

    # 2. Get Writing Lessons for Tamil, Telugu, and Hindi
    for lang in ["Tamil", "Telugu", "Hindi"]:
        print(f"\n[TEST 2] Fetching dynamic lessons for {lang}...")
        res = requests.get(f"{BASE_URL}/vision/lessons?language={lang}", headers=headers)
        assert res.status_code == 200, f"Failed to fetch {lang} lessons"
        lessons = res.json()
        print(f"[SUCCESS] {lang} lessons loaded: {len(lessons)} items (First item: {lessons[0]['char']} - {lessons[0]['meaning']})")

    # 3. Create dummy drawing PNG
    img = Image.new("RGB", (400, 300), color="white")
    draw = ImageDraw.Draw(img)
    draw.line([(50, 100), (200, 100), (125, 250)], fill="black", width=12)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_bytes = img_byte_arr.getvalue()

    # 4. Evaluate Handwriting in Trace, Guided, and Free Writing modes
    for mode in ["trace", "guided", "free"]:
        print(f"\n[TEST 3] Evaluating canvas attempt in '{mode}' mode...")
        files = {"file": ("handwriting.png", img_bytes, "image/png")}
        data = {
            "target_text": "அ",
            "practice_mode": mode,
            "language": "Tamil",
            "attempt_number": 1
        }
        res = requests.post(f"{BASE_URL}/vision/evaluate", headers=headers, files=files, data=data)
        assert res.status_code == 200, f"Failed evaluation in mode {mode}"
        result = res.json()
        print(f"[SUCCESS] Evaluation in '{mode}' mode successful!")
        print(f"   Target: {result['target']} | Detected: {result['detected']} | Overall Score: {result['overall_score']}/100")
        print(f"   Breakdown -> Char: {result['character_score']} | Shape: {result['shape_score']} | Stroke: {result['stroke_score']} | Alignment: {result['alignment_score']}")
        print(f"   Feedback: '{result['specific_feedback']}'")
        print(f"   Points awarded: +{result['points_awarded']} (Total user points: {result['total_points']})")

    # 5. Fetch PostgreSQL Handwriting Statistics
    print("\n[TEST 4] Fetching PostgreSQL handwriting stats from /vision/stats...")
    stats_res = requests.get(f"{BASE_URL}/vision/stats", headers=headers)
    assert stats_res.status_code == 200, "Failed to fetch handwriting stats"
    stats = stats_res.json()
    print("[SUCCESS] PostgreSQL Handwriting Stats fetched:")
    print(f"   Total attempts: {stats['total_attempts']}")
    print(f"   Practiced count: {stats['practiced_count']}")
    print(f"   Mastered count: {stats['mastered_count']}")
    print(f"   Average score: {stats['avg_score']}%")
    print(f"   Best character: {stats['best_character']} ({stats['best_character_score']}%)")

    print("\n==================================================")
    print("ALL HANDWRITING PIPELINE TESTS PASSED 100%!")
    print("==================================================")

if __name__ == "__main__":
    test_writing_pipeline()
