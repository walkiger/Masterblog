from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

def load_posts():
    """
    Load blog posts from the JSON file.

    Returns:
        list: A list of blog posts.
    """
    with open('blog_posts.json', 'r') as file:
        return json.load(file)

def save_posts(posts):
    """
    Save blog posts to the JSON file.

    Args:
        posts (list): A list of blog posts.
    """
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)

@app.route('/')
def index():
    """
    Display the home page with all blog posts.

    Returns:
        str: Rendered HTML template for the home page.
    """
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle the addition of a new blog post. Displays a form for adding a new blog post on GET request,
    and saves the new blog post on POST request.

    Returns:
        str: Rendered HTML template for the add page or a redirection to the home page.
    """
    if request.method == 'POST':
        blog_posts = load_posts()

        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        new_post = {
            'id': blog_posts[-1]['id'] + 1 if blog_posts else 1,
            'author': author,
            'title': title,
            'content': content,
            'likes': 0
        }

        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handle the update of an existing blog post. Displays a form for updating the blog post on GET request,
    and saves the updated blog post on POST request.

    Args:
        post_id (int): The ID of the blog post to update.

    Returns:
        str: Rendered HTML template for the update page or a redirection to the home page.
    """
    blog_posts = load_posts()

    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)

@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Handle the deletion of a blog post.

    Args:
        post_id (int): The ID of the blog post to delete.

    Returns:
        str: Redirection to the home page.
    """
    blog_posts = load_posts()

    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    save_posts(blog_posts)
    return redirect(url_for('index'))

@app.route('/like/<int:post_id>')
def like(post_id):
    """
    Handle the liking of a blog post by incrementing its like count.

    Args:
        post_id (int): The ID of the blog post to like.

    Returns:
        str: Redirection to the home page.
    """
    blog_posts = load_posts()

    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404

    if 'likes' not in post:
        post['likes'] = 0

    post['likes'] += 1

    save_posts(blog_posts)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
