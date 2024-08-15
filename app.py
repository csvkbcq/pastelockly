from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import SnippetForm, DecryptForm
from models import db, Snippet
from cryptography.fernet import Fernet, InvalidToken
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snippets.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

def encrypt_content(content, secret_key):
    cipher_suite = Fernet(secret_key)
    return cipher_suite.encrypt(content.encode())

def decrypt_content(encrypted_content, secret_key):
    cipher_suite = Fernet(secret_key)
    try:
        return cipher_suite.decrypt(encrypted_content).decode()
    except InvalidToken:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SnippetForm()
    if form.validate_on_submit():
        content = form.content.data
        secret_key = form.secret_key.data
        encrypted_content = None

        if secret_key:
            secret_key = Fernet.generate_key()
            encrypted_content = encrypt_content(content, secret_key)
            content = None

        snippet = Snippet(content=content, encrypted_content=encrypted_content, secret_key=secret_key)
        db.session.add(snippet)
        db.session.commit()
        return render_template('result.html', url=request.host_url + 'view/' + str(snippet.id))
    return render_template('index.html', form=form)

@app.route('/view/<int:id>', methods=['GET', 'POST'])
def view(id):
    snippet = Snippet.query.get_or_404(id)
    form = DecryptForm()
    
    if snippet.encrypted_content:
        if form.validate_on_submit():
            secret_key = form.secret_key.data
            decrypted_content = decrypt_content(snippet.encrypted_content, secret_key)
            if decrypted_content:
                return render_template('view.html', content=decrypted_content)
            else:
                flash('Invalid Secret Key!', 'danger')
        return render_template('view.html', form=form, requires_decryption=True)
    else:
        return render_template('view.html', content=snippet.content)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
