import os
import sys
import datetime

# Add the current directory to path
sys.path.append(os.getcwd())

try:
    import database
    from api import auth
    from models import LoginResponse
    print("Imports successful.")
    
    # Test DB init
    database.init_db()
    print("Database init successful.")
    
    # Test hashing
    from database import pwd_context
    h = pwd_context.hash("test")
    print(f"Hashing successful: {h[:10]}...")
    v = pwd_context.verify("test", h)
    print(f"Verification successful: {v}")
    
    # Test JWT
    import jwt
    SECRET_KEY = "test-secret"
    payload = {"username": "test", "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    print(f"JWT token generation type: {type(token)}")
    
    # Test Pydantic Model
    res = LoginResponse(
        success=True,
        message="Test",
        token=token,
        username="student"
    )
    print("Pydantic validation successful.")
    # Check if token in res is str
    if not isinstance(res.token, str):
        print(f"CRITICAL: Token in model is {type(res.token)}, expected str!")
    else:
        print("Model token is correctly a string.")

except Exception as e:
    import traceback
    traceback.print_exc()
