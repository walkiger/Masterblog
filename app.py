from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Load blog posts from JSON file
def load_posts():
    with open('blog_posts.json', 'r') as file:
        return json.load(file)

# Save blog posts to JSON file
def save_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
