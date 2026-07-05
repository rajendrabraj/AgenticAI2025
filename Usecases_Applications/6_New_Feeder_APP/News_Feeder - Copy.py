## This program processed the RSS news feeds reads them and sends daily email
## Rajendra Bichu  (Date : 5th April 2026)


import feedparser
import feedparser
from matplotlib import text
from oxmsg import message
import pandas as pd
from datetime import datetime
import hashlib
import html

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
    

# def fetch_rss():

#     feeds = [

#     “https://techcrunch.com/tag/artificial-intelligence/feed/”,
#     “https://www.technologyreview.com/topic/artificial-intelligence/feed/”,
#     "https://www.artificialintelligence-news.com/feed/",
#     "https://techcrunch.com/category/artificial-intelligence/feed/",
#     "https://www.wired.com/feed/tag/artificial-intelligence/latest/rss",
#     "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
#     "https://feeds.arstechnica.com/arstechnica/artificial-intelligence",
#     "https://aimagazine.com/rss",
#     "https://www.marktechpost.com/feed/",
#     "https://www.kdnuggets.com/feed",
#     "https://towardsdatascience.com/feed",
#     "https://towardsai.net/feed",
#     "https://www.analyticsvidhya.com/blog/feed/",
#     "https://machinelearningmastery.com/feed/",
#     "https://huggingface.co/blog/feed.xml",
#     "https://openai.com/blog/rss.xml",
#     "https://www.anthropic.com/news/rss.xml",
#     "https://deepmind.google/discover/blog/rss.xml",
#     "https://ai.googleblog.com/feeds/posts/default",
#     "https://bair.berkeley.edu/blog/feed.xml",
#     "https://news.mit.edu/rss/topic/artificial-intelligence2",
#     "https://www.lesswrong.com/feed.xml",
#     "https://gwern.net/rss.xml",
#     "https://www.reddit.com/r/MachineLearning/.rss",
#     "https://www.reddit.com/r/LocalLLaMA/.rss",
#     "https://www.reddit.com/r/singularity/.rss"
#     ]

#Parse the RSS feeds and print the titles of the articles

# articles = []

# for feed in feeds:
# parsed = feedparser.parse(feed)
# for entry in parsed.entries:
# articles.append(entry.title + " - " + entry.summary)

# return articles


