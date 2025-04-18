from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.routes import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    return "Login page"

@bp.route('/logout')
def logout():
    return "Logout route"

@bp.route('/register', methods=['GET', 'POST'])
def register():
    return "Register page" 