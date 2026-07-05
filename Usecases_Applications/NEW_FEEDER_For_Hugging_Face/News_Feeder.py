## This program processed the RSS news feeds reads them and sends daily email
## Rajendra Bichu  (Date : 5th April 2026)


import feedparser
import feedparser
from matplotlib import text
#from oxmsg import message
import pandas as pd
from datetime import datetime
import hashlib
import html

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os

from send_email_Tool import send_email


## Start Logging Information to log    
script_path = os.path.abspath(__file__)
# Get the directory name from the script path
script_dir = os.path.dirname(script_path)
# Get the parent directory using os.pardir ('..')
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
print(f"Parent directory path: {parent_directory}")
OUTPUT_CSV_FILE = os.path.join(parent_directory, "daily_ai_news.CSV")
OUTPUT_HTML_FILE = os.path.join(parent_directory, "daily_ai_news.html")


#data_directory_path = os.path.join(parent_directory, "data")
#print(f"Data directory path: {data_directory_path}")


print(f"Output CSV Path: {OUTPUT_CSV_FILE} \n \n ")
logging.info(f"[NEWSFEEDER BOT : ] Output CSV Path: {OUTPUT_CSV_FILE}")
print(f"Output HTML Path: {OUTPUT_HTML_FILE} \n \n ")
logging.info(f"[NEWSFEEDER BOT : ] Output HTML Path: {OUTPUT_HTML_FILE}")


# logging.basicConfig(
#     filename=os.path.join(parent_directory, "NewsFeederTask_LOG.log"),
#     format="%(asctime)s | %(levelname)s | %(message)s",
#     level=logging.INFO
# )

log_file_path = os.path.join(parent_directory, "NewsFeederTask_LOG.log") 
print(f"Log file path: {log_file_path}")


logging.basicConfig(
    filename= log_file_path,
    filemode='a',
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    force=True
)




RSS_FEEDS = [
    "https://cloud.google.com/blog/topics/ai-ml/rss/",
    "https://blogs.nvidia.com/feed/",
    "https://aws.amazon.com/blogs/aws/feed/",
    "https://techcommunity.microsoft.com/t5/azure-ai/bg-p/AzureAI/rss",
    "https://planet-ai.net/rss.xml",
    "https://openai.com/blog/rss.xml",
    "https://www.anthropic.com/news/rss",
    "https://azure.microsoft.com/en-us/blog/feed/",
    "https://aws.amazon.com/blogs/machine-learning/feed/",
    "https://developer.nvidia.com/blog/feed/",
    "https://blogs.nvidia.com/feed/",
    "https://www.uber.com/blog/engineering/feed/",
    "https://www.uber.com/blog/ai/feed/",
    "https://bair.berkeley.edu/blog/feed.xml",
    "https://ai.googleblog.com/feeds/posts/default",
    "https://deepmind.google/blog/rss.xml",
    "https://machinelearning.apple.com/rss.xml",
    "https://machinelearningmastery.com/feed/",
    "https://towardsdatascience.com/feed",
    "https://pub.towardsai.net/feed",
    "https://neptune.ai/blog/rss.xml",
    "https://huggingface.co/blog/feed.xml",
    "https://venturebeat.com/category/ai/feed/",
    "https://the-decoder.com/feed/",
    "https://theaiinsider.tech/feed/",
    "https://www.analyticsvidhya.com/blog/feed/",
    "https://www.marktechpost.com/feed/",
    "http://arxiv.org/rss/cs.LG",
    "https://news.mit.edu/rss/topic/artificial-intelligence",
    "https://www.csail.mit.edu/rss.xml",
    "https://cloud.google.com/blog/topics/ai-ml/rss/",
    "https://aws.amazon.com/blogs/aws/feed/",
    "https://techcommunity.microsoft.com/t5/azure-ai/bg-p/AzureAI/rss",
    "https://planet-ai.net/rss.xml",
    "https://developer.nvidia.com/blog/feed/",
    "https://blogs.nvidia.com/feed/"

    ]

