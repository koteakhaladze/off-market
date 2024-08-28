import asyncio
import threading
import sys
sys.path.append('..')
from backend.scraper import FacebookScraper
import schedule


urls = [
    "https://www.facebook.com/groups/1972974669636613/?sorting_setting=CHRONOLOGICAL",
]

def run_scraper():
    for url in urls:
        scraper = FacebookScraper(url)
        asyncio.run(scraper.execute())

schedule.every(15).minutes.do(run_scraper)

# Function to run the scheduler
def run_scheduler():
    while True:
        schedule.run_pending()

# Start the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()