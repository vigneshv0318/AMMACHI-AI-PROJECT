import mediapipe as mp
try:
    print("MP dir:", dir(mp))
    print("Solutions available:", hasattr(mp, 'solutions'))
    import mediapipe.solutions
    print("Imported mediapipe.solutions successfully")
    print(dir(mediapipe.solutions))
except Exception as e:
    print(f"Error: {e}")
