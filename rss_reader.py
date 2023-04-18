import feedparser
import time
from flask import Flask

app = Flask(__name__)

# RSS feed URLs
rss_feed_urls = ['https://upstract.com/feed', 'https://techcrunch.com/feed/']

# List of keywords to search for in the feed
keywords = ['GPT', 'ChatGPT', 'OpenAI', 'Anthropic']

# Set to keep track of already notified articles
notified_articles = set()

# Variable to keep track of unread counter
unread_counter = 0

# Function to send notification for a matched article
def send_notification(article_title):
    # Replace this with your own notification logic
    print(f'Notification: Keyword found in article: {article_title}')

# Function to log articles to a file
def log_article(article_title):
    with open('article_log.txt', 'a') as log_file:
        log_file.write(article_title + '\n')

@app.route('/')
def home():
    return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>RSS Notifier ({unread_counter})</title>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>
                function addNotification(notification) {{
                    $("#notifications").prepend("<li>" + notification + "</li>");
                }}
            </script>
        </head>
        <body>
            <h1>Notifications</h1>
            <ul id="notifications"></ul>
        </body>
        </html>
    '''

def check_rss():
    global unread_counter
    while True:
        # Fetch the RSS feeds
        for rss_feed_url in rss_feed_urls:
            # Fetch the RSS feed
            feed = feedparser.parse(rss_feed_url)

            # Loop through the feed entries
            for entry in feed.entries:
                # Check if the entry title contains any of the keywords
                if any(keyword in entry.title.lower() for keyword in keywords):
                    # Check if the article has already been notified
                    if entry.title not in notified_articles:
                        # Send notification
                        send_notification(entry.title)
                        # Log the article
                        log_article(entry.title)
                        # Add the article to the notified articles set
                        notified_articles.add(entry.title)
                        # Increment the unread counter
                        unread_counter += 1
                        # Add notification to the web page
                        app.send_static_file('index.html', code=f'<script>addNotification("{entry.title}")</script>')

        # Update the title of the web page with the current unread counter
        app.send_static_file('index.html', code=f'<script>document.title = "RSS Notifier ({unread_counter})";</script>')
        # Sleep for 15 seconds
        time.sleep(15)

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
