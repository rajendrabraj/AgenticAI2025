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
import logging
import os

## Start Logging Information to log    
script_path = os.path.abspath(__file__)
# Get the directory name from the script path
script_dir = os.path.dirname(script_path)
# Get the parent directory using os.pardir ('..')
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
print(f"Parent directory path: {parent_directory}")


#data_directory_path = os.path.join(parent_directory, "data")
#print(f"Data directory path: {data_directory_path}")



logging.basicConfig(
    filename=os.path.join(parent_directory, "StockNewsTask.log"),
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)


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



RSS_FEEDS = [
"https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
"https://www.moneycontrol.com/rss/MCtopnews.xml",
"https://www.moneycontrol.com/rss/marketreports.xml",
"https://www.business-standard.com/rss/markets-106.rss",
"https://www.livemint.com/rss/markets",
"https://www.financialexpress.com/market/feed/",
"https://www.thehindubusinessline.com/markets/?service=rss",
"https://www.cnbctv18.com/market/rss.xml",
"https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
"https://www.moneycontrol.com/rss/marketreports.xml",
"https://www.livemint.com/rss/markets",
"https://www.cnbctv18.com/market/rss.xml",
]


# RSS_FEEDS = [
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

##Keywords to filter relevant AI news articles



KEYWORDS = [
"stocks","ticket","company","market","share","investment","trading","finance","economy","business","earnings","revenue","growth","decline","volatility","index","portfolio","dividend",
"stock market","stocks","equities","share market","trading","investing","stock exchange","NSE","BSE","Sensex","Nifty 50",
"Nifty Bank","Indian stock market","IPO","initial public offering","bull market","bear market","market trends","stock analysis",
"technical analysis","fundamental analysis","market news","earnings","quarterly results","dividends","portfolio","asset allocation",
"large cap","mid cap","small cap","blue chip stocks","multibagger","stock tips","intraday trading","swing trading",
"long term investing","volatility","market crash","market rally","stock performance","sector stocks","banking stocks",
"IT stocks","pharma stocks","FMCG stocks","auto stocks","metal stocks","energy stocks","PSU stocks","retail investors",
"FIIs","DIIs","mutual funds","index funds","ETF","capital gains","stock valuation","PE ratio","PB ratio","market capitalization"

]


OUTPUT_FILE = "stocknews.csv"

# -----------------------------
# FETCH RSS
# -----------------------------

def fetch_rss():
    articles = []
    print("Running Fetch RSS...")
    logging.info(f"[NEWSFEEDER BOT : ] Running Fetch RSS...")  
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
    logging.info(f"[NEWSFEEDER BOT : ] Running Filter Articles...")  
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
    logging.info(f"[NEWSFEEDER BOT : ] Running Remove Duplicates...")  
    print("=="*50 )
    df["id"] = df["link"].apply(lambda x: hashlib.md5(x.encode()).hexdigest())
    return df.drop_duplicates(subset="id")

# -----------------------------
# SIMPLE SUMMARIZER (FREE)
# -----------------------------

def summarize_text(text):
    #print("Running Simple Summarizer...")
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
    subject = f"Stocks News Update - {today_date}"
    

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
        logging.info(f"[NEWSFEEDER BOT : ] Email sent successfully!")  

    except Exception as e:
        print("Error:", e)
        logging.info(f"[NEWSFEEDER BOT : ] Error occurred while sending email: {e}")  

    finally:
        server.quit()
        

def generate_report(df):
    print("Running Generate Report...")
    logging.info(f"[NEWSFEEDER BOT : ] Running Generate Report...")  
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
    
    df.to_html("Stock_News.html")
    

    print(f"Report generated: {OUTPUT_FILE}")


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
# -----------------------------
# EXECUTE
# -----------------------------

if __name__ == "__main__":
    print("Running AI News Feeder Main Function...")
    logging.info(f"[NEWSFEEDER BOT : ] AI News Feeder Main Function...")  
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