RSS_CATEGORIES = {

    "AI Research": [
        "https://huggingface.co/blog/feed.xml",
        "https://machinelearningmastery.com/feed/",
        "https://towardsdatascience.com/feed",
        "https://bair.berkeley.edu/blog/feed.xml",
        "http://arxiv.org/rss/cs.LG"
    ],

    "AI Companies": [
        "https://openai.com/blog/rss.xml",
        "https://www.anthropic.com/news/rss",
        "https://deepmind.google/blog/rss.xml",
        "https://blogs.nvidia.com/feed/",
        "https://developer.nvidia.com/blog/feed/"
    ],

    "Cloud AI": [
        "https://cloud.google.com/blog/topics/ai-ml/rss/",
        "https://aws.amazon.com/blogs/machine-learning/feed/",
        "https://techcommunity.microsoft.com/t5/azure-ai/bg-p/AzureAI/rss",
        "https://azure.microsoft.com/en-us/blog/feed/"
    ],

    "AI News": [
        "https://venturebeat.com/category/ai/feed/",
        "https://the-decoder.com/feed/",
        "https://www.marktechpost.com/feed/",
        "https://theaiinsider.tech/feed/"
    ],

    "AI Community": [
        "https://pub.towardsai.net/feed",
        "https://planet-ai.net/rss.xml"
    ],
    
    
    "Loop Engineering": [
        "https://huggingface.co/blog/feed.xml",
        "https://pub.towardsai.net/feed",
        "https://towardsdatascience.com/feed",
        "https://www.marktechpost.com/feed/",
        "https://machinelearningmastery.com/feed/",
        "https://bair.berkeley.edu/blog/feed.xml",
        "https://planet-ai.net/rss.xml"
    ],
    
    "AI Research": [
        "https://huggingface.co/blog/feed.xml",
        "https://machinelearningmastery.com/feed/",
        "https://towardsdatascience.com/feed",
        "https://bair.berkeley.edu/blog/feed.xml",
        "http://arxiv.org/rss/cs.LG"
    ],


    "Foundation Models": [
        "https://openai.com/blog/rss.xml",
        "https://www.anthropic.com/news/rss",
        "https://deepmind.google/blog/rss.xml",
        "https://huggingface.co/blog/feed.xml"
    ],

    "Cloud AI": [
        "https://cloud.google.com/blog/topics/ai-ml/rss/",
        "https://aws.amazon.com/blogs/machine-learning/feed/",
        "https://aws.amazon.com/blogs/aws/feed/",
        "https://techcommunity.microsoft.com/t5/azure-ai/bg-p/AzureAI/rss",
        "https://azure.microsoft.com/en-us/blog/feed/"
    ],

    "Hardware & Infrastructure": [
        "https://developer.nvidia.com/blog/feed/",
        "https://blogs.nvidia.com/feed/"
    ],

    "Big Tech AI": [
        "https://ai.googleblog.com/feeds/posts/default",
        "https://machinelearning.apple.com/rss.xml",
        "https://www.uber.com/blog/ai/feed/",
        "https://www.uber.com/blog/engineering/feed/"
    ],

    "AI Research": [
        "https://bair.berkeley.edu/blog/feed.xml",
        "https://www.csail.mit.edu/rss.xml",
        "https://news.mit.edu/rss/topic/artificial-intelligence",
        "https://planet-ai.net/rss.xml",
        "http://arxiv.org/rss/cs.LG"
    ],

    "AI News": [
        "https://venturebeat.com/category/ai/feed/",
        "https://the-decoder.com/feed/",
        "https://theaiinsider.tech/feed/"
    ],

    "AI Tutorials & Learning": [
        "https://machinelearningmastery.com/feed/",
        "https://towardsdatascience.com/feed",
        "https://pub.towardsai.net/feed",
        "https://www.analyticsvidhya.com/blog/feed/",
        "https://neptune.ai/blog/rss.xml",
        "https://www.marktechpost.com/feed/"
    ],

      
}

##Keywords to filter relevant AI news articles