# RSS_FEEDS = [
#     "https://www.aidataanalytics.network/rss/articles",
#     "https://techcrunch.com/category/artificial-intelligence/feed/",
#     "https://www.marktechpost.com/feed/",
#     "https://machinelearningmastery.com/blog/feed/",
#     "https://marktechpost.com/feed/",
#     "https://bair.berkeley.edu/blog/feed.xml",
#     "https://kdnuggets.com/feed",
#     "https://pub.towardsai.net/feed",    
#     "https://www.wired.com/feed/tag/ai/latest/rss",
#     "https://techcrunch.com/tag/artificial-intelligence/feed/"    
#     "https://huggingface.co/blog/feed.xml",
#     "https://openai.com/blog/rss.xml",
#     "https://www.anthropic.com/news/rss.xml",
#     "https://www.reddit.com/r/MachineLearning/.rss",    
#     "https://www.artificialintelligence-news.com/feed/",
#     "https://techcrunch.com/category/artificial-intelligence/feed/",
#     "https://www.wired.com/feed/tag/artificial-intelligence/latest/rss",
#     "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
#     "https://feeds.arstechnica.com/arstechnica/artificial-intelligence",
#     "https://aimagazine.com/rss",
#     "https://www.marktechpost.com/feed/",
#     "https://www.kdnuggets.com/feed",
#     "https://towardsdatascience.com/feed",
#     "https://towardsai.net/feed",
#     "https://www.analyticsvidhya.com/blog/feed/",
#     "https://machinelearningmastery.com/feed/",
#     "https://huggingface.co/blog/feed.xml",
#     "https://openai.com/blog/rss.xml",
#     "https://www.anthropic.com/news/rss.xml",
#     "https://deepmind.google/discover/blog/rss.xml",
#     "https://ai.googleblog.com/feeds/posts/default",
#     "https://bair.berkeley.edu/blog/feed.xml",
#     "https://news.mit.edu/rss/topic/artificial-intelligence2",
#     "https://www.lesswrong.com/feed.xml",
#     "https://gwern.net/rss.xml",
#     "https://www.reddit.com/r/MachineLearning/.rss",
#     "https://www.reddit.com/r/LocalLLaMA/.rss",
#     "https://www.reddit.com/r/singularity/.rss",
#     "https://techcrunch.com/category/artificial-intelligence/feed/",
#     "https://www.marktechpost.com/feed/",
#     "https://huggingface.co/blog/feed.xml",
#     "https://openai.com/blog/rss.xml",    
#     "https://www.reddit.com/r/MachineLearning/.rss",
#     "https://www.marktechpost.com/feed/",
#     "https://huggingface.co/blog/feed.xml",
#     "https://openai.com/blog/rss.xml",
#     "https://www.anthropic.com/news/rss",
#     "https://azure.microsoft.com/en-us/blog/feed/",
#     "https://aws.amazon.com/blogs/machine-learning/feed/",
#     "https://developer.nvidia.com/blog/feed/",
#     "https://bair.berkeley.edu/blog/feed.xml",
#     "https://ai.googleblog.com/feeds/posts/default",
#     "https://deepmind.google/blog/rss.xml",
#     "https://machinelearning.apple.com/rss.xml",
#     "https://machinelearningmastery.com/feed/",
#     "https://towardsdatascience.com/feed",
#     "https://pub.towardsai.net/feed",
#     "https://neptune.ai/blog/rss.xml",
#     "https://huggingface.co/blog/feed.xml",
#     "https://venturebeat.com/category/ai/feed/",
#     "https://the-decoder.com/feed/",
#     "https://theaiinsider.tech/feed/",
#     "https://www.analyticsvidhya.com/blog/feed/",
#     "https://www.marktechpost.com/feed/",
#     "http://arxiv.org/rss/cs.LG",
#     "https://news.mit.edu/rss/topic/artificial-intelligence",
#     "https://www.csail.mit.edu/rss.xml",
#     "https://cloud.google.com/blog/topics/ai-ml/rss/",
#     "https://blogs.nvidia.com/feed/",
#     "https://aws.amazon.com/blogs/aws/feed/",
#     "https://techcommunity.microsoft.com/t5/azure-ai/bg-p/AzureAI/rss",
#     "https://planet-ai.net/rss.xml",
#     "https://openai.com/blog/rss.xml",
#     "https://www.anthropic.com/news/rss",
#     "https://azure.microsoft.com/en-us/blog/feed/",
#     "https://aws.amazon.com/blogs/machine-learning/feed/",
#     "https://developer.nvidia.com/blog/feed/",
#     "https://blogs.nvidia.com/feed/",
#     "https://www.uber.com/blog/engineering/feed/",
#     "https://www.uber.com/blog/ai/feed/",
#     "https://bair.berkeley.edu/blog/feed.xml",
#     "https://ai.googleblog.com/feeds/posts/default",
#     "https://deepmind.google/blog/rss.xml",
#     "https://machinelearning.apple.com/rss.xml",
#     "https://machinelearningmastery.com/feed/",
#     "https://towardsdatascience.com/feed",
#     "https://pub.towardsai.net/feed",
#     "https://neptune.ai/blog/rss.xml",
#     "https://huggingface.co/blog/feed.xml",
#     "https://venturebeat.com/category/ai/feed/",
#     "https://the-decoder.com/feed/",
#     "https://theaiinsider.tech/feed/",
#     "https://www.analyticsvidhya.com/blog/feed/",
#     "https://www.marktechpost.com/feed/",
#     "http://arxiv.org/rss/cs.LG",
#     "https://news.mit.edu/rss/topic/artificial-intelligence",
#     "https://www.csail.mit.edu/rss.xml",
#     "https://cloud.google.com/blog/topics/ai-ml/rss/",
#     "https://aws.amazon.com/blogs/aws/feed/",
#     "https://techcommunity.microsoft.com/t5/azure-ai/bg-p/AzureAI/rss",
#     "https://planet-ai.net/rss.xml",
#     "https://developer.nvidia.com/blog/feed/",
#     "https://blogs.nvidia.com/feed/"

