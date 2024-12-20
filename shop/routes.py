from shop import app
from flask import render_template, redirect, url_for, flash, request
from shop.models import Item, User
from shop.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from shop import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/product', methods=['GET', 'POST'])
def products_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(item_name=purchased_item).first()
        if p_item_object:
                flash(f"Congratulations! You purchased {p_item_object.item_name} for {p_item_object.item_price}$", category='success')
        else:
            flash(f"Unfortunately, an error has occured {p_item_object.item_name}!", category='danger')
        return redirect(url_for('products_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        return render_template('products.html', items=items, purchase_form=purchase_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        create_user = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(create_user)
        db.session.commit()
        login_user(create_user)
        flash(f"Account created successfully! You are now logged in as {create_user.username}", category='success')
        return redirect(url_for('products_page'))
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(f'An error has occured while creating user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('products_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/checkout')
def checkout_page():
    return render_template('checkout.html')




