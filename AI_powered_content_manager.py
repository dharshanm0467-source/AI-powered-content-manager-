from textblob import TextBlob

# Function to summarize text
def summarize_text(text):
    sentences = text.split('.')
    summary = '. '.join(sentences[:2])
    return summary

# Function to categorize content
def categorize_content(text):
    text = text.lower()

    if "python" in text or "programming" in text:
        return "Technology"
    elif "football" in text or "cricket" in text:
        return "Sports"
    elif "stock" in text or "market" in text:
        return "Finance"
    elif "health" in text or "fitness" in text:
        return "Health"
    else:
        return "General"

# Function to save content
def save_content(title, content):
    category = categorize_content(content)
    summary = summarize_text(content)

    with open("content_data.txt", "a") as file:
        file.write(f"\nTitle: {title}\n")
        file.write(f"Category: {category}\n")
        file.write(f"Summary: {summary}\n")
        file.write(f"Content: {content}\n")
        file.write("-" * 50 + "\n")

    print("Content saved successfully!")

# Main Program
while True:
    print("\nAI Powered Content Manager")
    print("1. Add Content")
    print("2. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        title = input("Enter title: ")
        content = input("Enter content: ")

        save_content(title, content)

    elif choice == "2":
        print("Exiting...")
        break

    else:
        print("Invalid choice!")
