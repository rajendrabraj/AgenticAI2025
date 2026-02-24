import os
import sys
from pathlib import Path
from dotenv import load_dotenv


# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent))


load_dotenv()

#Load Env Variables
import os
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
