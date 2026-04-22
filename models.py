from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('Review', backref='author', lazy=True, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='user', lazy=True, cascade='all, delete-orphan')
    battles_created = db.relationship('Battle', backref='creator', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

# Character Model (Enhanced)
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    title = db.Column(db.String(100), nullable=False)
    magic_power = db.Column(db.Integer, default=50)
    physical_power = db.Column(db.Integer, default=50)
    weapon = db.Column(db.String(100))
    defense = db.Column(db.Integer, default=50)
    speed = db.Column(db.Integer, default=50)
    image = db.Column(db.String(500))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('Review', backref='character', lazy=True, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='character', lazy=True, cascade='all, delete-orphan')
    battles_as_char1 = db.relationship('Battle', foreign_keys='Battle.character1_id', backref='char1', lazy=True)
    battles_as_char2 = db.relationship('Battle', foreign_keys='Battle.character2_id', backref='char2', lazy=True)
    
    def to_dict(self):
        avg_rating = db.session.query(db.func.avg(Rating.rating)).filter(Rating.character_id == self.id).scalar() or 0
        review_count = Review.query.filter_by(character_id=self.id).count()
        
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'magic_power': self.magic_power,
            'physical_power': self.physical_power,
            'weapon': self.weapon,
            'defense': self.defense,
            'speed': self.speed,
            'image': self.image,
            'description': self.description,
            'avg_rating': round(float(avg_rating), 2),
            'review_count': review_count,
            'overall_score': self._calculate_overall_score(),
            'created_at': self.created_at.isoformat()
        }
    
    def _calculate_overall_score(self):
        """Calculate overall power score"""
        return (self.magic_power + self.physical_power + self.defense + self.speed) / 4

# Review Model
class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'character_id': self.character_id,
            'user_id': self.user_id,
            'username': self.author.username,
            'title': self.title,
            'content': self.content,
            'rating': self.rating,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Rating Model
class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure one rating per user per character
    __table_args__ = (db.UniqueConstraint('character_id', 'user_id', name='unique_user_character_rating'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'character_id': self.character_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'created_at': self.created_at.isoformat()
        }

# Battle/Game Theory Model
class Battle(db.Model):
    __tablename__ = 'battle'
    id = db.Column(db.Integer, primary_key=True)
    character1_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False, index=True)
    character2_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    char1_strategy = db.Column(db.String(100))  # 'aggressive', 'defensive', 'balanced'
    char2_strategy = db.Column(db.String(100))
    char1_win_probability = db.Column(db.Float)
    char2_win_probability = db.Column(db.Float)
    simulation_rounds = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'character1_id': self.character1_id,
            'character2_id': self.character2_id,
            'char1_name': self.char1.name,
            'char2_name': self.char2.name,
            'winner_id': self.winner_id,
            'winner_name': self.winner.name if self.winner_id else None,
            'char1_strategy': self.char1_strategy,
            'char2_strategy': self.char2_strategy,
            'char1_win_probability': round(self.char1_win_probability, 2) if self.char1_win_probability else 0,
            'char2_win_probability': round(self.char2_win_probability, 2) if self.char2_win_probability else 0,
            'simulation_rounds': self.simulation_rounds,
            'created_at': self.created_at.isoformat()
        }

# Denormalized view for analytics (cached stats)
class CharacterStats(db.Model):
    __tablename__ = 'character_stats'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False, unique=True)
    total_battles = db.Column(db.Integer, default=0)
    total_wins = db.Column(db.Integer, default=0)
    win_rate = db.Column(db.Float, default=0)
    avg_rating = db.Column(db.Float, default=0)
    total_reviews = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'character_id': self.character_id,
            'total_battles': self.total_battles,
            'total_wins': self.total_wins,
            'win_rate': round(self.win_rate, 2),
            'avg_rating': round(self.avg_rating, 2),
            'total_reviews': self.total_reviews
        }