KEYWORDS = [
"llm","github", "gpt", "rag", "retrieval", "claude",  "anthropic", "openai", "transformer", "ai agent", "deep learning", "machine learning", "artificial intelligence", "neural network", "natural language processing", "computer vision", "reinforcement learning", "generative ai", "diffusion model", "multimodal ai", "self-supervised learning", "unsupervised learning", "supervised learning", "few-shot learning", "zero-shot learning",
"generative ai", "diffusion model", "multimodal ai", "self-supervised learning", "unsupervised learning", "supervised learning", "few-shot learning", "zero-shot learning",
"RAG","LLM","GPT","Transformer","AI Agent","Deep Learning","Machine Learning","Artificial Intelligence","Neural Network","Natural Language Processing","Computer Vision","Reinforcement Learning","Generative AI","Diffusion Model","Multimodal AI","Self-Supervised Learning","Unsupervised Learning","Supervised Learning","Few-Shot Learning","Zero-Shot Learning","trend","machine","python","feature","model","dataset","training","inference","deployment","scaling","optimization","benchmark","evaluation","research","development","application","use case","industry","business","ethics","regulation"    ,
"agent","vector","database","embedding","retrieval","knowledge graph","reasoning","planning","tool use","memory","multi-modal","vision","language","code","audio","video","reinforcement learning","supervised learning","unsupervised learning","self-supervised learning","few-shot learning","zero-shot learning","transfer learning","continual learning","federated learning"
"architeure","framework","library","platform","service","API","open source","proprietary","cloud","on-premise","edge","hardware","GPU","TPU","ASIC","FPGA","quantum computing",
"agents","tool use","memory","multi-modal","vision","language","code","audio","video","reinforcement learning","supervised learning","unsupervised learning","self-supervised learning","few-shot learning","zero-shot learning","transfer learning","continual learning","federated learning"
"ai","AI","AI News","Anthropic","OpenAI","facebook","meta","google","deepmind","microsoft","azure","amazon","aws","nvidia","tesla","elon musk","sam altman","sundar pichai","satya nadella","mark zuckerberg",
"openAI","data science","security""ChatGPT","Bard","Gemini","Claude","LLaMA","Falcon","Mistral","Gemini Pro","Gemini Ultra","Gemini 1.5 Pro","Gemini 1.5 Ultra",
"AI-driven","AI-powered","AI-based","AI-enabled","AI-assisted","AI-enhanced","AI-optimized","AI-integrated","AI-centric","AI-first","AI-native","AI-focused","AI-led","AI-driven innovation","AI-powered solutions","AI-based applications","AI-enabled services","AI-assisted tools","AI-enhanced capabilities","AI-optimized performance","AI-integrated systems","AI-centric approach","AI-first strategy","AI-native development","AI-focused research","AI-led initiatives"
"AI","Artificial Intelligence","Generative AI","GenAI","LLM","Large Language Models","Foundation Models","Multimodal AI","Diffusion Models",
"Neural Networks","Deep Learning","Machine Learning","NLP","Natural Language Processing","Computer Vision","Speech AI",
"Text-to-Image","Text-to-Video","Text-to-Speech","AI Agents","Agentic AI","Autonomous Agents",
"RAG","Retrieval Augmented Generation","Vector Databases","Embeddings","Semantic Search","Prompt Engineering","Fine-tuning",
"Model Training","Inference","Open Source AI","AI Safety","AI Alignment","Responsible AI","Explainable AI","XAI","AI Ethics",
"AI Regulation","AI Policy","AI Startups","AI Research","AI Breakthroughs","AI Applications","Enterprise AI",
"AI Tools","AI Automation","AI Assistants","Copilots","Chatbots","Conversational AI","AI Hardware","GPUs","AI Chips","Edge AI",
"On-device AI","AI Infrastructure",
"MLOps","AIOps","Data Science","Big Data","Synthetic Data","Reinforcement Learning","Transfer Learning","Zero-shot Learning",
"Few-shot Learning","AGI","Artificial General Intelligence","Superintelligence","AI Trends","AI News","AI Innovations",
"AI Products","AI Platforms","AI APIs","AI Integration","AI Ecosystem","AI Market","AI Investments","AI Funding",
"AI Acquisitions","AI Partnerships","AI Benchmarks","AI Evaluation","AI Security","Adversarial AI","AI Governance",
"Human-AI Interaction","Claude AI","Anthropic Claude","Claude Opus","Claude Sonnet","Claude Code","Claude Computer Use",
"Claude Agents","Claude API","Claude MCP","Model Context Protocol","Anthropic AI","ChatGPT","OpenAI GPT","GPT-4o","GPT-5",
"OpenAI Codex","OpenAI Sora","DALL·E","OpenAI API","Gemini AI","Google Gemini","Gemini Pro","Gemini Ultra",
"Gemini Multimodal","Microsoft Copilot","GitHub Copilot","Copilot Studio","Azure AI","MAI Models","Perplexity AI",
"Perplexity Search","DeepSeek","DeepSeek LLM","Meta Llama","Llama 3","LlamaIndex","Mistral AI","Mixtral",
"Cohere AI","Command R","Falcon LLM","Qwen AI","ERNIE AI","Character AI","Janitor AI","Pi AI","Inflection AI",
"YouChat","Phind AI","Kimi AI","Groq AI","Groq LPU","Hugging Face","Hugging Face Transformers","Hugging Face Hub",
"LangChain","LangGraph","CrewAI","AutoGen","Agent Frameworks","Multi-Agent Systems","AI Orchestration","Agent Workflow",
"AI Automation Tools","AI SaaS","AI Platforms","AI APIs","AI Marketplaces","Prompt Engineering Tools","Prompt Marketplaces",
"AI Plugins","AI Extensions","AI SDK","AI Dev Tools",
"AI Coding Assistants","Cursor AI","Replit AI","Codeium","Tabnine","Sourcegraph Cody","AI IDE","AI Pair Programming",
"AI Design Tools","Midjourney","Stable Diffusion","Adobe Firefly","Canva AI","Runway ML","Pika Labs","Synthesia",
"HeyGen","ElevenLabs","PlayHT","Descript AI","NotebookLM","Notion AI","Grammarly AI","Jasper AI","Writesonic",
"Copy.ai","Gamma AI","Tome AI","Beautiful.ai","Framer AI","Webflow AI","Bubble AI","Vercel AI","v0 AI","Lovable AI","Zapier AI",
"Make AI","AI Automation Platforms","AI Agents Marketplace","AI App Builders","No-code AI","Low-code AI",
"AI Workflows","AI Assistants","AI Copilots","AI Search Engines","AI Browsers","AI Knowledge Tools","AI Research Tools",
"AI Summarization","AI Transcription","Speech-to-Text AI","Voice AI","Text-to-Speech AI","Multimodal AI Tools","Vision AI",
"Video Generation AI","Image Generation AI","AI Content Creation","AI Marketing Tools","AI SEO Tools","AI Analytics",
"AI BI Tools","AI Data Platforms","Vector DB","Pinecone","Weaviate","Chroma DB","FAISS","Embeddings API","Semantic Retrieval",
"Hybrid Search","Knowledge Graph AI","RAG Systems","RAG Pipelines","RAG Frameworks","Retrieval Systems","AI Indexing",
"AI Memory","Long Context Models","Context Window","Agent Memory","Tool Use AI","Function Calling","AI Tool Use",
"AI Plugins Ecosystem","AI Integrations","Enterprise AI","AI Productivity Tools","AI Collaboration Tools",
"AI Workspace","AI OS","AI Infrastructure","AI Compute","GPU AI","AI Chips","NVIDIA AI","CUDA AI","Edge AI",
"On-device AI","TinyML","AI Deployment","AI Inference","AI Training","Fine-tuned Models","Custom LLMs","Domain-specific AI",
"Vertical AI","AI Startups","AI Unicorns","AI Funding","AI Ecosystem","AI Trends","AI News","AI Breakthroughs","AI Benchmarks",
"LMArena","AI Evaluation","AI Leaderboards","AI Safety","AI Alignment","Responsible AI","AI Governance","AI Regulation",
"AI Policy","AI Ethics","Explainable AI","XAI","AI Security","Adversarial AI","AI Risk","AGI",
"Artificial General Intelligence","Superintelligence","Agentic Workflows","Autonomous AI","Self-driving Agents",
"Human-in-the-loop AI","AI Collaboration","Human-AI Interaction"

]

