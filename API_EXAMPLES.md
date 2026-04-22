# API Documentation with Examples

## Overview

This document provides comprehensive examples for using the Elden Ring DBMS REST API.

---

## 🔤 BASE URL

```
http://localhost:5000
```

All examples use curl. Replace `localhost:5000` with your server URL for production.

---

## 📚 CHARACTER MANAGEMENT

### 1. Get All Characters

**Request:**
```bash
curl http://localhost:5000/api/characters
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Ranni",
    "title": "Witch of Moon",
    "magic_power": 95,
    "physical_power": 60,
    "weapon": "Dark Moon",
    "defense": 70,
    "speed": 85,
    "image": "https://...",
    "description": "The Witch of the Moon...",
    "avg_rating": 4.5,
    "review_count": 2,
    "overall_score": 77.5,
    "created_at": "2024-01-15T10:30:00"
  }
]
```

---

### 2. Search Characters

**Request:**
```bash
# Search by name
curl "http://localhost:5000/api/characters?q=Malenia"

# Search and sort by magic power
curl "http://localhost:5000/api/characters?q=Malenia&sort=magic"

# Sort by overall score
curl "http://localhost:5000/api/characters?sort=overall"
```

**Query Parameters:**
- `q`: Search query (name search)
- `sort`: Sort by 'name', 'magic', 'physical', or 'overall'

---

### 3. Get Single Character Details

**Request:**
```bash
curl http://localhost:5000/api/characters/1
```

**Response:**
```json
{
  "id": 1,
  "name": "Ranni",
  "title": "Witch of Moon",
  "magic_power": 95,
  "physical_power": 60,
  "weapon": "Dark Moon",
  "defense": 70,
  "speed": 85,
  "image": "https://...",
  "description": "The Witch of the Moon...",
  "avg_rating": 4.5,
  "review_count": 2,
  "overall_score": 77.5,
  "created_at": "2024-01-15T10:30:00",
  "reviews": [
    {
      "id": 1,
      "title": "Great character",
      "content": "Very powerful...",
      "rating": 5,
      "username": "player1",
      "created_at": "2024-01-15T11:00:00"
    }
  ],
  "ratings": [
    {
      "id": 1,
      "user_id": 1,
      "rating": 5
    }
  ],
  "total_battles": 3,
  "total_wins": 2,
  "win_rate": 66.67
}
```

---

### 4. Create New Character

**Request:**
```bash
curl -X POST http://localhost:5000/api/characters \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Character",
    "title": "The Legendary",
    "magic_power": 85,
    "physical_power": 90,
    "defense": 80,
    "speed": 75,
    "weapon": "Legendary Sword",
    "image": "https://example.com/image.jpg",
    "description": "A powerful warrior from the Lands Between"
  }'
```

**Response:**
```json
{
  "msg": "Character created successfully",
  "character": {
    "id": 13,
    "name": "New Character",
    "title": "The Legendary",
    ...
  }
}
```

---

### 5. Update Character

**Request:**
```bash
curl -X POST http://localhost:5000/api/characters/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ranni",
    "title": "Witch of Moon",
    "magic_power": 100,
    "physical_power": 65,
    "defense": 75,
    "speed": 90,
    "weapon": "Dark Moon",
    "image": "https://...",
    "description": "Updated description"
  }'
```

---

### 6. Delete Character

**Request:**
```bash
curl -X DELETE http://localhost:5000/api/characters/1
```

**Response:**
```json
{
  "msg": "Character deleted successfully"
}
```

---

## 📝 REVIEWS SYSTEM

### 1. Get All Reviews

**Request:**
```bash
# Get all reviews
curl http://localhost:5000/api/reviews

# Get reviews for specific character
curl "http://localhost:5000/api/reviews?character_id=1"

# Get reviews by specific user
curl "http://localhost:5000/api/reviews?user_id=1"
```

---

### 2. Create Review

**Request:**
```bash
curl -X POST http://localhost:5000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "character_id": 1,
    "user_id": 1,
    "title": "Amazing warrior",
    "content": "Ranni is incredibly powerful with excellent magic abilities. Her defensive capabilities are also impressive. Highly recommended for advanced players.",
    "rating": 5
  }'
```

**Validation:**
- `character_id`: Required, must exist
- `user_id`: Required, must exist
- `title`: Required, max 200 characters
- `content`: Required, text body
- `rating`: Required, 1-5 integer

**Response:**
```json
{
  "msg": "Review created successfully",
  "review": {
    "id": 21,
    "character_id": 1,
    "user_id": 1,
    "username": "player1",
    "title": "Amazing warrior",
    "content": "...",
    "rating": 5,
    "created_at": "2024-01-15T12:00:00",
    "updated_at": "2024-01-15T12:00:00"
  }
}
```

---

### 3. Delete Review

**Request:**
```bash
curl -X DELETE http://localhost:5000/api/reviews/21
```

---

