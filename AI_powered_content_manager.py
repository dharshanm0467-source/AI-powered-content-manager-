import os
import json
from datetime import datetime
from pathlib import Path

# pip install openai
try:
    from openai import OpenAI
except ImportError:
    print("Run: pip install openai")
    exit()

class ContentManager:
    def __init__(self, api_key, storage_file="content_db.json"):
        self.client = OpenAI(api_key=api_key)
        self.storage_file = Path(storage_file)
        self.db = self.load_db()

    def load_db(self):
        if self.storage_file.exists():
            with open(self.storage_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"posts": []}

    def save_db(self):
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.db, f, indent=2, ensure_ascii=False)

    def generate_ideas(self, topic, count=5):
        prompt = f"Give me {count} viral content ideas for '{topic}'. Include hook + 1 line description. Format as JSON list."

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )

        ideas = response.choices[0].message.content
        return ideas

    def generate_post(self, topic, platform="Instagram", tone="casual"):
        prompt = f"Write a {platform} post about '{topic}' in {tone} tone. Max 150 words. Add 5 relevant hashtags."

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content
        post = {
            "id": len(self.db["posts"]) + 1,
            "topic": topic,
            "platform": platform,
            "tone": tone,
            "content": content,
            "created_at": datetime.now().isoformat()
        }
        self.db["posts"].append(post)
        self.save_db()
        return post

    def search_posts(self, keyword):
        results = [p for p in self.db["posts"] if keyword.lower() in p["content"].lower() or keyword.lower() in p["topic"].lower()]
        return results

    def list_posts(self):
        return self.db["posts"]

def main():
    print("="*50)
    print(" AI POWERED CONTENT MANAGER")
    print("="*50)

    api_key = input("Enter your OpenAI API key: ").strip()
    cm = ContentManager(api_key)

    while True:
        print("\n1. Generate Ideas")
        print("2. Generate Post")
        print("3. Search Posts")
        print("4. List All Posts")
        print("5. Exit")

        choice = input("\nChoose option: ")

        if choice == "1":
            topic = input("Enter topic/niche: ")
            count = int(input("How many ideas? ") or 5)
            ideas = cm.generate_ideas(topic, count)
            print("\n--- AI Ideas ---\n", ideas)

        elif choice == "2":
            topic = input("Enter topic: ")
            platform = input("Platform [Instagram/Twitter/LinkedIn]: ") or "Instagram"
            tone = input("Tone [casual/professional/funny]: ") or "casual"
            post = cm.generate_post(topic, platform, tone)
            print("\n--- Generated Post ---\n", post["content"])
            print(f"\nSaved! ID: {post['id']}")

        elif choice == "3":
            keyword = input("Search keyword: ")
            results = cm.search_posts(keyword)
            if results:
                for p in results:
                    print(f"\nID {p['id']} | {p['topic']} | {p['platform']}\n{p['content'][:100]}...")
            else:
                print("No posts found.")

        elif choice == "4":
            posts = cm.list_posts()
            for p in posts:
                print(f"\nID {p['id']} | {p['topic']} | {p['created_at'][:10]}")

        elif choice == "5":
            print("Bye! All content saved to content_db.json")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