# CATEGORY_KEYWORDS = {

#     "LLMs": [
#         "gpt",
#         "llm",
#         "claude",
#         "gemini",
#         "mistral",
#         "llama"
#     ],

#     "Agents": [
#         "agent",
#         "autonomous",
#         "crewai",
#         "langgraph",
#         "autogen"
#     ],

#     "Research": [
#         "paper",
#         "arxiv",
#         "benchmark",
#         "dataset",
#         "training"
#     ],

#     "Cloud": [
#         "aws",
#         "azure",
#         "google cloud",
#         "bedrock",
#         "vertex ai"
#     ],

#     "Hardware": [
#         "gpu",
#         "nvidia",
#         "cuda",
#         "chip",
#         "ai accelerator"
#     ]
# }



CATEGORY_KEYWORDS = {

    # =====================================================
    # LLMs & Foundation Models
    # =====================================================
    "LLMs": [
        "llm","large language model","foundation model",
        "gpt","gpt-4","gpt-4o","gpt-5","chatgpt",

        "claude haiku","anthropic",
        "gemini","gemini pro","gemini ultra",
        "llama","llama 2","llama 3","llama 4",
        "mistral","mixtral",
        "deepseek","qwen","phi","falcon",
        "cohere","command-r","ernie","kimi",
        "reasoning model","thinking model"
    ],

    # =====================================================
    # AI Agents
    # =====================================================
    "AI Agents": [
        "agent","agents",
        "ai agent",
        "agentic ai",
        "autonomous agent",
        "multi-agent",
        "agentic workflow",
        "workflow",
        "agent workflow",
        "agent orchestration",
        "planning",
        "memory",
        "reasoning",
        "browser agent",
        "web agent"
    ],

    # =====================================================
    # Agent Frameworks
    # =====================================================
    "Agent Frameworks": [
        "langchain",
        "langgraph",
        "crewai",
        "autogen",
        "openai agents sdk",
        "agent sdk",
        "agent framework",
        "agent runtime",
        "agent protocol",
        "agent platform"
    ],

    # =====================================================
    # MCP & A2A
    # =====================================================
    "MCP / A2A": [
        "mcp",
        "model context protocol",
        "mcp server",
        "a2a",
        "agent-to-agent",
        "computer use",
        "tool use",
        "tool calling",
        "function calling",
        "claude computer use",
        "claude code"
    ],

    # =====================================================
    # RAG & Context Engineering
    # =====================================================
    "RAG": [
        "rag",
        "retrieval augmented generation",
        "vector rag",
        "vectorless rag",
        "vector-less rag",
        "graph rag",
        "graphrag",
        "adaptive rag",
        "context engineering",

        "knowledge graph",
        "semantic search",
        "vector search",
        "vector database",
        "embedding",
        "embeddings",
        "retrieval",
        "reranker",
        "reranking",
        "chunking",
        "long context",
        "context window"
    ],

    # =====================================================
    # AI Research
    # =====================================================
    "Research": [
        "paper",
        "research",
        "deep research",
        "arxiv",
        "benchmark",
        "leaderboard",
        "dataset",
        "synthetic data",
        "evaluation",
        "training",
        "pretraining",
        "fine tuning",
        "finetuning",
        "alignment",
        "rlhf",
        "dpo",
        "reinforcement learning",
        "deep learning",
        "machine learning",
        "multimodal",
        "diffusion",
        "transformer",
        "attention",
        "neural network",
        "vision language model",
        "vlm",
        "inference"
    ],

    # =====================================================
    # AI Coding
    # =====================================================
    "AI Coding": [
        "cursor",
        "windsurf",
        "claude code",
        "github copilot",
        "copilot",
        "codex",
        "codeium",
        "tabnine",
        "replit",
        "bolt.new",
        "bolt",
        "lovable",
        "v0",
        "developer",
        "software engineering",
        "pair programming",
        "sdk",
        "api",
        "vs code",
        "ide"
    ],

    # =====================================================
    # AI Search & Knowledge
    # =====================================================
    "AI Search": [
        "perplexity",
        "ai search",
        "search",
        "notebooklm",
        "knowledge base",
        "knowledge graph",
        "semantic search",
        "retrieval",
        "research assistant"
    ],

    # =====================================================
    # Cloud AI
    # =====================================================
    "Cloud AI": [
        "aws",
        "amazon",
        "bedrock",
        "sagemaker",
        "azure",
        "azure ai",
        "azure openai",
        "microsoft",
        "google cloud",
        "vertex ai",
        "gcp",
        "cloud ai"
    ],

    # =====================================================
    # Hardware
    # =====================================================
    "Hardware": [
        "gpu",
        "cuda",
        "nvidia",
        "blackwell",
        "hopper",
        "gb200",
        "b200",
        "b100",
        "h200",
        "h100",
        "tensor core",
        "chip",
        "processor",
        "ai accelerator",
        "accelerator",
        "amd",
        "intel",
        "qualcomm",
        "apple silicon",
        "tpu",
        "asic"
    ],

    # =====================================================
    # Enterprise AI
    # =====================================================
    "Enterprise AI": [
        "enterprise",
        "business",
        "automation",
        "workflow",
        "crm",
        "erp",
        "copilot",
        "salesforce",
        "oracle",
        "sap",
        "servicenow",
        "digital worker"
    ],

    # =====================================================
    # AI Tools
    # =====================================================
    "AI Tools": [
        "comfyui",
        "n8n",
        "zapier",
        "make.com",
        "ollama",
        "hugging face",
        "transformers",
        "llama.cpp",
        "vllm",
        "docker",
        "kubernetes",
        "mlflow",
        "ray"
    ],

    # =====================================================
    # Generative Media
    # =====================================================
    "Generative Media": [
        "sora",
        "midjourney",
        "stable diffusion",
        "flux",
        "runway",
        "firefly",
        "dalle",
        "elevenlabs",
        "heygen",
        "pika",
        "image generation",
        "video generation",
        "text-to-image",
        "text-to-video",
        "text-to-audio"
    ],

    # =====================================================
    # AI Companies
    # =====================================================
    "Companies": [
        "openai",
        "anthropic",
        "claude",
        "google",
        "deepmind",
        "meta",
        "microsoft",
        "amazon",
        "aws",
        "nvidia",
        "apple",
        "xai",
        "tesla",
        "perplexity",
        "cohere",
        "mistral ai",
        "hugging face",
        "stability ai",
        "together ai",
        "fireworks ai",
        "groq",
        "cerebras",
        "sambanova",
        "writer",
        "adept",
        "glean"
    ],


    # =====================================================
    # Claude / Anthropic
    # =====================================================
    "Claude AI": [
        "claude",
        "claude ai",
        "claude code",
        "claude sonnet",
        "claude opus",
        "claude haiku",
        "claude computer use",
        "anthropic",
        "anthropic ai",
        "anthropic api",
        "anthropic console",
        "anthropic models",
        "model context protocol",
        "mcp",
        "mcp server",
        "computer use",
        "tool use",
        "claude desktop",
        "claude max",
        "claude pro"
    ],

    # =====================================================
    # Context / Loop Engineering
    # =====================================================
    "Loop Engineering": [
        "loop engineering",
        "context engineering",
        "prompt engineering",
        "context window",
        "long context",
        "prompt caching",
        "memory",
        "agent memory",
        "reasoning",
        "planning",
        "tool calling",
        "function calling",
        "structured output",
        "json mode",
        "retrieval",
        "rag",
        "vectorless rag",
        "graph rag",
        "graphrag",
        "knowledge graph",
        "semantic search",
        "embedding",
        "embeddings",
        "context retrieval"
    ],

    # =====================================================
    # Antigravity
    # =====================================================
    "Antigravity": [
        "antigravity",
        "anti gravity",
        "gravity manipulation",
        "gravity control",
        "anti-gravity",
        "warp drive",
        "warp field",
        "alcubierre",
        "alcubierre drive",
        "negative energy",
        "exotic matter",
        "zero point energy",
        "electrogravitics",
        "uap",
        "ufo",
        "advanced propulsion",
        "next generation propulsion",
        "space propulsion",
        "antigravity",
        "anti gravity",
        "gravity manipulation",
        "reactionless drive",
        "reactionless propulsion",
        "warp drive",
        "electrogravitics",
        "propellantless propulsion",
        "advanced propulsion",
        "space propulsion",
        "negative energy",
        "zero point energy",
        "uap",
        "ufo propulsion",
    ],


}