## ⭐ RATINGS SYSTEM

### 1. Get All Ratings

**Request:**
```bash
# All ratings
curl http://localhost:5000/api/ratings

# Ratings for character
curl "http://localhost:5000/api/ratings?character_id=1"
```

---

### 2. Create or Update Rating

**Request:**
```bash
curl -X POST http://localhost:5000/api/ratings \
  -H "Content-Type: application/json" \
  -d '{
    "character_id": 1,
    "user_id": 1,
    "rating": 5
  }'
```

**Note:** If a rating already exists for this user-character pair, it will be updated.

**Response:**
```json
{
  "msg": "Rating saved successfully",
  "rating": {
    "id": 1,
    "character_id": 1,
    "user_id": 1,
    "rating": 5,
    "created_at": "2024-01-15T12:00:00"
  }
}
```

---

## ⚔️ GAME THEORY - BATTLE SIMULATION

### 1. Simulate Battle

**Request:**
```bash
curl -X POST http://localhost:5000/api/simulate-battle \
  -H "Content-Type: application/json" \
  -d '{
    "character1_id": 2,
    "character2_id": 1,
    "char1_strategy": "aggressive",
    "char2_strategy": "defensive",
    "rounds": 1
  }'
```

**Strategy Options:**
- `aggressive` - High risk, high reward
- `defensive` - Lower risk, steady approach
- `balanced` - Moderate approach

**Response:**
```json
{
  "battle": {
    "id": 5,
    "character1_id": 2,
    "character2_id": 1,
    "char1_name": "Malenia",
    "char2_name": "Ranni",
    "winner_id": 2,
    "winner_name": "Malenia",
    "char1_strategy": "aggressive",
    "char2_strategy": "defensive",
    "char1_win_probability": 60.0,
    "char2_win_probability": 40.0,
    "simulation_rounds": 1,
    "created_at": "2024-01-15T12:00:00"
  },
  "char1": {
    "name": "Malenia",
    "total_power": 273,
    "strategy": "aggressive",
    "win_probability": 60.0
  },
  "char2": {
    "name": "Ranni",
    "total_power": 215,
    "strategy": "defensive",
    "win_probability": 40.0
  },
  "winner": {
    "id": 2,
    "name": "Malenia"
  }
}
```

---

### 2. Get Battle History

**Request:**
```bash
# Page 1, 10 results per page
curl "http://localhost:5000/api/battles?page=1&per_page=10"

# Get specific page
curl "http://localhost:5000/api/battles?page=2&per_page=20"
```

**Response:**
```json
{
  "battles": [
    {
      "id": 5,
      "char1_name": "Malenia",
      "char2_name": "Ranni",
      "winner_name": "Malenia",
      "char1_win_probability": 60.0,
      "char2_win_probability": 40.0,
      "created_at": "2024-01-15T12:00:00"
    }
  ],
  "total": 5,
  "pages": 1,
  "current_page": 1
}
```

---

## 📊 ANALYTICS & AGGREGATIONS

### 1. Get Database Statistics

**Request:**
```bash
curl http://localhost:5000/api/analytics/database-stats
```

**Response:**
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
  },
  "most_reviewed_character": {
    "id": 2,
    "name": "Ranni",
    "review_count": 4
  },
  "most_battled_character": {
    "id": 1,
    "name": "Malenia",
    "battle_count": 3
  }
}
```

---

### 2. Get Top Characters

**Request:**
```bash
# Top rated characters
curl "http://localhost:5000/api/analytics/top-characters?metric=rating&limit=10"

# Most reviewed
curl "http://localhost:5000/api/analytics/top-characters?metric=reviews&limit=10"

# Best battle record
curl "http://localhost:5000/api/analytics/top-characters?metric=battles&limit=10"

# Most powerful (power ranking)
curl "http://localhost:5000/api/analytics/top-characters?metric=power&limit=10"
```

**Metrics:**
- `rating` - Sorted by average rating
- `reviews` - Sorted by review count
- `battles` - Sorted by win rate / battle success
- `power` - Sorted by combined power stats

**Response (Example for rating metric):**
```json
[
  {
    "character": {
      "id": 2,
      "name": "Malenia",
      "title": "Blade of Miquella",
      "magic_power": 98,
      ...
    },
    "rating_count": 5,
    "avg_rating": 4.8
  },
  {
    "character": {
      "id": 1,
      "name": "Ranni",
      ...
    },
    "rating_count": 4,
    "avg_rating": 4.5
  }
]
```

---

### 3. Compare Multiple Characters

**Request:**
```bash
# Compare characters with IDs 1, 2, and 3
curl "http://localhost:5000/api/analytics/character-comparison?ids=1&ids=2&ids=3"
```

**Response:**
```json
[
  {
    "character": {
      "id": 1,
      "name": "Ranni",
      ...
    },
    "avg_rating": 4.5,
    "review_count": 4,
    "total_battles": 2,
    "total_wins": 1,
    "win_rate": 50.0,
    "power_score": 77.5
  },
  {
    "character": {
      "id": 2,
      "name": "Malenia",
      ...
    },
    "avg_rating": 4.8,
    "review_count": 5,
    "total_battles": 3,
    "total_wins": 2,
    "win_rate": 66.67,
    "power_score": 89.5
  }
]
```

---

### 4. Advanced Search

**Request:**
```bash
# Search with multiple filters
curl "http://localhost:5000/api/analytics/search?q=Malenia&min_magic=80&max_magic=100&min_rating=4"

