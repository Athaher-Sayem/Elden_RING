# 🎮 Elden Ring DBMS - Advanced Character Database System

A comprehensive full-stack web application built with Flask, SQLAlchemy, and advanced DBMS concepts. This system demonstrates enterprise-level database design, Game Theory simulations, and data analytics.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Database Design](#-database-design)
- [API Documentation](#-api-documentation)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [Usage Examples](#-usage-examples)
- [Advanced Features](#-advanced-features)
- [Project Structure](#-project-structure)

---

## ✨ Features

### 1. **Advanced DBMS System**
- ✅ Relational database with normalized tables (SQLite)
- ✅ Foreign key relationships and constraints
- ✅ CRUD operations on all entities
- ✅ JOIN queries combining multiple tables
- ✅ Aggregation queries (COUNT, AVG, GROUP BY)
- ✅ Indexed searches for performance optimization
- ✅ Transaction-like operations for data consistency

### 2. **Character Management**
- Add, edit, delete, and search characters
- Store comprehensive stats: Magic Power, Physical Power, Defense, Speed
- Weapon and description tracking
- Image management with URL support
- Calculated overall power scores

### 3. **Review & Rating System**
- Users can leave detailed reviews with ratings (1-5)
- Aggregate ratings and review counts
- JOIN queries for character-review relationships
- Recent review display with sorting options

### 4. **Game Theory Battle Simulation**
- Simulate battles between two characters
- Payoff matrix model for strategy analysis
- Three strategy types: Aggressive, Defensive, Balanced
- Win probability calculations based on stats and strategies
- Nash equilibrium concepts applied to character matchups
- Full battle history tracking

### 5. **Analytics Dashboard**
- Database statistics (total characters, users, reviews, battles)
- Top characters by various metrics
- Advanced filtering and search
- Character comparison tool
- Win rate calculations
- Rating aggregations

### 6. **Multi-Page Interface**
- 🏠 Home page with character browsing
- 📄 Character detail pages
- ➕ Add/Edit character pages
- 📝 Reviews and ratings system
- ⚔️ Battle Arena (Game Theory simulation)
- 📊 Analytics Dashboard

---

## 🏗️ Architecture

```
Frontend (JavaScript/HTML/CSS)
         ↓
REST API (Flask)
         ↓
ORM Layer (SQLAlchemy)
         ↓
Database (SQLite)
```

### Tech Stack
- **Backend**: Flask 3.1.3, SQLAlchemy 2.0.49
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **APIs**: RESTful JSON endpoints

---

## 🗄️ Database Design

### Entity-Relationship Diagram

```
┌─────────────┐         ┌─────────────┐
│    User     │         │  Character  │
├─────────────┤         ├─────────────┤
│ id (PK)     │────┐    │ id (PK)     │
│ username    │    │    │ name        │
│ email       │    │    │ title       │
│ created_at  │    │    │ magic_power │
└─────────────┘    │    │ phys_power  │
     ▲             │    │ defense     │
     │             │    │ speed       │
     │         ┌───┴────┤ weapon      │
     │         │        │ image       │
     │         │        │ description │
     │    ┌────▼────┐   │ created_at  │
     │    │ Review  │   └─────────────┘
     │    ├─────────┤        ▲
     ├────│ id (PK) │        │
     │    │ char_id │────────┤
     │    │ user_id │        │
     │    │ title   │        │
     │    │ content │        │
     │    │ rating  │   ┌────┴────┐
     │    │ date    │   │ Rating   │
     │    └─────────┘   ├──────────┤
     │                  │ id (PK)  │
     ├─────────────────│ char_id  │
     │                 │ user_id  │
     │         ┌───────│ rating   │
     │         │       │ date     │
     │    ┌────▼───┐   └──────────┘
     │    │ Battle │
     │    ├────────┤    (Unique: char_id + user_id)
     └────│ id     │
          │ char1  │
          │ char2  │
          │ winner │
          │ strat1 │
          │ strat2 │
          │ prob1  │
          │ prob2  │
          └────────┘
```

### Tables Description

#### **Character**
- Primary storage for game characters
- Indexed on `name` for fast searches
- Calculated field: `overall_score = (magic + physical + defense + speed) / 4`

#### **User**
- Stores user account information
- One-to-many relationship with Reviews and Ratings
- Created via API endpoints

#### **Review**
- Links users with characters
- Foreign keys: character_id, user_id
- Supports text reviews with ratings

#### **Rating**
- Simplified rating system (1-5)
- Unique constraint: one rating per user per character
- Used for aggregation queries (AVG rating per character)

#### **Battle**
- Game Theory simulation results
- Links two characters
- Stores strategies and win probabilities
- Used for analytics on combat statistics

#### **CharacterStats**
- Denormalized cache table for performance
- Stores pre-calculated battle statistics
- Reduces need for complex aggregations on reads

---

## 📡 API Documentation

### Character Endpoints

#### **GET /api/characters**
```bash
# List all characters
curl http://localhost:5000/api/characters

# Search and sort
curl "http://localhost:5000/api/characters?q=Malenia&sort=magic"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Malenia",
    "title": "Blade of Miquella",
    "magic_power": 98,
    "physical_power": 95,
    "defense": 75,
    "speed": 90,
    "weapon": "Waterfowl Dance",
    "image": "https://...",
    "description": "...",
    "avg_rating": 4.8,
    "review_count": 3,
    "overall_score": 89.5,
    "created_at": "2024-01-15T10:30:00"
  }
]
```

#### **GET /api/characters/{id}**
Retrieve detailed information for a single character including reviews and battle stats.

#### **POST /api/characters**
```json
{
  "name": "New Character",
  "title": "The Mighty",
  "magic_power": 75,
  "physical_power": 80,
  "defense": 70,
  "speed": 85,
  "weapon": "Great Sword",
  "image": "https://...",
  "description": "A powerful warrior..."
}
```

#### **POST /api/characters/{id}**
Update an existing character (same JSON structure as POST).

#### **DELETE /api/characters/{id}**
Delete a character (cascades to related reviews, ratings, battles).

---

### Review Endpoints

#### **GET /api/reviews**
```bash
# Get all reviews
curl http://localhost:5000/api/reviews

# Filter by character
curl "http://localhost:5000/api/reviews?character_id=1"

# Filter by user
curl "http://localhost:5000/api/reviews?user_id=1"
```

#### **POST /api/reviews**
```json
{
  "character_id": 1,
  "user_id": 1,
  "title": "Great character",
  "content": "Detailed review text...",
  "rating": 5
}
```

#### **DELETE /api/reviews/{id}**
Remove a review.

---

### Rating Endpoints

#### **GET /api/ratings**
```bash
curl "http://localhost:5000/api/ratings?character_id=1"
```

#### **POST /api/ratings**
```json
{
  "character_id": 1,
  "user_id": 1,
  "rating": 4
}
```
(Automatically creates or updates existing rating)

---

### Game Theory - Battle Simulation

#### **POST /api/simulate-battle**
Simulate a battle using Game Theory payoff matrices.

```json
{
  "character1_id": 2,
  "character2_id": 1,
  "char1_strategy": "aggressive",
  "char2_strategy": "defensive",
  "rounds": 1
}
```

**Response:**
```json
{
  "battle": {
    "id": 1,
    "char1_name": "Radahn",
    "char2_name": "Malenia",
    "winner_name": "Malenia",
    "char1_win_probability": 40.0,
    "char2_win_probability": 60.0
  },
  "char1": {
    "name": "Radahn",
    "total_power": 253,
    "strategy": "aggressive",
    "win_probability": 40.0
  },
  "char2": {
    "name": "Malenia",
    "total_power": 273,
    "strategy": "defensive",
    "win_probability": 60.0
  },
  "winner": {
    "id": 1,
    "name": "Malenia"
  }
}
```

#### **GET /api/battles**
```bash
curl "http://localhost:5000/api/battles?page=1&per_page=10"
```

---

### Analytics Endpoints

#### **GET /api/analytics/top-characters**
```bash
# Top rated
curl "http://localhost:5000/api/analytics/top-characters?metric=rating&limit=10"

# Most reviewed
curl "http://localhost:5000/api/analytics/top-characters?metric=reviews&limit=10"

# Best battle record
curl "http://localhost:5000/api/analytics/top-characters?metric=battles&limit=10"
```

#### **GET /api/analytics/database-stats**
Get overall database statistics.

```json
{
  "total_characters": 12,
  "total_users": 3,
  "total_reviews": 21,
  "total_ratings": 36,
  "total_battles": 5,
  "avg_character_rating": 4.2,
  "most_rated_character": {
    "id": 1,
    "name": "Malenia",
    "rating_count": 5
  }
}
```

#### **GET /api/analytics/character-comparison**
```bash
curl "http://localhost:5000/api/analytics/character-comparison?ids=1&ids=2&ids=3"
```

Compares multiple characters across all metrics.

#### **GET /api/analytics/search**
```bash
# Advanced search with filters
curl "http://localhost:5000/api/analytics/search?q=Malenia&min_magic=80&max_magic=100&min_rating=4"
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Windows/macOS/Linux

### Step 1: Clone and Navigate
```bash
cd e:\elden_flask_project
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
pip list
```

Should show:
- Flask 3.1.3
- Flask-SQLAlchemy 3.1.1
- SQLAlchemy 2.0.49

---

## ▶️ Running the Application

### Start the Server
```bash
python app.py
```

Output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Access the Application
Open your browser to: **http://localhost:5000**

### Pages Available
- 🏠 **Home**: http://localhost:5000/
- ➕ **Add Character**: http://localhost:5000/add-character
- 📝 **Reviews**: http://localhost:5000/reviews
- ⚔️ **Battle Arena**: http://localhost:5000/game-theory
- 📊 **Analytics**: http://localhost:5000/analytics
- 👤 **Character Details**: http://localhost:5000/character/1

---

## 📚 Usage Examples

### Example 1: Search Characters
```javascript
// Frontend JavaScript
async function searchCharacters() {
  let response = await fetch("/api/characters?q=Malenia&sort=magic");
  let characters = await response.json();
  console.log(characters);
}
```

### Example 2: Simulate a Battle
```bash
curl -X POST http://localhost:5000/api/simulate-battle \
  -H "Content-Type: application/json" \
  -d '{
    "character1_id": 2,
    "character2_id": 1,
    "char1_strategy": "aggressive",
    "char2_strategy": "defensive"
  }'
```

### Example 3: Get Analytics
```bash
# Top characters by rating
curl http://localhost:5000/api/analytics/top-characters?metric=rating&limit=5

# Database statistics
curl http://localhost:5000/api/analytics/database-stats
```

### Example 4: Add a Review
```bash
curl -X POST http://localhost:5000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "character_id": 1,
    "user_id": 1,
    "title": "Excellent fighter",
    "content": "Malenia is incredibly powerful and fast.",
    "rating": 5
  }'
```

---

## 🎯 Advanced Features

### Game Theory Analysis

#### Payoff Matrix Implementation
The battle simulation uses a payoff matrix to determine optimal strategies:

```
                Opponent: Aggressive  Defensive  Balanced
Player: Aggressive      0.5             1.2       0.9
        Defensive       0.8             0.5       0.9
        Balanced        1.1             0.9       1.0
```

This creates a simple rock-paper-scissors-like scenario where:
- Aggressive beats Defensive (1.2 multiplier)
- Defensive beats Aggressive (0.8 multiplier)
- Balanced performs consistently (0.9-1.1)

#### Win Probability Calculation
```python
char1_score = (magic + physical + speed) / 300 * modifier1
char2_score = (magic + physical + speed) / 300 * modifier2
total = char1_score + char2_score
prob1 = char1_score / total
prob2 = char2_score / total
```

### Database Queries

#### JOIN Query Example
Get characters with their average ratings:
```python
results = db.session.query(
    Character,
    func.avg(Rating.rating).label('avg_rating')
).outerjoin(Rating, Character.id == Rating.character_id)\
 .group_by(Character.id)\
 .order_by(desc(func.avg(Rating.rating)))\
 .limit(10).all()
```

#### Aggregation Query Example
Get most reviewed characters:
```python
results = db.session.query(
    Character,
    func.count(Review.id).label('review_count')
).outerjoin(Review, Character.id == Review.character_id)\
 .group_by(Character.id)\
 .order_by(desc(func.count(Review.id)))\
 .limit(10).all()
```

#### Battle Statistics
Win rate calculation with complex JOIN:
```python
battles = db.session.query(
    Character,
    func.count(Battle.id).label('total_battles'),
    func.sum(func.case((Battle.winner_id == Character.id, 1))).label('wins')
).outerjoin(Battle, 
           or_(Battle.character1_id == Character.id, 
               Battle.character2_id == Character.id)
).group_by(Character.id)\
 .order_by(desc(func.sum(...)))\
 .all()
```

### Performance Optimization

1. **Database Indexing**
   - `Character.name` - indexed for fast search
   - `Character.id` - primary key index
   - `Review.character_id` - foreign key index
   - `Review.created_at` - range query optimization

2. **Query Optimization**
   - Use JOINs instead of N+1 queries
   - Limit results with pagination
   - Cache denormalized stats in CharacterStats table

3. **Caching Strategy**
   - Database statistics cached
   - Character stats denormalized for fast access

---

## 📁 Project Structure

```
elden_flask_project/
├── app.py                      # Main Flask application
├── models.py                   # SQLAlchemy ORM models
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── templates/
│   ├── index.html             # Home page with character list
│   ├── character_detail.html   # Character details & reviews
│   ├── add_character.html      # Add/Edit character form
│   ├── reviews.html            # Reviews & ratings system
│   ├── game_theory.html        # Battle simulation arena
│   └── analytics.html          # Analytics dashboard
│
├── static/
│   ├── style.css              # Comprehensive styling
│   ├── script.js              # Shared JavaScript utilities
│   └── images/                # Character images directory
│
├── instance/
│   └── elden.db               # SQLite database (auto-created)
│
└── db.py                      # Database utilities (placeholder)
```

---

## 🗄️ Database Schema SQL

```sql
-- Characters Table
CREATE TABLE character (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    title VARCHAR(100) NOT NULL,
    magic_power INTEGER DEFAULT 50,
    physical_power INTEGER DEFAULT 50,
    weapon VARCHAR(100),
    defense INTEGER DEFAULT 50,
    speed INTEGER DEFAULT 50,
    image VARCHAR(500),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_character_name ON character(name);

-- Users Table
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews Table
CREATE TABLE review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    rating INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (character_id) REFERENCES character(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
CREATE INDEX idx_review_character_id ON review(character_id);

-- Ratings Table
CREATE TABLE rating (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (character_id) REFERENCES character(id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    UNIQUE (character_id, user_id)
);
CREATE INDEX idx_rating_character_id ON rating(character_id);

-- Battles Table
CREATE TABLE battle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character1_id INTEGER NOT NULL,
    character2_id INTEGER NOT NULL,
    user_id INTEGER,
    winner_id INTEGER,
    char1_strategy VARCHAR(100),
    char2_strategy VARCHAR(100),
    char1_win_probability FLOAT,
    char2_win_probability FLOAT,
    simulation_rounds INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (character1_id) REFERENCES character(id),
    FOREIGN KEY (character2_id) REFERENCES character(id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (winner_id) REFERENCES character(id)
);
CREATE INDEX idx_battle_created_at ON battle(created_at);

-- Character Stats Table (Denormalized)
CREATE TABLE character_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER NOT NULL UNIQUE,
    total_battles INTEGER DEFAULT 0,
    total_wins INTEGER DEFAULT 0,
    win_rate FLOAT DEFAULT 0,
    avg_rating FLOAT DEFAULT 0,
    total_reviews INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (character_id) REFERENCES character(id)
);
```

---

## 🤔 Common Operations

### View All Characters
```
GET /api/characters
```

### Search for a Character
```
GET /api/characters?q=Malenia&sort=magic
```

### Get Top Rated Characters (JOIN Query)
```
GET /api/analytics/top-characters?metric=rating&limit=5
```

### Simulate a Battle (Game Theory)
```
POST /api/simulate-battle
{
  "character1_id": 2,
  "character2_id": 1,
  "char1_strategy": "aggressive",
  "char2_strategy": "defensive"
}
```

### Compare Characters
```
GET /api/analytics/character-comparison?ids=1&ids=2&ids=3
```

### Get Database Statistics
```
GET /api/analytics/database-stats
```

---

## 📊 Sample Data

The application comes with 12 pre-loaded characters:
1. Ranni - Witch of Moon
2. Malenia - Blade of Miquella
3. Radahn - Starscourge
4. Mohg - Lord of Blood
5. Blaidd - Half-Wolf Knight
6. Rykard - God Devouring Serpent
7. Fia - Deathbed Companion
8. Melina - Kindling Maiden
9. Godfrey - First Elden Lord
10. Marika - Eternal Queen
11. Miquella - Lord of Grace
12. Godrick - The Grafted

Plus demo users and sample reviews/ratings.

---

## 🐛 Troubleshooting

### Database Error
If you see SQLite errors:
```bash
# Delete old database
rm instance/elden.db

# Restart application - new database will be created
python app.py
```

### Port Already in Use
```bash
# Use different port
flask run --port 5001
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

## 📝 License

This project is educational material for demonstrating DBMS concepts.

---

## 🎓 Concepts Demonstrated

✅ **DBMS**
- Normalization (1NF, 2NF, 3NF)
- Foreign keys & referential integrity
- Transactions & ACID properties
- Indexing & query optimization
- JOIN operations
- GROUP BY & aggregations

✅ **Operating Systems**
- Process management in Flask
- File I/O operations
- Memory management
- Context switching (async operations)

✅ **Game Theory**
- Payoff matrices
- Nash equilibrium concepts
- Strategy optimization
- Probability calculations

✅ **Data Analysis**
- Statistical aggregations
- Comparative analysis
- Performance metrics
- Win rate calculations

---

**Happy exploring the Lands Between! ⚔️**
