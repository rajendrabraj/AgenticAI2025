# AI News Feeder with Categories
# NOTE:
# Your original script is very large because of the KEYWORDS list.
# To avoid changing your send_email() function, only these structural changes are needed:
#
# 1. Replace RSS_FEEDS with RSS_CATEGORIES (dict).
# 2. Update fetch_rss() to include a "category" field.
# 3. Keep filter_articles(), remove_duplicates(), summarize_text(), send_email() unchanged.
# 4. Update generate_report() to group by category.
# 5. Include category column in CSV.
#
# Paste your existing KEYWORDS list and send_email() function unchanged from your current file.
#
RSS_CATEGORIES = {
    "AI Research":[
        "https://huggingface.co/blog/feed.xml",
        "https://machinelearningmastery.com/feed/",
        "https://towardsdatascience.com/feed",
        "https://bair.berkeley.edu/blog/feed.xml",
        "http://arxiv.org/rss/cs.LG"
    ],
    "AI Companies":[
        "https://openai.com/blog/rss.xml",
        "https://www.anthropic.com/news/rss",
        "https://deepmind.google/blog/rss.xml",
        "https://blogs.nvidia.com/feed/",
        "https://developer.nvidia.com/blog/feed/"
    ],
    "Cloud AI":[
        "https://cloud.google.com/blog/topics/ai-ml/rss/",
        "https://aws.amazon.com/blogs/machine-learning/feed/",
        "https://techcommunity.microsoft.com/t5/azure-ai/bg-p/AzureAI/rss",
        "https://azure.microsoft.com/en-us/blog/feed/"
    ],
    "AI News":[
        "https://venturebeat.com/category/ai/feed/",
        "https://the-decoder.com/feed/",
        "https://www.marktechpost.com/feed/",
        "https://theaiinsider.tech/feed/"
    ]
}

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

def generate_email_body(df):
    body=""
    for category,group in df.groupby("category"):
        body += "\n"+"="*70+"\n"
        body += category+"\n"
        body += "="*70+"\n\n"
        for _,row in group.iterrows():
            body += f"• {row['title']}\n"
            body += f"  {row['link']}\n\n"
    return body
