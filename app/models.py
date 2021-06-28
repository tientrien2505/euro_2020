from app import db, app
from datetime import datetime
from flask_login import UserMixin
import time

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(10))
    email = db.Column(db.String(50))

    def get_id(self):
        try:
            return self.user_id
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')
    
    @classmethod
    def get(cls, user_id):
        return User.query.filter_by(user_id=user_id).first()

class Price(db.Model):
    __tablename__ = 'price'
    price_id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('round.round_id'))
    cost = db.Column(db.Float, default=10000)


class UserFixture(db.Model):
    __tablename__ = 'user_fixture'
    user_fixture_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    fixture_id = db.Column(db.Integer, db.ForeignKey('fixture.fixture_id'))

class Round(db.Model):
    __tablename__ = 'round'
    round_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    fixture = db.relationship('Fixture', backref='_round', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    @classmethod
    def add(cls, name):
        _round = Round.query.filter_by(name=name).first()
        if _round is None:
            _round = Round(name)
            db.session.add(_round)
            db.session.commit()
        return _round

class Fixture(db.Model):
    __tablename__ = 'fixture'
    fixture_id = db.Column(db.Integer, primary_key=True)
    referee = db.Column(db.String(100))
    date = db.Column(db.String(25))
    timestamp = db.Column(db.String(10))
    # date = db.Column(db.String(30))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'))
    home_goal = db.Column(db.Integer)
    away_goal = db.Column(db.Integer)
    fixture_round = db.Column(db.Integer, db.ForeignKey('round.round_id'))
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    score_halftime_home = db.Column(db.Integer)
    score_halftime_away = db.Column(db.Integer)
    score_fulltime_home = db.Column(db.Integer)
    score_fulltime_away = db.Column(db.Integer)
    score_extratime_home = db.Column(db.Integer)
    score_extratime_away = db.Column(db.Integer)
    score_penalty_home = db.Column(db.Integer)
    score_penalty_away = db.Column(db.Integer)


    def __init__(self
    , fixture_id
    , referee
    , date
    , timestamp
    , venue_id
    , home_goal
    , away_goal
    , fixture_round
    , home_team_id
    , away_team_id
    , score_halftime_home
    , score_halftime_away
    , score_fulltime_home
    , score_fulltime_away
    , score_extratime_home
    , score_extratime_away
    , score_penalty_home
    , score_penalty_away
    ):
        self.fixture_id = fixture_id
        self.referee = referee
        self.date = date
        self.timestamp = timestamp
        self.venue_id = venue_id
        self.home_goal = home_goal
        self.away_goal = away_goal
        self.fixture_round = fixture_round
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.score_halftime_home = score_halftime_home
        self.score_halftime_away = score_halftime_away
        self.score_fulltime_home = score_fulltime_home
        self.score_fulltime_away = score_fulltime_away
        self.score_extratime_home = score_extratime_home
        self.score_extratime_away = score_extratime_away
        self.score_penalty_home = score_penalty_home
        self.score_penalty_away = score_penalty_away

    @classmethod
    def add(cls
    , fixture_id
    , referee
    , date
    , timestamp
    , venue_id
    , home_goal
    , away_goal
    , fixture_round
    , home_team_id
    , away_team_id
    , score_halftime_home
    , score_halftime_away
    , score_fulltime_home
    , score_fulltime_away
    , score_extratime_home
    , score_extratime_away
    , score_penalty_home
    , score_penalty_away
    ):
        fixture = Fixture.query.filter_by(fixture_id=fixture_id).first()
        if fixture is None:
            fixture = Fixture(
            fixture_id
            , referee
            , date
            , timestamp
            , venue_id
            , home_goal
            , away_goal
            , fixture_round
            , home_team_id
            , away_team_id
            , score_halftime_home
            , score_halftime_away
            , score_fulltime_home
            , score_fulltime_away
            , score_extratime_home
            , score_extratime_away
            , score_penalty_home
            , score_penalty_away)
            db.session.add(fixture)
            db.session.commit()
        else:
            fixture.fixture_id = fixture_id
            fixture.referee = referee
            fixture.date = date
            fixture.timestamp = timestamp
            fixture.venue_id = venue_id
            fixture.home_goal = home_goal
            fixture.away_goal = away_goal
            fixture.fixture_round = fixture_round
            fixture.home_team_id = home_team_id
            fixture.away_team_id = away_team_id
            fixture.score_halftime_home = score_halftime_home
            fixture.score_halftime_away = score_halftime_away
            fixture.score_fulltime_home = score_fulltime_home
            fixture.score_fulltime_away = score_fulltime_away
            fixture.score_extratime_home = score_extratime_home
            fixture.score_extratime_away = score_extratime_away
            fixture.score_penalty_home = score_penalty_home
            fixture.score_penalty_away = score_penalty_away
            db.session.commit()
            
        return fixture

    @classmethod
    def get_next_fixtures(cls):
        current = time.time()
        future_fixtures = Fixture.query.filter(Fixture.timestamp > current).all()
        return future_fixtures

class Team(db.Model):
    __tablename__ = 'team'
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    logo = db.Column(db.String(100))
    fixture_home = db.relationship('Fixture', foreign_keys='Fixture.home_team_id', backref='home_team', lazy='dynamic')
    fixture_away = db.relationship('Fixture', foreign_keys='Fixture.away_team_id', backref='away_team', lazy='dynamic')

    def __init__(self, team_id, name, logo):
        self.team_id = team_id
        self.name = name
        self.logo = logo

    @classmethod
    def add(cls, team_id, name, logo):
        team = Team.query.filter_by(team_id=team_id).first()
        if team is None:
            team = Team(team_id, name, logo)
            db.session.add(team)
            db.session.commit()
        return team

class Venue(db.Model):
    __tablename__ = 'venue'
    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    city = db.Column(db.String(50))
    fixture = db.relationship(Fixture, backref='venue', lazy=True)

    def __init__(self, venue_id, name, city):
        self.venue_id = venue_id
        self.name = name
        self.city = city

    @classmethod
    def add(cls, venue_id, name, city):
        venue = Venue.query.filter_by(venue_id=venue_id).first()
        if venue is None:
            venue = Venue(venue_id, name, city)
            db.session.add(venue)
            db.session.commit()
        return venue