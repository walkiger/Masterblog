from flask import Flask, request, render_template, redirect, url_for
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

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Load existing posts
        blog_posts = load_posts()

        # Get form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Create a new blog post with a unique ID
        new_post = {
            'id': blog_posts[-1]['id'] + 1 if blog_posts else 1,
            'author': author,
            'title': title,
            'content': content
        }

        # Add new post to the list
        blog_posts.append(new_post)

        # Save updated posts to JSON file
        save_posts(blog_posts)

        # Redirect to the home page
        return redirect(url_for('index'))

    return render_template('add.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