# Search only
curl "http://localhost:5000/api/analytics/search?q=warrior"

# Magic power range
curl "http://localhost:5000/api/analytics/search?min_magic=90&max_magic=100"

# Minimum rating
curl "http://localhost:5000/api/analytics/search?min_rating=4.5"
```

**Parameters:**
- `q`: Search query (searches name, title, weapon)
- `min_magic`: Minimum magic power (0-100)
- `max_magic`: Maximum magic power (0-100)
- `min_rating`: Minimum average rating (0-5)

**Response:**
```json
[
  {
    "id": 2,
    "name": "Malenia",
    "title": "Blade of Miquella",
    "magic_power": 98,
    "physical_power": 95,
    "defense": 75,
    "speed": 90,
    "weapon": "Waterfowl Dance",
    "avg_rating": 4.8,
    "review_count": 5,
    "overall_score": 89.5
  }
]
```

---

## 👥 USER MANAGEMENT

### 1. Get All Users

**Request:**
```bash
curl http://localhost:5000/api/users
```

**Response:**
```json
[
  {
    "id": 1,
    "username": "player1",
    "email": "player1@elden.com",
    "created_at": "2024-01-15T10:00:00"
  },
  {
    "id": 2,
    "username": "player2",
    "email": "player2@elden.com",
    "created_at": "2024-01-15T10:00:00"
  }
]
```

---

### 2. Create User

**Request:**
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newplayer",
    "email": "newplayer@elden.com"
  }'
```

**Response:**
```json
{
  "msg": "User created successfully",
  "user": {
    "id": 4,
    "username": "newplayer",
    "email": "newplayer@elden.com",
    "created_at": "2024-01-15T12:00:00"
  }
}
```

---

## 🔍 FILTERING & PAGINATION

### Common Query Parameters

```bash
# Pagination
?page=1&per_page=20

# Search
?q=search_term

# Sort
?sort=name
?sort=magic
?sort=overall

# Limit results
?limit=10

# Filter by metrics
?metric=rating
?metric=reviews
?metric=battles
```

---

## 📋 ERROR RESPONSES

### 400 Bad Request
```json
{
  "error": "Name and title required"
}
```

### 404 Not Found
```json
{
  "error": "Character not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Database error occurred"
}
```

---

## 🧪 Testing Example Workflow

```bash
#!/bin/bash

# 1. Get all characters
echo "Getting all characters..."
curl http://localhost:5000/api/characters

# 2. Create a new character
echo -e "\nCreating new character..."
curl -X POST http://localhost:5000/api/characters \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","title":"Hero","magic_power":75,"physical_power":80,"defense":70,"speed":85,"weapon":"Sword","image":"https://example.com/img.jpg","description":"Test character"}'

# 3. Simulate battle
echo -e "\nSimulating battle..."
curl -X POST http://localhost:5000/api/simulate-battle \
  -H "Content-Type: application/json" \
  -d '{"character1_id":1,"character2_id":2,"char1_strategy":"aggressive","char2_strategy":"defensive"}'

# 4. Get analytics
echo -e "\nGetting database stats..."
curl http://localhost:5000/api/analytics/database-stats

# 5. Get top characters
echo -e "\nGetting top rated characters..."
curl "http://localhost:5000/api/analytics/top-characters?metric=rating&limit=5"
```

---

## 💾 Quick Reference

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List Characters | GET | `/api/characters` |
| Get Character | GET | `/api/characters/{id}` |
| Create Character | POST | `/api/characters` |
| Update Character | POST | `/api/characters/{id}` |
| Delete Character | DELETE | `/api/characters/{id}` |
| List Reviews | GET | `/api/reviews` |
| Create Review | POST | `/api/reviews` |
| Delete Review | DELETE | `/api/reviews/{id}` |
| List Ratings | GET | `/api/ratings` |
| Rate Character | POST | `/api/ratings` |
| Simulate Battle | POST | `/api/simulate-battle` |
| Battle History | GET | `/api/battles` |
| DB Stats | GET | `/api/analytics/database-stats` |
| Top Characters | GET | `/api/analytics/top-characters` |
| Compare Characters | GET | `/api/analytics/character-comparison` |
| Advanced Search | GET | `/api/analytics/search` |
| List Users | GET | `/api/users` |
| Create User | POST | `/api/users` |

---

**Need help? Check the README.md for more details! ⚔️**
