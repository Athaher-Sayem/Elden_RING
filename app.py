from flask import Flask, render_template, request, jsonify, url_for
from models import db, Character, User, Review, Rating, Battle, CharacterStats
from sqlalchemy import func, desc, and_, or_
import random
import math
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elden.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ==================== INITIALIZATION ====================
def init_demo_data():
    """Initialize database with demo data"""
    
    # Demo Characters (20 characters with varied stats and descriptions)
    chars_data = [
        {
            "name": "Ranni",
            "title": "Witch of Moon",
            "magic_power": 95,
            "physical_power": 60,
            "weapon": "Dark Moon",
            "defense": 70,
            "speed": 85,
            "image": "/static/images/marika.jpg",
            "description": "The Witch of the Moon, seeking a different fate for the Lands Between."
        },
        {
            "name": "Malenia",
            "title": "Blade of Miquella",
            "magic_power": 98,
            "physical_power": 95,
            "weapon": "Waterfowl Dance",
            "defense": 75,
            "speed": 90,
            "image": "/static/images/1.jpg",
            "description": "Goddess of Rot, undefeated in combat. Her blade never knew defeat."
        },
        {
            "name": "Radahn",
            "title": "Starscourge",
            "magic_power": 90,
            "physical_power": 98,
            "weapon": "Greatsword",
            "defense": 88,
            "speed": 65,
            "image": "/static/images/marika.jpg",
            "description": "The Starscourge General who commands gravity itself in battle."
        },
        {
            "name": "Mohg",
            "title": "Lord of Blood",
            "magic_power": 88,
            "physical_power": 82,
            "weapon": "Blood Spear",
            "defense": 80,
            "speed": 75,
            "image": "/static/images/1.jpg",
            "description": "Omen King who seeks to become the Lord of Chaos and reshape reality."
        },
        {
            "name": "Blaidd",
            "title": "Half-Wolf Knight",
            "magic_power": 60,
            "physical_power": 85,
            "weapon": "Greatsword",
            "defense": 82,
            "speed": 80,
            "image": "/static/images/marika.jpg",
            "description": "Faithful knight with the form of a beast, loyal to Ranni's cause."
        },
        {
            "name": "Rykard",
            "title": "God Devouring Serpent",
            "magic_power": 85,
            "physical_power": 80,
            "weapon": "Serpent Blade",
            "defense": 85,
            "speed": 55,
            "image": "/static/images/1.jpg",
            "description": "Lord of Blasphemy who devoured rotten gods for power."
        },
        {
            "name": "Fia",
            "title": "Deathbed Companion",
            "magic_power": 70,
            "physical_power": 50,
            "weapon": "Cursed Dagger",
            "defense": 60,
            "speed": 70,
            "image": "/static/images/marika.jpg",
            "description": "A mysterious figure who seeks Death and an ancient destiny."
        },
        {
            "name": "Melina",
            "title": "Kindling Maiden",
            "magic_power": 80,
            "physical_power": 65,
            "weapon": "Flame",
            "defense": 72,
            "speed": 85,
            "image": "/static/images/1.jpg",
            "description": "Maiden with the ability to kindle the Erdtree itself."
        },
        {
            "name": "Godfrey",
            "title": "First Elden Lord",
            "magic_power": 75,
            "physical_power": 92,
            "weapon": "Axe of Godrick",
            "defense": 86,
            "speed": 70,
            "image": "/static/images/marika.jpg",
            "description": "The first Elden Lord and legendary warrior, also known as Hoarah Loux."
        },
        {
            "name": "Marika",
            "title": "Eternal Queen",
            "magic_power": 99,
            "physical_power": 90,
            "weapon": "Elden Rings",
            "defense": 95,
            "speed": 88,
            "image": "/static/images/1.jpg",
            "description": "The eternal queen who shaped the Lands Between and all demigods."
        },
        {
            "name": "Miquella",
            "title": "Lord of Grace",
            "magic_power": 92,
            "physical_power": 70,
            "weapon": "Cursed Prayer",
            "defense": 78,
            "speed": 82,
            "image": "/static/images/marika.jpg",
            "description": "Demigod of mercy trapped in a cocoon, seeking redemption."
        },
        {
            "name": "Godrick",
            "title": "The Grafted",
            "magic_power": 65,
            "physical_power": 72,
            "weapon": "Halberd",
            "defense": 70,
            "speed": 60,
            "image": "/static/images/1.jpg",
            "description": "A lord obsessed with grafting limbs to artificially gain power."
        },
        {
            "name": "Rennala",
            "title": "Queen of the Full Moon",
            "magic_power": 92,
            "physical_power": 55,
            "weapon": "Moonlight Greatsword",
            "defense": 75,
            "speed": 78,
            "image": "/static/images/marika.jpg",
            "description": "Queen of sorcery who rebirths demigods through magic and rebirth rituals."
        },
        {
            "name": "Starscourge Radahn",
            "title": "Mightiest General",
            "magic_power": 85,
            "physical_power": 99,
            "weapon": "Colossal Greatsword",
            "defense": 90,
            "speed": 70,
            "image": "/static/images/1.jpg",
            "description": "The mightiest warrior who mastered gravity and commands entire armies."
        },
        {
            "name": "Morgott",
            "title": "The Omen King",
            "magic_power": 82,
            "physical_power": 88,
            "weapon": "Cursed Greatsword",
            "defense": 85,
            "speed": 75,
            "image": "/static/images/marika.jpg",
            "description": "The Omen King, a mysterious demigod cursed by his own nature."
        },
        {
            "name": "Radagon",
            "title": "The Golden Consort",
            "magic_power": 90,
            "physical_power": 95,
            "weapon": "Hammer of the Erdtree",
            "defense": 92,
            "speed": 80,
            "image": "/static/images/1.jpg",
            "description": "Golden consort who defends the Erdtree with divine power."
        },
        {
            "name": "Fortissax",
            "title": "Death's Shadow",
            "magic_power": 94,
            "physical_power": 91,
            "weapon": "Ancient Blade",
            "defense": 88,
            "speed": 76,
            "image": "/static/images/marika.jpg",
            "description": "An ancient dragon who wields the power of death and decay."
        },
        {
            "name": "Astel",
            "title": "Naturalborn of the Void",
            "magic_power": 96,
            "physical_power": 78,
            "weapon": "Void Sword",
            "defense": 82,
            "speed": 87,
            "image": "/static/images/1.jpg",
            "description": "An alien entity from the void with incomprehensible power."
        },
        {
            "name": "Maliketh",
            "title": "The Black Blade",
            "magic_power": 88,
            "physical_power": 92,
            "weapon": "Black Blade",
            "defense": 89,
            "speed": 84,
            "image": "/static/images/marika.jpg",
            "description": "Guardian of Destined Death, wielding the power of fate itself."
        },
        {
            "name": "Placidusax",
            "title": "Lord of Scarlet Rot",
            "magic_power": 95,
            "physical_power": 94,
            "weapon": "Ancient Dragon Breath",
            "defense": 90,
            "speed": 72,
            "image": "/static/images/1.jpg",
            "description": "An ancient dragon lord corrupted by scarlet rot, immensely powerful."
        }
    ]
    
    # Ensure demo characters exist; add any missing by name (preserves user data)
    existing = {c.name for c in Character.query.all()}
    added = 0
    for char_data in chars_data:
        if char_data['name'] not in existing:
            char = Character(**char_data)
            db.session.add(char)
            added += 1
    if added:
        db.session.commit()
    
    # Demo Users
    if User.query.count() == 0:
        users = [
            User(username="player1", email="player1@elden.com"),
            User(username="player2", email="player2@elden.com"),
            User(username="analyst", email="analyst@elden.com"),
        ]
        for user in users:
            db.session.add(user)
        db.session.commit()
    
    # Demo Reviews and Ratings
    if Review.query.count() == 0:
        characters = Character.query.all()
        users = User.query.all()
        
        sample_reviews = [
            ("Incredible Power", "Marika's command over reality is unmatched. A true demigod.", 5),
            ("Deadly Efficiency", "Malenia's combat skills are unparalleled. Every move is lethal.", 5),
            ("Gravity Master", "Radahn's control over gravity makes him a force to be reckoned with.", 4),
            ("Chaotic Magic", "Mohg's blood magic is devastatingly effective in battle.", 4),
            ("Loyal Fighter", "Blaidd fights with honor and strength. A true warrior.", 4),
            ("Mysterious", "Ranni's motives are unclear, but her power is evident.", 3),
            ("Underestimated", "Don't let Fia's appearance fool you. She's dangerous.", 3),
        ]
        
        for i, char in enumerate(characters[:7]):
            for j, user in enumerate(users):
                if i + j < len(sample_reviews):
                    title, content, rating = sample_reviews[i + j]
                    review = Review(
                        character_id=char.id,
                        user_id=user.id,
                        title=title,
                        content=content,
                        rating=rating
                    )
                    db.session.add(review)
                    
                    rating_obj = Rating(
                        character_id=char.id,
                        user_id=user.id,
                        rating=rating
                    )
                    db.session.add(rating_obj)
        
        db.session.commit()
    
    # Demo Battles
    if Battle.query.count() == 0:
        characters = Character.query.all()
        users = User.query.all()
        
        battles_data = [
            (characters[0].id, characters[1].id, characters[1].id, 0.35, 0.65),
            (characters[2].id, characters[3].id, characters[2].id, 0.60, 0.40),
            (characters[4].id, characters[5].id, characters[5].id, 0.45, 0.55),
            (characters[0].id, characters[2].id, characters[2].id, 0.40, 0.60),
            (characters[1].id, characters[9].id, characters[9].id, 0.45, 0.55),
        ]
        
        for char1_id, char2_id, winner_id, prob1, prob2 in battles_data:
            battle = Battle(
                character1_id=char1_id,
                character2_id=char2_id,
                user_id=users[0].id,
                winner_id=winner_id,
                char1_strategy="balanced",
                char2_strategy="aggressive",
                char1_win_probability=prob1,
                char2_win_probability=prob2,
                simulation_rounds=1
            )
            db.session.add(battle)
        
        db.session.commit()

