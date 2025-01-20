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
            'content': content,
            'likes': 0  # Initialize likes to 0
        }

        # Add new post to the list
        blog_posts.append(new_post)

        # Save updated posts to JSON file
        save_posts(blog_posts)

        # Redirect to the home page
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Load existing posts
    blog_posts = load_posts()

    # Find the blog post with the given ID
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post with form data
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Save updated posts to JSON file
        save_posts(blog_posts)

        # Redirect to the home page
        return redirect(url_for('index'))

    # Else, it's a GET request
    return render_template('update.html', post=post)

@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Load existing posts
    blog_posts = load_posts()

    # Find the blog post with the given ID and remove it from the list
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save updated posts to JSON file
    save_posts(blog_posts)

    # Redirect to the home page
    return redirect(url_for('index'))

@app.route('/like/<int:post_id>')
def like(post_id):
    # Load existing posts
    blog_posts = load_posts()

    # Find the blog post with the given ID
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404

    # Increment the like count
    post['likes'] += 1

    # Save updated posts to JSON file
    save_posts(blog_posts)

    # Redirect to the home page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