#     ]

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


]

OUTPUT_FILE = "daily_ai_news.csv"

# -----------------------------
# FETCH RSS
# -----------------------------

def fetch_rss():
    articles = []
    print("Running Fetch RSS...")
    print("=="*50 )
    for url in RSS_FEEDS:
        print("=="*50 )
        print(url+"\n")        
        print("=="*50 )
        feed = feedparser.parse(url)            

        for entry in feed.entries:
            articles.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "description": entry.get("description", "")  
                  
            })
        print("Next URL ")
        print("=="*50 )
        print(url+"\n") 
        print("=="*50 )
    print("dataFrame : ")
    print("=="*50 )
    print(pd.DataFrame(articles))
    print("=="*50 )
    return pd.DataFrame(articles)



# -----------------------------
# FILTER ARTICLES
# -----------------------------

def filter_articles(df):
    print("Running Filter Articles...")
    print("=="*50 )
    df["combined"] = (df["title"] + " " + df["description"]).str.lower()
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
    print("=="*50 )
    df["id"] = df["link"].apply(lambda x: hashlib.md5(x.encode()).hexdigest())
    return df.drop_duplicates(subset="id")

# -----------------------------
# SIMPLE SUMMARIZER (FREE)
# -----------------------------

def summarize_text(text):
    print("Running Simple Summarizer...")
    return text[:200] # simple truncation (free fallback)




# -----------------------------
# GENERATE REPORT
# -----------------------------

def send_email(body):   
    # Your Gmail credentials
    sender_email = "aiwthraj@gmail.com"
    app_password = "eamfbjsxhpfwxmds"

    # Receiver email
    receiver_email = "aiwthraj@gmail.com"

    from datetime import datetime; 
    today_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    subject = f"Daily AI News Update - {today_date}"
    

    # Create message
    message = MIMEMultipart()
    message["From"] = "aiwthraj@gmail.com"
    message["To"] = "rajendrabraj@gmail.com"
    message["cc"] = "aiwthraj@gmail.com"
    message["Subject"] = subject


    # Email body
    #body = "Daily AI News for Today."
    message_body=body
    message.attach(MIMEText(message_body, "plain"))

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure connection
        server.login(sender_email, app_password)

        # Send email
        server.send_message(message)
        print("Email sent successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        server.quit()
        

def generate_report(df):
    print("Running Generate Report...")
    print("=="*50 )
    df["summary_short"] = df["description"].apply(summarize_text)

    df = df[["title", "link", "summary_short"]]
    
    # email_message_body = "\n".join(
    # # df.apply(lambda row: f"Title: {row['title']}, Link: {row['link']}, Summary: {row['summary_short']}", axis=1)
    # #     )
    
    email_message_body = "\n".join(
    df.apply(lambda row: f"News   : {row['title']}, URL Link   : {row['link']}", axis=1)
        )

    
    # print("=="*50 )
    # print("Email Body : ")
    # print(email_message_body)
    # print("=="*50 )
    
    ##Send Email
    send_email(email_message_body)
    
    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False)
    
    html = df.to_html()
    
    df.to_html("News.html")
    

    print(f"Report generated: {OUTPUT_FILE}")


# -----------------------------
# MAIN PIPELINE
# -----------------------------

def run_pipeline():
    print("Running AI News Feeder STARTED...")
    print("=="*50 )
    
    df = fetch_rss()
    df = filter_articles(df)
    print("Before Generating Report..")
    print("=="*50 )
    print(df)
    print("=="*50 )
    #df = remove_duplicates(df)
    generate_report(df)
    print("Running AI News Feeder COMPLETED...")
    print("=="*50 )
# -----------------------------
# EXECUTE
# -----------------------------

if __name__ == "__main__":
    print("Running AI News Feeder Main Function...")
    print("=="*50 )
    run_pipeline()
    print("=="*50 )



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