# # 1. Upgrade core installer tools
# !pip install -U pip setuptools wheel

# # 2. Install the main libraries without forcing broken versions
# # This allows pip to find versions that work together
# !pip install spacy nltk gradio beautifulsoup4 numpy scipy

# # 3. Download the specific models/data
# !python -m spacy download en_core_web_sm
# !pip install -U nltk
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')

# !pip install faiss-cpu

import spacy
import nltk

nltk.download("punkt")
