# Smoke test (to run locally after install).
import os, sys, platform, importlib.util
import os
from dotenv import load_dotenv
load_dotenv()

import os

load_dotenv() # This loads the variables from .env

# Access environment variables
api_key = os.getenv('GOOGLE_API_KEY')
print(f"API Key: {api_key}")

# (Optional) Create a .env file from the notebook for demo purposes only.
# In real projects, create this manually and NEVER commit the key.
from pathlib import Path

env_path = Path.cwd() / ".env"
print(env_path)

if not env_path.exists():
    env_path.write_text("GOOGLE_API_KEY=AIzaSyDbsRjBlMG3jI49q8lURFMK6i2DOrmu_Qw\n")
env_path.resolve()


print("Python:", sys.version)
print("Platform:", platform.platform())
print("GOOGLE_API_KEY set:", bool(os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")))

adk_spec = importlib.util.find_spec("adk")
print("ADK module found:", bool(adk_spec))
if not adk_spec:
    print("If False, ensure your venv is active and 'google-adk' is installed in it.")