with app.app_context():
    db.create_all()
    init_demo_data()

# ==================== UTILITY FUNCTIONS ====================

def img_url(c):
    """Get proper image URL"""
    if isinstance(c.image, str):
        if c.image.startswith("http://") or c.image.startswith("https://") or c.image.startswith("/static/"):
            return c.image
        return url_for('static', filename=c.image)
    return url_for('static', filename='images/default.jpg')

def calculate_win_probability(char1, char2, strategy1="balanced", strategy2="balanced"):
    """
    Calculate win probability using Game Theory concepts
    Payoff Matrix approach
    """
    # Normalize stats to 0-1 range
    max_stat = 100
    char1_score = (char1.magic_power + char1.physical_power + char1.speed) / (3 * max_stat)
    char2_score = (char2.magic_power + char2.physical_power + char2.speed) / (3 * max_stat)
    
    # Strategy modifiers (simple payoff matrix concept)
    strategy_modifiers = {
        "aggressive": {"aggressive": 0.5, "defensive": 1.2, "balanced": 0.9},
        "defensive": {"aggressive": 0.8, "defensive": 0.5, "balanced": 0.9},
        "balanced": {"aggressive": 1.1, "defensive": 0.9, "balanced": 1.0}
    }
    
    mod1 = strategy_modifiers.get(strategy1, {}).get(strategy2, 1.0)
    mod2 = strategy_modifiers.get(strategy2, {}).get(strategy1, 1.0)
    
    char1_adjusted = char1_score * mod1
    char2_adjusted = char2_score * mod2
    
    total = char1_adjusted + char2_adjusted
    if total == 0:
        return 0.5, 0.5
    
    prob1 = char1_adjusted / total
    prob2 = char2_adjusted / total
    
    return prob1, prob2