#OUTPUT_FILE = "daily_ai_news.csv"

# -----------------------------
# FETCH RSS
# -----------------------------

# def fetch_rss():
#     articles = []
#     print("Running Fetch RSS...")
#     logging.info(f"[NEWSFEEDER BOT : ] Running Fetch RSS...")  
#     print("=="*50 )
#     for url in RSS_FEEDS:
#         print("=="*50 )
#         print(url+"\n")        
#         print("=="*50 )
#         feed = feedparser.parse(url)            

#         for entry in feed.entries:
#             articles.append({
#             "title": entry.get("title", ""),
#             "link": entry.get("link", ""),
#             "description": entry.get("description", "")  
                  
#             })
#         print("Next URL ")
#         print("=="*50 )
#         print(url+"\n") 
#         print("=="*50 )
#     print("dataFrame : ")
#     print("=="*50 )
#     print(pd.DataFrame(articles))
#     print("=="*50 )
#     return pd.DataFrame(articles)

# def fetch_rss():

#     articles = []

#     for category, feeds in RSS_CATEGORIES.items():

#         print(f"\nCategory : {category}")

#         for url in feeds:

#             print(url)

#             feed = feedparser.parse(url)

#             for entry in feed.entries:

#                 articles.append({

#                     "category": category,
#                     "title": entry.get("title", ""),
#                     "link": entry.get("link", ""),
#                     "description": entry.get("description", "")

