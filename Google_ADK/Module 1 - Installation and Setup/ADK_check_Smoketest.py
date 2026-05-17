# Smoke test (to run locally after install).
import os, sys, platform, importlib.util
import os
from dotenv import load_dotenv
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()

import os

# Find the .env file, searching upwards in the directory tree
dotenv_path = find_dotenv()

# Load the .env file
load_dotenv(dotenv_path)

# Now you can access environment variables
print(f"Path to .env file: {dotenv_path}")



load_dotenv() # This loads the variables from .env

# Access environment variables
api_key = os.getenv('GOOGLE_API_KEY')
print(f"API Key: {api_key}")

# (Optional) Create a .env file from the notebook for demo purposes only.
# In real projects, create this manually and NEVER commit the key.
from pathlib import Path

# env_path = Path.cwd() / ".env"
# print(env_path)

# if not env_path.exists():
#     env_path.write_text("GOOGLE_API_KEY=AIzaSyDbsRjBlMG3jI49q8lURFMK6i2DOrmu_Qw\n")
# env_path.resolve()

print("-" * 90)
print("Python:", sys.version)
print("Platform:", platform.platform())
print("GOOGLE_API_KEY set:", bool(os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")))
print("-" * 90)

adk_spec = importlib.util.find_spec("adk")
print("ADK module found:", bool(adk_spec))
if not adk_spec:
    print("If False, ensure your venv is active and 'google-adk' is installed in it.")
    
    
import pkg_resources

try:
    version = pkg_resources.get_distribution("google-adk").version
    print("Google ADK Version:", version)
except pkg_resources.DistributionNotFound:
    print("Google ADK is not installed.")    
    
    
import importlib.util
print("-" * 90)
adk_spec = importlib.util.find_spec("google.adk")
print("-" * 90)
print("Google ADK module found:", bool(adk_spec))
print("-" * 90)
if adk_spec:
    print("Module location:", adk_spec.origin)
    print("-" * 90)
else:
    print("Google ADK is not installed.")    
    print("-" * 90)