# ==================== PAGES ====================

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/character/<int:char_id>')
def character_detail(char_id):
    return render_template("character_detail.html", char_id=char_id)

@app.route('/reviews')
def reviews_page():
    return render_template("reviews.html")

@app.route('/game-theory')
def game_theory_page():
    return render_template("game_theory.html")

@app.route('/analytics')
def analytics_page():
    return render_template("analytics.html")

@app.route('/add-character')
def add_character_page():
    return render_template("add_character.html")

# ==================== CHARACTER CRUD ====================

@app.route('/api/characters', methods=['GET'])
def get_characters():
    """Get all characters with optional filtering"""
    q = request.args.get("q", "").lower()
    sort_by = request.args.get("sort", "name")
    
    query = Character.query
    
    if q:
        query = query.filter(Character.name.ilike(f"%{q}%"))
    
    # Sorting options
    if sort_by == "magic":
        query = query.order_by(desc(Character.magic_power))
    elif sort_by == "physical":
        query = query.order_by(desc(Character.physical_power))
    elif sort_by == "overall":
        # This would require a calculated field; for now, sort by magic
        query = query.order_by(desc(Character.magic_power))
    else:
        query = query.order_by(Character.name)
    
    characters = query.all()
    return jsonify([c.to_dict() for c in characters])

