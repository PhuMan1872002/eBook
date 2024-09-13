from flask import render_template, request, redirect, flash, url_for, jsonify, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from .dao import load_books, load_book, auth_user, check_account, create_user, reset_password, load_comments, count_comments, add_comment
from .utils import upload_avatar, send_email, generate_reset_code, cart_stats
from .decorators import annonymous_user
from app import mail


def index():
    return render_template('pages/index.html', 
                        lastest=load_books(latest=True)
                    )


def collections():
    return render_template('pages/collections.html')


def detail(id):
    return render_template('pages/detail.html', 
                        book=load_book(book_id=id),
                        comments=load_comments(book=id, page=request.args.get('comment', 1, type=int)),
                        count=count_comments(book=id)
                    )


def about():
    return render_template('pages/about.html')


def login_admin():
    email = request.form.get('email')
    password = request.form.get('password')
    user = auth_user(email=email, password=password)

    if user and user.is_admin():
        flash(f"Welcome to {user.username} comeback!", category="success")
        login_user(user=user)
        return redirect(url_for('admin.index'))

    flash("Invalid email or password. Please try again.", category="warning")
    return redirect(url_for('admin.index'))


@annonymous_user
def login():
    next = request.args.get('next')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        user = auth_user(email=email, password=password)
        
        if user:
            flash(f"Welcome to {user.username} comeback!", category="success")
            login_user(user=user, remember=remember)
            return redirect(next or url_for('index'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('pages/login.html', next=next)


@annonymous_user
def register():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('pwd')
        confirm_pwd = request.form.get('confirm_pwd')
        avatar = request.files.get('avatar')
        
        if password.strip() != confirm_pwd.strip():
            flash('Invalid password or confirm not match. Please try again.', 'warning')
            return render_template('pages/register.html')
        
        if check_account(email=email, username=username):
            flash('Invalid username or email. Please use different username or email', 'warning')
            return render_template('pages/register.html')
        
        avatar_url = upload_avatar(file_name=avatar) if avatar else None
        
        account = create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            avatar=avatar_url
        )
        
        if account:
            flash(f"Account {account.username} created successfully!", category="success")
            return redirect(url_for('login'))
        
    return render_template('pages/register.html')


@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
def profile():
    return render_template('pages/profile.html')


@login_required
def change_password():
    password = request.form.get('pwd')
    new_pwd = request.form.get('new_pwd')
        
    if password.strip() == new_pwd.strip():
        flash('New password must be different from the old password.', 'warning')
        return render_template('pages/profile.html')
    
    user = reset_password(username=current_user.username, new_password=new_pwd)
    if user:
        flash('Change password successful.', 'success')
        logout_user()
        return redirect(url_for('index'))
    
    
@annonymous_user
def forgot_password():
    email = request.form.get('find_email')
    account = check_account(email=email)
    
    if not account:
        flash(f'Not found {email}.', 'warning')
        return render_template('pages/login.html')
    
    reset_code = generate_reset_code(user=account)
    message = f"""
                Hey ✌️, {account.last_name} {account.first_name}\n
                We've sent you the code: {reset_code} to reset your password.\n
                𝄃𝄃𝄂𝄂𝄀𝄁𝄃𝄂𝄂𝄃\n
                Code: {reset_code}\n
                𝄃𝄃𝄂𝄂𝄀𝄁𝄃𝄂𝄂𝄃\n
                Have A Good Day ❤️.
                """
    msg = send_email(subject="Password Reset Code 🔒", content=message, to_email=email)
    mail.send(msg)
    return redirect(url_for('index'))


@annonymous_user
def reset_password():
    if request.method.__eq__('POST'):
        otp = request.form.get('otp')
        new_password = request.form.get('new_pwd')
        account = check_account(otp=otp)
        
        if not account:
            flash(f'Invalid OTP.', 'warning')
            return redirect(url_for('reset_password'))
        else:
            flash(f'Change password successful', 'success')
            account.reset_code = None
            account.set_password(password=new_password)
            account.save() 
            return redirect(url_for('login'))
        
    return render_template('pages/set_password.html')


def comment():
    try:
        comment = add_comment(
                content=request.json.get('content'),
                book=request.json.get('id'))
        count = count_comments(book=request.json.get('id'))
        return jsonify(
            {
                'status': 201,
                'count': count,
                'data': {
                    'id': comment.id,
                    'content': comment.content,
                    'user': {
                        'full_name': comment.user.full_name(),
                        'username': comment.user.username,
                        'avatar': comment.user.avatar,
                    },
                    'date_created': comment.date_created
                }
            },
        )
    except:
        return jsonify({
                'status':  500,
                'error': 'An error occurred'
            })


def cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('title')
    price = data.get('price')

    cart = session.get('cart')
    
    if not cart:
        cart = {}

    if id in cart:
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:
        cart[id] = {
            "id": id,
            "title": name,
            "price": price,
            "quantity": 1
        }

    session["cart"] = cart

    return jsonify(cart_stats(cart))


