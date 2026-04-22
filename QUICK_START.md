# Quick Start Guide

## 🚀 Get Up and Running in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
```
http://localhost:5000
```

---

## 📍 Navigation

| Page | URL | Purpose |
|------|-----|---------|
| Home | `/` | Browse all characters |
| Add Character | `/add-character` | Create new character |
| Character Details | `/character/{id}` | View full stats & reviews |
| Reviews | `/reviews` | Community reviews system |
| Battle Arena | `/game-theory` | Simulate battles using Game Theory |
| Analytics | `/analytics` | Database statistics & trends |

---

## 🔗 Key API Endpoints

### Characters
```bash
GET    /api/characters                    # List all
POST   /api/characters                    # Create
GET    /api/characters/{id}               # Get one
POST   /api/characters/{id}               # Update
DELETE /api/characters/{id}               # Delete
```

### Reviews
```bash
GET    /api/reviews                       # List all
POST   /api/reviews                       # Create
DELETE /api/reviews/{id}                  # Delete
```

### Ratings
```bash
GET    /api/ratings                       # List all
POST   /api/ratings                       # Create/Update
```

### Battle Simulation
```bash
POST   /api/simulate-battle               # Run simulation
GET    /api/battles                       # View history
```

### Analytics
```bash
GET    /api/analytics/database-stats      # Stats
GET    /api/analytics/top-characters      # Rankings
GET    /api/analytics/character-comparison # Compare
GET    /api/analytics/search              # Advanced search
```

---

## 💡 Example API Calls

### Search Characters
```bash
curl "http://localhost:5000/api/characters?q=Malenia&sort=magic"
```

### Get Database Stats
```bash
curl http://localhost:5000/api/analytics/database-stats
```

### Simulate Battle
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

### Add Review
```bash
curl -X POST http://localhost:5000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "character_id": 1,
    "user_id": 1,
    "title": "Excellent!",
    "content": "Amazing character",
    "rating": 5
  }'
```

---

## 📊 Default Demo Data

- **12 Characters**: Malenia, Radahn, Marika, etc.
- **3 Users**: player1, player2, analyst
- **Sample Reviews**: Pre-loaded reviews and ratings
- **Sample Battles**: 5 simulated battles

---

## 🎯 Features Overview

✅ **CRUD Operations** - Add, view, edit, delete characters  
✅ **Search & Filter** - Find characters by name, stats, rating  
✅ **Reviews & Ratings** - Community feedback system  
✅ **Game Theory** - Battle simulations with strategies  
✅ **Analytics** - Statistics and trend analysis  
✅ **Advanced Queries** - JOINs, aggregations, comparisons  
✅ **Responsive UI** - Works on desktop and mobile  

---

## 🔧 Troubleshooting

**Port 5000 already in use?**
```bash
flask run --port 5001
```

**Database error?**
```bash
# Delete database to reset
rm instance/elden.db

# Restart app
python app.py
```

**Module not found?**
```bash
pip install --upgrade -r requirements.txt
```

---

**Ready to explore? Open http://localhost:5000 🎮**