@app.route('/api/characters/<int:char_id>', methods=['GET'])
def get_character(char_id):
    """Get single character details"""
    char = Character.query.get_or_404(char_id)
    char_dict = char.to_dict()
    
    # Add reviews and ratings
    reviews = Review.query.filter_by(character_id=char_id).all()
    ratings = Rating.query.filter_by(character_id=char_id).all()
    
    char_dict['reviews'] = [r.to_dict() for r in reviews]
    char_dict['ratings'] = [r.to_dict() for r in ratings]
    char_dict['review_count'] = len(reviews)
    
    # Battle statistics
    battles_as_char1 = Battle.query.filter_by(character1_id=char_id).all()
    battles_as_char2 = Battle.query.filter_by(character2_id=char_id).all()
    
    total_battles = len(battles_as_char1) + len(battles_as_char2)
    wins = sum(1 for b in battles_as_char1 if b.winner_id == char_id) + \
           sum(1 for b in battles_as_char2 if b.winner_id == char_id)
    
    char_dict['total_battles'] = total_battles
    char_dict['total_wins'] = wins
    char_dict['win_rate'] = round((wins / total_battles * 100) if total_battles > 0 else 0, 2)
    
    return jsonify(char_dict)

@app.route('/api/characters', methods=['POST'])
def create_character():
    """Create a new character"""
    try:
        d = request.json
        
        # Validate input
        if not d.get('name') or not d.get('title'):
            return jsonify({"error": "Name and title required"}), 400
        
        if Character.query.filter_by(name=d['name']).first():
            return jsonify({"error": "Character already exists"}), 400
        
        char = Character(
            name=d['name'],
            title=d['title'],
            magic_power=int(d.get('magic_power', 50)),
            physical_power=int(d.get('physical_power', 50)),
            weapon=d.get('weapon', ''),
            defense=int(d.get('defense', 50)),
            speed=int(d.get('speed', 50)),
            image=d.get('image', ''),
            description=d.get('description', '')
        )
        
        db.session.add(char)
        db.session.commit()
        
        return jsonify({"msg": "Character created successfully", "character": char.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/api/characters/<int:char_id>', methods=['POST'])
def update_character(char_id):
    """Update a character"""
    try:
        char = Character.query.get_or_404(char_id)
        d = request.json
        
        # Update fields
        if 'name' in d:
            char.name = d['name']
        if 'title' in d:
            char.title = d['title']
        if 'magic_power' in d:
            char.magic_power = int(d['magic_power'])
        if 'physical_power' in d:
            char.physical_power = int(d['physical_power'])
        if 'weapon' in d:
            char.weapon = d['weapon']
        if 'defense' in d:
            char.defense = int(d['defense'])
        if 'speed' in d:
            char.speed = int(d['speed'])
        if 'image' in d:
            char.image = d['image']
        if 'description' in d:
            char.description = d['description']
        
        db.session.commit()
        
        return jsonify({"msg": "Character updated successfully", "character": char.to_dict()})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/api/characters/<int:char_id>', methods=['DELETE'])
def delete_character(char_id):
    """Delete a character"""
    try:
        char = Character.query.get_or_404(char_id)
        db.session.delete(char)
        db.session.commit()
        
        return jsonify({"msg": "Character deleted successfully"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# ==================== REVIEW SYSTEM ====================

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    """Get all reviews with filtering"""
    char_id = request.args.get("character_id")
    user_id = request.args.get("user_id")
    
    query = Review.query
    
    if char_id:
        query = query.filter_by(character_id=char_id)
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    reviews = query.order_by(desc(Review.created_at)).all()
    return jsonify([r.to_dict() for r in reviews])

@app.route('/api/reviews', methods=['POST'])
def create_review():
    """Create a new review"""
    try:
        d = request.json
        
        # Validate
        if not all(k in d for k in ['character_id', 'user_id', 'title', 'content', 'rating']):
            return jsonify({"error": "Missing required fields"}), 400
        
        if int(d['rating']) < 1 or int(d['rating']) > 5:
            return jsonify({"error": "Rating must be 1-5"}), 400
        
        review = Review(
            character_id=int(d['character_id']),
            user_id=int(d['user_id']),
            title=d['title'],
            content=d['content'],
            rating=int(d['rating'])
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify({"msg": "Review created successfully", "review": review.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review"""
    try:
        review = Review.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        
        return jsonify({"msg": "Review deleted successfully"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# ==================== RATING SYSTEM ====================

@app.route('/api/ratings', methods=['GET'])
def get_ratings():
    """Get all ratings"""
    char_id = request.args.get("character_id")
    
    query = Rating.query
    
    if char_id:
        query = query.filter_by(character_id=char_id)
    
    ratings = query.all()
    return jsonify([r.to_dict() for r in ratings])

@app.route('/api/ratings', methods=['POST'])
def create_or_update_rating():
    """Create or update a rating"""
    try:
        d = request.json
        
        # Validate
        if not all(k in d for k in ['character_id', 'user_id', 'rating']):
            return jsonify({"error": "Missing required fields"}), 400
        
        if int(d['rating']) < 1 or int(d['rating']) > 5:
            return jsonify({"error": "Rating must be 1-5"}), 400
        
        # Check if rating exists
        rating = Rating.query.filter_by(
            character_id=int(d['character_id']),
            user_id=int(d['user_id'])
        ).first()
        
        if rating:
            rating.rating = int(d['rating'])
        else:
            rating = Rating(
                character_id=int(d['character_id']),
                user_id=int(d['user_id']),
                rating=int(d['rating'])
            )
            db.session.add(rating)
        
        db.session.commit()
        
        return jsonify({"msg": "Rating saved successfully", "rating": rating.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# ==================== GAME THEORY - BATTLE SIMULATION ====================

@app.route('/api/simulate-battle', methods=['POST'])
def simulate_battle():
    """Simulate a battle between two characters using Game Theory"""
    try:
        d = request.json
        
        char1_id = int(d.get('character1_id'))
        char2_id = int(d.get('character2_id'))
        char1_strategy = d.get('char1_strategy', 'balanced')
        char2_strategy = d.get('char2_strategy', 'balanced')
        rounds = int(d.get('rounds', 1))
        
        char1 = Character.query.get_or_404(char1_id)
        char2 = Character.query.get_or_404(char2_id)
        
        # Calculate win probabilities using Game Theory
        prob1, prob2 = calculate_win_probability(char1, char2, char1_strategy, char2_strategy)
        
        # Simulate winner
        winner_id = char1_id if random.random() < prob1 else char2_id
        
        # Save battle to database
        battle = Battle(
            character1_id=char1_id,
            character2_id=char2_id,
            winner_id=winner_id,
            char1_strategy=char1_strategy,
            char2_strategy=char2_strategy,
            char1_win_probability=prob1,
            char2_win_probability=prob2,
            simulation_rounds=rounds
        )
        
        db.session.add(battle)
        db.session.commit()
        
        # Create detailed battle report
        char1_total = char1.magic_power + char1.physical_power + char1.speed
        char2_total = char2.magic_power + char2.physical_power + char2.speed
        
        return jsonify({
            "battle": battle.to_dict(),
            "char1": {
                "name": char1.name,
                "total_power": char1_total,
                "strategy": char1_strategy,
                "win_probability": round(prob1 * 100, 2)
            },
            "char2": {
                "name": char2.name,
                "total_power": char2_total,
                "strategy": char2_strategy,
                "win_probability": round(prob2 * 100, 2)
            },
            "winner": {
                "id": winner_id,
                "name": char1.name if winner_id == char1_id else char2.name
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/api/battles', methods=['GET'])
def get_battles():
    """Get all battles with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    paginated = Battle.query.order_by(desc(Battle.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        "battles": [b.to_dict() for b in paginated.items],
        "total": paginated.total,
        "pages": paginated.pages,
        "current_page": page
    })

# ==================== ANALYTICS - JOIN QUERIES & AGGREGATIONS ====================

@app.route('/api/analytics/top-characters', methods=['GET'])
def top_characters():
    """Get top characters by various metrics (JOIN + Aggregation)"""
    metric = request.args.get('metric', 'rating')
    limit = request.args.get('limit', 10, type=int)
    
    if metric == 'rating':
        # JOIN Character with Rating, GROUP BY, ORDER BY AVG
        results = db.session.query(
            Character,
            func.count(Rating.id).label('rating_count'),
            func.avg(Rating.rating).label('avg_rating')
        ).outerjoin(Rating, Character.id == Rating.character_id)\
         .group_by(Character.id)\
         .order_by(desc(func.avg(Rating.rating)))\
         .limit(limit).all()
        
        return jsonify([{
            "character": char.to_dict(),
            "rating_count": count,
            "avg_rating": round(float(avg) if avg else 0, 2)
        } for char, count, avg in results])
    
    elif metric == 'reviews':
        # JOIN Character with Review, GROUP BY COUNT
        results = db.session.query(
            Character,
            func.count(Review.id).label('review_count')
        ).outerjoin(Review, Character.id == Review.character_id)\
         .group_by(Character.id)\
         .order_by(desc(func.count(Review.id)))\
         .limit(limit).all()
        
        return jsonify([{
            "character": char.to_dict(),
            "review_count": count
        } for char, count in results])
    
    elif metric == 'battles':
        # Battle statistics
        results = db.session.query(
            Character,
            func.count(Battle.id).label('total_battles'),
            func.sum(func.case(
                (Battle.winner_id == Character.id, 1)
            )).label('total_wins')
        ).outerjoin(Battle, 
                   or_(Battle.character1_id == Character.id, 
                       Battle.character2_id == Character.id)
        ).group_by(Character.id)\
         .order_by(desc(func.sum(func.case((Battle.winner_id == Character.id, 1)))))\
         .limit(limit).all()
        
        return jsonify([{
            "character": char.to_dict(),
            "total_battles": battles or 0,
            "total_wins": wins or 0,
            "win_rate": round((wins / battles * 100) if battles and battles > 0 else 0, 2)
        } for char, battles, wins in results])
    
    else:
        # Power ranking
        results = Character.query.order_by(
            desc(Character.magic_power + Character.physical_power)
        ).limit(limit).all()
        
        return jsonify([char.to_dict() for char in results])

@app.route('/api/analytics/character-comparison', methods=['GET'])
def character_comparison():
    """Compare multiple characters"""
    char_ids = request.args.getlist('ids')
    
    if not char_ids:
        return jsonify({"error": "No character IDs provided"}), 400
    
    characters = Character.query.filter(Character.id.in_(char_ids)).all()
    
    comparison = []
    for char in characters:
        avg_rating = db.session.query(func.avg(Rating.rating))\
            .filter(Rating.character_id == char.id).scalar() or 0
        
        review_count = Review.query.filter_by(character_id=char.id).count()
        
        battles = Battle.query.filter(
            or_(Battle.character1_id == char.id, Battle.character2_id == char.id)
        ).all()
        
        wins = sum(1 for b in battles if b.winner_id == char.id)
        
        comparison.append({
            "character": char.to_dict(),
            "avg_rating": round(float(avg_rating), 2),
            "review_count": review_count,
            "total_battles": len(battles),
            "total_wins": wins,
            "win_rate": round((wins / len(battles) * 100) if battles else 0, 2),
            "power_score": char._calculate_overall_score()
        })
    
    return jsonify(comparison)

@app.route('/api/analytics/database-stats', methods=['GET'])
def database_stats():
    """Get overall database statistics"""
    
    total_characters = Character.query.count()
    total_users = User.query.count()
    total_reviews = Review.query.count()
    total_ratings = Rating.query.count()
    total_battles = Battle.query.count()
    
    avg_character_rating = db.session.query(func.avg(Rating.rating)).scalar() or 0
    
    # Most rated character
    most_rated = db.session.query(
        Character,
        func.count(Rating.id).label('rating_count')
    ).outerjoin(Rating, Character.id == Rating.character_id)\
     .group_by(Character.id)\
     .order_by(desc(func.count(Rating.id)))\
     .first()
    
    # Most reviewed character
    most_reviewed = db.session.query(
        Character,
        func.count(Review.id).label('review_count')
    ).outerjoin(Review, Character.id == Review.character_id)\
     .group_by(Character.id)\
     .order_by(desc(func.count(Review.id)))\
     .first()
    
    # Most battled character
    most_battled = db.session.query(
        Character,
        func.count(Battle.id).label('battle_count')
    ).outerjoin(Battle, 
               or_(Battle.character1_id == Character.id, 
                   Battle.character2_id == Character.id)
    ).group_by(Character.id)\
     .order_by(desc(func.count(Battle.id)))\
     .first()
    
    return jsonify({
        "total_characters": total_characters,
        "total_users": total_users,
        "total_reviews": total_reviews,
        "total_ratings": total_ratings,
        "total_battles": total_battles,
        "avg_character_rating": round(float(avg_character_rating), 2),
        "most_rated_character": {
            "id": most_rated[0].id,
            "name": most_rated[0].name,
            "rating_count": most_rated[1]
        } if most_rated else None,
        "most_reviewed_character": {
            "id": most_reviewed[0].id,
            "name": most_reviewed[0].name,
            "review_count": most_reviewed[1]
        } if most_reviewed else None,
        "most_battled_character": {
            "id": most_battled[0].id,
            "name": most_battled[0].name,
            "battle_count": most_battled[1]
        } if most_battled else None
    })

@app.route('/api/analytics/search', methods=['GET'])
def advanced_search():
    """Advanced search with filtering"""
    q = request.args.get('q', '').lower()
    min_magic = request.args.get('min_magic', 0, type=int)
    max_magic = request.args.get('max_magic', 100, type=int)
    min_rating = request.args.get('min_rating', 0, type=float)
    
    query = Character.query
    
    if q:
        query = query.filter(or_(
            Character.name.ilike(f"%{q}%"),
            Character.title.ilike(f"%{q}%"),
            Character.weapon.ilike(f"%{q}%")
        ))
    
    if min_magic or max_magic:
        query = query.filter(Character.magic_power.between(min_magic, max_magic))
    
    characters = query.all()
    
    if min_rating > 0:
        # Filter by minimum rating
        filtered = []
        for char in characters:
            avg_rating = db.session.query(func.avg(Rating.rating))\
                .filter(Rating.character_id == char.id).scalar() or 0
            if avg_rating >= min_rating:
                filtered.append(char)
        characters = filtered
    
    return jsonify([c.to_dict() for c in characters])

# ==================== USERS ====================

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        d = request.json
        
        if not all(k in d for k in ['username', 'email']):
            return jsonify({"error": "Username and email required"}), 400
        
        if User.query.filter_by(username=d['username']).first():
            return jsonify({"error": "Username already exists"}), 400
        
        user = User(username=d['username'], email=d['email'])
        db.session.add(user)
        db.session.commit()
        
        return jsonify({"msg": "User created successfully", "user": user.to_dict()}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)