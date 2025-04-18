from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.routes import bp
from app.models import Event
from app import db

@bp.route('/events')
@login_required
def list_events():
    return "Events list"

@bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event():
    return "Create event"

@bp.route('/events/<int:id>')
@login_required
def view_event(id):
    return f"View event {id}" 