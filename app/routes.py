from app import app
from flask import render_template, jsonify, request, redirect, url_for
from app.models import *
from app.football_api import get_fixtures
from datetime import datetime, timezone
from app.forms import *
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_

@app.route('/')
def index():
    future_fixtures = Fixture.get_next_fixtures()
    print(future_fixtures)
    return render_template('index.html', current_page='Trang chủ', fixtures=future_fixtures)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.re_password.data:
            user = User(email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', current_page='Đăng ký', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(and_(User.email==form.email.data, User.password==form.password.data)).first()
        if user is not None:
            is_authenticated = login_user(user, remember=True)
            if is_authenticated:
                print('hello')
                next = request.args.get('next', 'index')
                return redirect(url_for(next))
    return render_template('login.html', current_page='Đăng nhập', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/update_api')
@login_required
def update_api():
    fixtures = get_fixtures()
    fixtures = fixtures['response']
    for fixture in fixtures:
        venue_dict = fixture['fixture']['venue']
        venue = Venue.add(venue_dict['id'], venue_dict['name'], venue_dict['city'])
        
        home_team_dict = fixture['teams']['home']
        away_team_dict = fixture['teams']['away']
        home_team = Team.add(home_team_dict['id'], home_team_dict['name'], home_team_dict['logo'])
        away_team = Team.add(away_team_dict['id'], away_team_dict['name'], away_team_dict['logo'])

        _round = Round.add(fixture['league']['round'])

        ft_dict = fixture['fixture']
        print(ft_dict['date'])
        ft = Fixture.add(
            ft_dict['id'],
            ft_dict['referee'],
            ft_dict['date'],
            # ft_dict['date'],
            ft_dict['timestamp'],
            venue.venue_id,
            fixture['goals']['home'],
            fixture['goals']['away'],
            _round.round_id,
            home_team.team_id,
            away_team.team_id,
            fixture['score']['halftime']['home'],
            fixture['score']['halftime']['away'],
            fixture['score']['fulltime']['home'],
            fixture['score']['fulltime']['away'],
            fixture['score']['extratime']['home'],
            fixture['score']['extratime']['away'],
            fixture['score']['penalty']['home'],
            fixture['score']['penalty']['away'],
        )
    return jsonify(fixtures)