#                 })

#     return pd.DataFrame(articles)


def fetch_rss():
    import feedparser, pandas as pd
    articles=[]
    for category,feeds in RSS_CATEGORIES.items():
        for url in feeds:
            feed=feedparser.parse(url)
            for entry in feed.entries:
                articles.append({
                    "category":category,
                    "title":entry.get("title",""),
                    "link":entry.get("link",""),
                    "description":entry.get("description","")
                })
    return pd.DataFrame(articles)



# -----------------------------
# FILTER ARTICLES
# -----------------------------

def filter_articles(df):
    print("Running Filter Articles...")
    logging.info(f"[NEWSFEEDER BOT : ] Running Filter Articles...")  
    print("=="*50 )
    if "combined" not in df.columns:
        df["combined"] = (
            df["title"].fillna("").astype(str) + " " + df["description"].fillna("").astype(str)
        ).str.lower()
    else:
        df["combined"] = df["combined"].fillna("").astype(str)
    print("Before Filtering : ")
    print(df["combined"])
    print("=="*50 )
    filtered = df[df["combined"].apply(
    lambda x: any(keyword in x for keyword in KEYWORDS)
    )]
    print("=="*50 )
    print("After Filtering : ")
    print("=="*50 )
    print(filtered)
    print("=="*50 )
    print("Filter COMPLETED...")
    return filtered


# -----------------------------
# REMOVE DUPLICATES
# -----------------------------

def remove_duplicates(df):
    print("Running Remove Duplicates...")
    logging.info(f"[NEWSFEEDER BOT : ] Running Remove Duplicates...")  
    print("=="*50 )
    if "combined" not in df.columns:
        df["combined"] = (
            df["title"].fillna("").astype(str) + " " + df["description"].fillna("").astype(str)
        ).str.lower()
    if "id" not in df.columns:
        df["id"] = df["link"].fillna("").astype(str).apply(lambda x: hashlib.md5(x.encode()).hexdigest())
    return df.drop_duplicates(subset="id").reset_index(drop=True)

