import asyncio
import csv
import json
import threading
import sys

import psycopg2
sys.path.append('..')
from backend.scraper import FacebookScraper
import schedule

import csv
import os

# Get the absolute path to the CSV file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
csv_path = os.path.join(parent_dir, 'files', 'groups.csv')

urls = []
# Read and print the CSV data
with open(csv_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        urls.append(
            row['Group Link']
        )


def run_scraper():
    for url in urls:
        scraper = FacebookScraper(url)
        asyncio.run(scraper.execute())

schedule.every(15).seconds.do(run_scraper)

# Function to run the scheduler
def run_scheduler():
    while True:
        schedule.run_pending()

# Start the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()


# def get_connection():
#     db = {
#         "host": "127.0.0.1",
#         "database": "real_estate_db",
#         "user": "",
#         "password": "",
#         "port": "5432",
#     }

#     return psycopg2.connect(
#         database=db["database"],
#         user=db["user"],
#         password=db["password"],
#         host=db["host"],
#         port=db["port"],
#     )

# def get_db_connection():
#     connection = get_connection()
#     return connection.cursor(), connection

# if __name__ == '__main__':
#     cursor, connection = get_db_connection()
#     cursor.execute("SELECT * FROM posts;")
#     data = cursor.fetchall()
#     print(data)
#     column_names = [desc[0] for desc in cursor.description]
#     with open("posts.csv", 'w', newline='', encoding='utf-8') as csvfile:
#         csvwriter = csv.writer(csvfile)
        
#         # Write header
#         csvwriter.writerow(column_names)
        
#         # Write data rows
#         for row in data:
#             # Convert image_urls JSON to string if it's not None
#             row = list(row)
#             if row[5] is not None:  # Assuming image_urls is the 6th column (index 5)
#                 row[5] = json.dumps(row[5])
#             if row[7] is not None:
#                 row[7] = json.dumps(row[7])
#             # Convert text_hash from bytes to hex string
#             row[8] = row[8].hex()  # Assuming text_hash is the 8th column (index 7)
            
#             csvwriter.writerow(row)