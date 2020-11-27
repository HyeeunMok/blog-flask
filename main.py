from flask import Flask, render_template, request
import requests
import smtplib


posts_url = "https://api.npoint.io/43644ec4f0013682fc0d"
posts = requests.get(posts_url).json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        send_email(name, email, phone, message)
        return render_template('contact.html', success_message=True)
    return render_template("contact.html", success_message=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone:{phone}\nMessage: {message}"
    # Replace to your email and password
    sender_email = "xxxx@gmail.com"
    sender_password = "xxxxx"
    recipient = email
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=sender_email, password=sender_password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=recipient,
            msg=email_message)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