# -----------------------------
# SIMPLE SUMMARIZER (FREE)
# -----------------------------

def summarize_text(text):
    #print("Running Simple Summarizer...")
    return text[:200] # simple truncation (free fallback)

## Classify Article based on keywords in the title and description

# def classify_article(text):

#     text = text.lower()

#     for category, words in CATEGORY_KEYWORDS.items():

#         if any(word.lower() in text for word in words):
#             return category

#     return "General AI"


def classify_article(text):

    if not text:
        return "General AI"

    text = str(text).lower()

    matched_categories = []

    for category, words in CATEGORY_KEYWORDS.items():

        if any(word.lower() in text for word in words):
            matched_categories.append(category)

    if not matched_categories:
        matched_categories.append("General AI")

    category_label = ", ".join(matched_categories)
    logging.info(f"[Classified Articles : ] Article classified into categories: {category_label}")

    return category_label



# -----------------------------
# GENERATE REPORT
# -----------------------------


#   for category,group in df.groupby("category"):
#         body += "\n"+"="*70+"\n"
#         body += "News Category : "+"\n"
#         body += category +"\n"
#         body += "="*70+"\n\n"
#         for _,row in group.iterrows():
#             body += f"• {row['title']}\n"
#             body += f"  {row['link']}\n\n"
    

        
# def generate_email_body(df):
#     body_parts = []

#     for category, group in df.groupby("category", dropna=False):
#         body_parts.append("\n")
#         body_parts.append("#" * 80)
#         body_parts.append(f"#***** NEWS CATEGORY : {str(category).upper()} *****")
#         body_parts.append("#" * 80 + "\n")

#         for _, row in group.iterrows():
#             title = str(row.get("title", "")).strip()
#             link = str(row.get("link", "")).strip()
#             body_parts.append(f"• {title}\n")
#             body_parts.append(f"  {link}\n\n")

#     body = "".join(body_parts)
#     logging.info(f"[EMAIL BODY: ] {body} \n")
#     return body

def generate_email_body(df):
    body_parts = []

    for category, group in df.groupby("categories", dropna=False):
        body_parts.append("\n")
        body_parts.append("#" * 80)
        print(f"Generating Email Body for Category: {category}\n\n")
        logging.info(f"[Generating Email Body : ] Generating Email Body for Category: {category}\n\n")        
        body_parts.append(f"#***** NEWS CATEGORY : {str(category).upper()} *****")
        body_parts.append("#" * 80 + "\n")

        for _, row in group.iterrows():
            title = str(row.get("title", "")).strip()
            link = str(row.get("link", "")).strip()
            body_parts.append(f"• {title}\n")
            body_parts.append(f"  {link}\n\n")

    body = "".join(body_parts)
    logging.info(f"[EMAIL BODY: ] {body} \n")
    return body

#===================================

# import smtplib


# def send_email():
#     server = None
#     try:
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login("email", "password")

#         server.sendmail("from", "to", "message")

#     finally:
#         if server:
#             server.quit()
            
#===================================


            
# def send_email(body):   
#     # Your Gmail credentials
#     sender_email = "aiwthraj@gmail.com"
#     app_password = "eamfbjsxhpfwxmds"

#     # Receiver email
#     receiver_email = "aiwthraj@gmail.com"

#     from datetime import datetime; 
#     today_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     subject = f"Daily AI News Update - {today_date}"
    

#     # Create message
#     message = MIMEMultipart()
#     message["From"] = "aiwthraj@gmail.com"
#     message["To"] = "rajendrabraj@gmail.com"
#     message["cc"] = "aiwthraj@gmail.com"
#     message["Subject"] = subject


#     # Email body
#     #body = "Daily AI News for Today."
#     message_body=body
#     message.attach(MIMEText(message_body, "plain"))
    
     


#     server = None
#     try:
#         server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
#         server.starttls()  # Secure connection
#         server.login(sender_email, app_password)
#         server.send_message(message)

#         print("Email sent successfully!")
#         logging.info(f"[NEWSFEEDER BOT : ] Email sent successfully!")

#     except Exception as e:
#         print("Error:", e)
#         logging.info(f"[NEWSFEEDER BOT : ] Error occurred while sending email: {e}")

#     finally:
#         if server is not None:
#             try:
#                 server.quit()
#             except Exception:
#                 try:
#                     server.close()
#                 except Exception:
#                     pass
        

