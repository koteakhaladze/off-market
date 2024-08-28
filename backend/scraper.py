
import json
import time
from playwright.async_api import async_playwright
import psycopg2
from psycopg2.extras import execute_values

def get_connection():
    db = {
        "host": "127.0.0.1",
        "database": "doc-hub",
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


class FacebookScraper:
    def __init__(self, url):
        self.posts = []
        self.base_url = url
        self.completed = False

    def save(self):
        try:
            cursor, connection = get_db_connection()
            values_list = [
                (post["user_name"], post["user_url"], post["text"], post["timestamp"], json.dumps(post["image_urls"]) if post["image_urls"] else None ,self.base_url) 
                for post in self.posts
            ]
            print(f"inserting {len(values_list)}")
            execute_values(
                cursor,
                "INSERT INTO posts (user_name, user_url, text, timestamp, image_urls, url) VALUES %s",
                values_list,
                "(%s, %s, %s, %s, %s, %s)",
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
            i += 200
            yield page

    async def execute(self):
        async with async_playwright() as playwright:
            async def postprocess_response(response) -> None:
                if "api/graphql" in response.url:
                    print("Response URL: ", response.url)
                    try:
                        response_text = await response.text()
                        response_text = response_text.replace('}}}}}', "}}}}},")
                        json_data = json.loads("[" + response_text[0:-1] + "]")
                        date = None
                        image_urls = []
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
                                            text = story["comet_sections"].get("message", {}).get("story", {}).get("message", {}).get("text", "")
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
                                            print(f"found post {user_name} {len(image_urls)} {text}")
                                            self.posts.append({
                                                "user_name": user_name,
                                                "user_url": url,
                                                "text": text,
                                                "timestamp": date,
                                                "image_urls": image_urls
                                            })
                                            if len(self.posts) == 100:
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
            while True:
                await base_page.goto(self.base_url)
                try:
                    await base_page.wait_for_selector("[aria-label=\"Close\"]")
                    loc = base_page.locator("[aria-label=\"Close\"]")
                    await loc.dispatch_event("click")
                    break
                except Exception as e:
                    print(e)
                    continue
            # 1 week ago
            self.time = int(time.time() - 60 * 60 * 24 * 7)
            async for page in self.scroll_to_bottom(base_page):
                if self.completed:
                    break
                page.on("response", postprocess_response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(FacebookScraper().execute())