import os

file_path = "/Users/thomaskim/Cryptocasinomedia/scripts/update_articles.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace emails
content = content.replace("research@cryptocasinomedia.com", "cryptocasinomedia@gmail.com")
content = content.replace("compliance@cryptocasinomedia.com", "cryptocasinomedia@gmail.com")
content = content.replace("security@cryptocasinomedia.com", "cryptocasinomedia@gmail.com")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Email replacement in update_articles.py completed successfully!")