def generate_report(df):
    print("Running Generate Report...")
    logging.info(f"[NEWSFEEDER BOT : ] Running Generate Report...")  
    print("=="*50 )
    if "combined" not in df.columns:
        df["combined"] = (
            df["title"].fillna("").astype(str) + " " + df["description"].fillna("").astype(str)
        ).str.lower()
    df["summary_short"] = df["description"].fillna("").astype(str).apply(summarize_text)

    # df = df[["title", "link", "summary_short"]]
    
    df = df[["category","title","link","summary_short","combined"]].copy()
    
    #df["category"] = df["combined"].apply(classify_article)
    
    df.loc[:, "categories"] = df["combined"].fillna("").astype(str).apply(classify_article)
    
    
    
    
    
    
    # email_message_body = "\n".join(
    # # df.apply(lambda row: f"Title: {row['title']}, Link: {row['link']}, Summary: {row['summary_short']}", axis=1)
    # #     )
    
    # email_message_body = "\n".join(
    # df.apply(lambda row: f"News   : {row['title']}, URL Link   : {row['link']}", axis=1)
    #     )

    email_message_body = ""

      
    # print("=="*50 )
    # print("Email Body : ")
    # print(email_message_body)
    # print("=="*50 )
    
    
    ## Generate Email Body
    
    email_message_body = generate_email_body(df)    
    
    logging.info(f"[Generate REPORT  BODY: ] {email_message_body} \n")
    
    


    from pathlib import Path
    # Output paths
    csv_file = OUTPUT_CSV_FILE
    html_file = OUTPUT_HTML_FILE
    
    print(f"Output CSV Path: {csv_file} \n \n ")
    logging.info(f"[Generate REPORT : NEWSFEEDER BOT : ] Output CSV Path: {csv_file}")
    print(f"Output HTML Path: {html_file} \n \n ")
    logging.info(f"[Generate REPORT : NEWSFEEDER BOT : ] Output HTML Path: {html_file}")
    

    # # Remove existing files if they exist
    # csv_file.unlink(missing_ok=True)
    # html_file.unlink(missing_ok=True)

    
    # Save to CSV
    # df.to_csv(OUTPUT_FILE, index=False)    
    # html = df.to_html()    
    # df.to_html("News.html")    
    
    # Save to CSV
    
    # df.to_csv(csv_file, index=False, mode="w")
    # df.to_html(html_file, index=False)
    

    print(f"Report generated: {csv_file}")
    logging.info(f"[Generate REPORT : NEWSFEEDER BOT : ] Report generated: {csv_file}")
    print(f"Report generated: {html_file}")
    logging.info(f"[Generate REPORT : NEWSFEEDER BOT : ] Report generated: {html_file}")

    ##Send Email by calling the function    
    send_email(email_message_body)
    print(f"Email generated:")
    logging.info(f"[NEWSFEEDER BOT : ] Email generated:")
    
 


# -----------------------------
# MAIN PIPELINE
# -----------------------------

def run_pipeline():
    print("Running AI News Feeder STARTED...")
    logging.info(f"[NEWSFEEDER BOT : ] Running AI News Feeder...")  
    print("=="*50 )
    
    df = fetch_rss()
    df = filter_articles(df)
    print("Before Generating Report..")
    print("=="*50 )
    print(df)
    print("=="*50 )
    print("START Removing Duplicates...")
    logging.info(f"[NEWSFEEDER BOT : ] START Removing Duplicates...")
    df = remove_duplicates(df)
    print("COMPLETED Removing Duplicates...")
    print("=="*50 )
    print("START Generating Report...")
    generate_report(df)
    print("COMPLETED    Generating Report...")    
    print("Running AI News Feeder COMPLETED...")
    logging.info(f"[NEWSFEEDER BOT : ] AI News Feeder COMPLETED...")  
    print("=="*50 )


def main():
    print("Running AI News Feeder Main Function...")
    print("AI News Feeder Main STARTED Function...")
    logging.info(f"[NEWSFEEDER BOT : ] AI News Feeder Main STARTED Function...")  
    print("=="*50 )
    run_pipeline()
    logging.info(f"[NEWSFEEDER BOT : ] AI News Feeder Main COMPLETED Function...")  
    print("AI News Feeder Main COMPLETED Function...")
    print("=="*50 )

# -----------------------------
# EXECUTE
# -----------------------------

if __name__ == "__main__":
    main()



# -----------------------------
# OPTIONAL LLM SUMMARIZATION
# -----------------------------
"""
from openai import OpenAI
client = OpenAI(api_key="YOUR_API_KEY")

def summarize_text(text):
	response = client.chat.completions.create(
	model="gpt-4o-mini",
	messages=[
	{"role": "system", "content": "Summarize AI news in 2 lines"},
	{"role": "user", "content": text}
	]

)
return response.choices[0].message.content

"""