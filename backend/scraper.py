
import json
import time
from playwright.async_api import async_playwright
import psycopg2
from psycopg2.extras import execute_values
import requests
from playwright.async_api import TimeoutError

def get_connection():
    db = {
        "host": "127.0.0.1",
        "database": "real_estate_db",
        "user": "",
        "password": "",
        "port": "5432",
    }

    return psycopg2.connect(
        database=db["database"],
        user=db["user"],
        password=db["password"],
        host=db["host"],
        port=db["port"],
    )

def get_db_connection():
    connection = get_connection()
    return connection.cursor(), connection

import hashlib

def generate_text_hash(text):
    # Encode the text to bytes using UTF-8 encoding
    text_bytes = text.encode('utf-8')
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256(text_bytes)
    # Get the hexadecimal representation of the hash
    return hash_object.hexdigest()

class FacebookScraper:
    def __init__(self, url):
        self.posts = []
        self.base_url = url
        self.completed = False
        self.last_found_post = 0
        print("starting scraping")

    def save(self):
        try:
            cursor, connection = get_db_connection()
            values_list = [
                (post["user_name"], post["user_url"], post["text"], post["timestamp"], json.dumps(post["image_urls"]) if post["image_urls"] else None , post.get("comments", None), self.base_url, generate_text_hash(post["text"])) 
                for post in self.posts
            ]
            print(f"inserting {len(values_list)}")
            execute_values(
                cursor,
                "INSERT INTO posts (user_name, user_url, text, timestamp, image_urls, comments, base_url, text_hash) VALUES %s ON CONFLICT (text_hash, base_url) DO NOTHING;",
                values_list,
                "(%s, %s, %s, %s, %s, %s, %s, %s)",
            )
            connection.commit()
            cursor.close()
        except Exception as e:
            print(e)

    async def scroll_to_bottom(self, page):
        scroll_y, scroll_height = await page.evaluate("""
            () => [
                window.scrollY,
                window.document.documentElement.scrollHeight
            ]
        """)

        i = 0
        while scroll_y * i < scroll_height:
            await page.evaluate(f"""
                (i) => {{
                    window.scrollTo({{
                        top: i,
                        left: 0,
                        behavior: 'smooth'
                    }})
                }}
            """, i)
            i += 10
            yield page


    async def execute(self):
        async with async_playwright() as playwright:
            async def postprocess_response(response) -> None:
                if "api/graphql" in response.url:
                    try:
                        response_text = await response.text()
                        response_text = response_text.replace('}}}}}', "}}}}},")
                        json_data = json.loads("[" + response_text[0:-1] + "]")
                        date = None
                        image_urls = []
                        all_comments = []
                        for item in json_data:
                            for k,v in item.items():
                                if k == "data":
                                    if "node" in v:
                                        node = v["node"]
                                        if node.get("__typename", "") == "Story":
                                            comet_sections = node["comet_sections"]
                                            context_layout = comet_sections.get("context_layout", "")
                                            if context_layout:
                                                metadata = context_layout["story"]["comet_sections"]["metadata"]
                                                for metadata_item in metadata:
                                                    metadata_story = metadata_item["story"]
                                                    if "creation_time" in metadata_story:
                                                        date = metadata_story["creation_time"]
                                            story = comet_sections["content"]["story"]
                                            try:
                                                comments = comet_sections.get("feedback", {}).get("story", {}).get("story_ufi_container", {}).get("story", {}).get("feedback_context", {}).get("interesting_top_level_comments", [])
                                                if comments:
                                                    for comment in comments:
                                                        comment_text = comment.get("comment", {}).get("body", {}).get("text", "")
                                                        if comment_text:
                                                            comment_user = comment["comment"]["author"]["name"]
                                                            url = comment["comment"]["author"]["url"]
                                                            all_comments.append({
                                                                "user_name": comment_user,
                                                                "user_url": url,
                                                                "text": comment_text,
                                                            })
                                            except Exception as e:
                                                print(e)
                                            if not story:
                                                continue
                                            text = story.get("comet_sections", {}).get("message", {}).get("story", {}).get("message", {}).get("text", "")
                                            if not text:
                                                continue
                                            attachments = story.get("attachments")
                                            if attachments:
                                                for attach in attachments:
                                                    image_url = attach.get("styles", {}).get("attachment", {}).get("media", {}).get("photo_image", {}).get("uri", "")
                                                    image_urls.append(image_url)
                                            actor = story["actors"][0]
                                            user_name = actor["name"]
                                            url = actor["url"]
                                            if date and date < self.time:
                                                self.completed = True
                                            print(f"found post {user_name} with {text[:20]} {[comment['user_name'] for comment in all_comments]}")
                                            if text:
                                                self.last_found_post = int(time.time())
                                                self.posts.append({
                                                    "user_name": user_name,
                                                    "user_url": url,
                                                    "text": text,
                                                    "timestamp": date,
                                                    "image_urls": image_urls,
                                                    "comments": json.dumps(all_comments)
                                                })
                                            all_comments = []
                                            if len(self.posts) == 10:
                                                print("Saving")
                                                self.save()
                                                self.posts = []
                    except Exception as e:
                        print(e)
            browser = await playwright.chromium.launch(**{
                "channel": "chrome",
                "headless": True,
                "slow_mo": 60,
                "devtools": True,
                "proxy": {
                    "server": "http://proxy.scrape.do:8080",
                    "username": "4f8f0440cff74bf0848bf6a70e0807826e9b1dc3d1f",
                    "password": "",
                },
                "args": ['--ignore-certificate-errors', '--disable-web-security']
            })
            base_page = await browser.new_page()
            await browser.new_context(
                extra_http_headers={
                    "Accept-Language": "en-US,en;q=0.9",
                    "Connection": "keep-alive",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",  # noqa
                }
            )
            tries = 0
            exited = False
            while True:
                try:
                    if tries > 10:
                        exited = True
                        break
                    await base_page.goto(self.base_url)
                    await base_page.wait_for_selector("[aria-label=\"Close\"]")
                    loc = base_page.locator("[aria-label=\"Close\"]")
                    await loc.dispatch_event("click")
                    try:
                        await base_page.wait_for_selector(".x9f619.x1n2onr6.x1ja2u2z.x78zum5.x2lah0s.x1nhvcw1.x6s0dn4.xozqiw3.x1q0g3np.xexx8yu.xwrv7xz.x8182xy.xmgb6t1.x1kgmq87", timeout=30000)
                        loc = base_page.locator(".x9f619.x1n2onr6.x1ja2u2z.x78zum5.x2lah0s.x1nhvcw1.x6s0dn4.xozqiw3.x1q0g3np.xexx8yu.xwrv7xz.x8182xy.xmgb6t1.x1kgmq87")
                        text = await loc.inner_text()
                        if "private" in text.lower():
                            print("private")
                            exited = True
                    except TimeoutError as e:
                        print("exited")
                        exited = False
                    break
                except Exception as e:
                    print(e)
                    tries += 1
                    continue
            # 1 week ago
            if exited:
                return
            self.time = int(time.time() - 60 * 60 * 24 * 7)
            self.last_found_post =int(time.time())
            async for page in self.scroll_to_bottom(base_page):
                if int(time.time()) - self.last_found_post > 180:
                    self.completed = True
                    break
                if self.completed:
                    self.save()
                    break
                page.on("response", postprocess_response)

