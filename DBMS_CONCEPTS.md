# 🗄️ DBMS Concepts Explained - Elden Ring DBMS Project

This document explains the advanced database management system (DBMS) concepts implemented in this project.

---

## 📚 Table of Contents

1. [Database Normalization](#database-normalization)
2. [Relational Model](#relational-model)
3. [ACID Properties](#acid-properties)
4. [Indexes & Performance](#indexes--performance)
5. [JOIN Operations](#join-operations)
6. [Aggregations & GROUP BY](#aggregations--group-by)
7. [Constraints & Integrity](#constraints--integrity)
8. [Query Optimization](#query-optimization)

---

## 🔄 Database Normalization

### What is Normalization?
Normalization is the process of organizing database tables to reduce redundancy and improve data integrity.

### Normal Forms (1NF → 3NF)

#### **First Normal Form (1NF)**
Requirement: All attributes contain only atomic (indivisible) values.

**Before (NOT 1NF):**
```
CHARACTER table:
| id | name     | stats (INVALID - not atomic)   |
|----|----------|--------------------------------|
| 1  | Malenia  | [Magic: 98, Power: 95, ...]   |
```

**After (1NF):**
```
CHARACTER table:
| id | name     | magic_power | physical_power | defense |
|----|----------|-------------|----------------|---------|
| 1  | Malenia  | 98          | 95             | 75      |
```

✅ **Implementation in Project**: Each `character` field is atomic (single value)

---

#### **Second Normal Form (2NF)**
Requirements: 
- Must be in 1NF
- No partial dependencies (non-key attributes depend on entire primary key)

**Example in Project:**
```
REVIEW table:
| id | character_id | user_id | title | content |
```

Every non-key attribute (title, content) depends on the entire composite key if it were composite.

✅ **Implementation**: Review attributes depend on the full primary key (id)

---

#### **Third Normal Form (3NF)**
Requirements:
- Must be in 2NF
- No transitive dependencies (non-key attributes don't depend on other non-key attributes)

**Bad Example (Transitive Dependency):**
```
BOOK table:
| id | title | author_id | author_name |  ❌ author_name depends on author_id
```

**Good Example (3NF):**
```
BOOK table:          AUTHOR table:
| id | title |       | id | name |
| 1  | Lord  |       | 1  | Tolkien |
```

✅ **Implementation in Project**: No transitive dependencies
- Character doesn't store computed fields
- Stats are directly measured, not derived from other stats

---

## 📊 Relational Model

### Tables in This Project

#### 1. **CHARACTER Table** (Core Entity)
```sql
CREATE TABLE character (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    title VARCHAR(100) NOT NULL,
    magic_power INTEGER DEFAULT 50,
    physical_power INTEGER DEFAULT 50,
    defense INTEGER DEFAULT 50,
    speed INTEGER DEFAULT 50,
    weapon VARCHAR(100),
    image VARCHAR(500),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Key Concepts:**
- `PRIMARY KEY (id)`: Uniquely identifies each character
- `UNIQUE (name)`: No duplicate character names
- `NOT NULL`: Required fields
- `DEFAULT`: Auto-populated values

#### 2. **USER Table** (Entity)
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. **REVIEW Table** (Weak Entity)
```sql
CREATE TABLE review (
    id INTEGER PRIMARY KEY,
    character_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    rating INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (character_id) REFERENCES character(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

**Key Concepts:**
- `FOREIGN KEY`: Links to parent tables
- Composite relationship (depends on both character and user)
- Weak entity (cannot exist without parent)

#### 4. **RATING Table** (Junction Entity)
```sql
CREATE TABLE rating (
    id INTEGER PRIMARY KEY,
    character_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (character_id, user_id),
    FOREIGN KEY (character_id) REFERENCES character(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

**Key Concepts:**
- `UNIQUE (character_id, user_id)`: Composite unique constraint
- Enforces one rating per user per character
- Prevents duplicate ratings

#### 5. **BATTLE Table** (Association Entity)
```sql
CREATE TABLE battle (
    id INTEGER PRIMARY KEY,
    character1_id INTEGER NOT NULL,
    character2_id INTEGER NOT NULL,
    winner_id INTEGER NOT NULL,
    char1_strategy VARCHAR(100),
    char2_strategy VARCHAR(100),
    char1_win_probability FLOAT,
    char2_win_probability FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (character1_id) REFERENCES character(id),
    FOREIGN KEY (character2_id) REFERENCES character(id),
    FOREIGN KEY (winner_id) REFERENCES character(id)
);
```

**Key Concepts:**
- Multiple foreign keys to same table (many-to-many via junction)
- Self-referential relationship (character fights another character)

---

### Entity-Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                   RELATIONAL SCHEMA                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐                 ┌──────────────┐              │
│  │ CHARACTER    │                 │ USER         │              │
│  ├──────────────┤                 ├──────────────┤              │
│  │ id (PK)      │◄────┐      ┌───►│ id (PK)      │              │
│  │ name (UQ)    │     │      │    │ username (UQ)│              │
│  │ title        │     │  ┌───┴────│ email (UQ)   │              │
│  │ magic_power  │     │  │    │   │ created_at   │              │
│  │ ...stats...  │     │  │    │   └──────────────┘              │
│  │ created_at   │     │  │    │                                 │
│  └──────────────┘     │  │    └──────┐                          │
│          ▲            │  │           │                          │
│          │            │  │       ┌───┴────────┐                │
│          │            │  │       │  REVIEW    │                │
│          │            │  │       ├────────────┤                │
│          │            └──┼──────►│ id (PK)    │                │
│          │               │   ┌──►│ char_id(FK)│                │
│          │               │   │  │ user_id(FK)│                │
│          │               │   │  │ title      │                │
│          │               │   │  │ content    │                │
│    ┌─────┴──────┐        │   │  │ rating     │                │
│    │  RATING    │        │   │  └────────────┘                │
│    ├────────────┤        │   │                                │
│    │ id (PK)    │        │   └─────────┐                      │
│    │ char_id(FK)├────────┘             │                      │
│    │ user_id(FK)├────────┐             │                      │
│    │ rating     │        │             │                      │
│    └────────────┘        │             │                      │
│                          │             │                      │
│          ┌────────────────┴─────────────┘                      │
│          │                                                      │
│    ┌─────┴──────────────────────────────────────┐             │
│    │         BATTLE                             │             │
│    ├──────────────────────────────────────────┤             │
│    │ id (PK)                                   │             │
│    │ character1_id (FK) ──────┐                │             │
│    │ character2_id (FK) ───┐  │                │             │
│    │ winner_id (FK) ───────┼──┤                │             │
│    │ char1_strategy         │  │                │             │
│    │ char2_strategy         │  │                │             │
│    │ char1_win_probability  │  │                │             │
│    │ char2_win_probability  │  │                │             │
│    └──────────────────────────┘                │             │
│                                                  │             │
└──────────────────────────────────────────────────┘             │
```

---

## ⚙️ ACID Properties

ACID properties ensure reliable database transactions:

### **A - Atomicity**
Transaction is all-or-nothing.

**Example in Project:**
```python
# Create review and update rating atomically
db.session.add(review)
db.session.add(rating)
db.session.commit()  # All or nothing

# If error occurs before commit, rollback
db.session.rollback()
```

### **C - Consistency**
Database moves from valid state to valid state.

**Example in Project:**
- Foreign key constraints ensure character_id exists
- Unique constraints prevent duplicate ratings
- Default values maintain state validity

### **I - Isolation**
Concurrent transactions don't interfere.

**Example in Project:**
- SQLite handles basic isolation
- Multiple users can rate simultaneously
- Each transaction is independent

### **D - Durability**
Committed data survives failures.

**Example in Project:**
- SQLite writes to disk immediately
- Battle results permanently stored
- No data loss after commit

---

## 🚀 Indexes & Performance

### What are Indexes?
Data structures that speed up data retrieval by maintaining sorted lookup tables.

### Indexes in This Project

#### **Primary Key Index** (Automatic)
```sql
CREATE TABLE character (
    id INTEGER PRIMARY KEY AUTOINCREMENT  -- Automatically indexed
);
```

**Use**: Fast lookup by ID
```python
character = Character.query.get(1)  -- O(log n) instead of O(n)
```

#### **Unique Index** (Automatic on UNIQUE constraint)
```sql
CREATE TABLE character (
    name VARCHAR(100) NOT NULL UNIQUE  -- Indexed
);
```

**Use**: Prevent duplicates efficiently
```python
if Character.query.filter_by(name="Malenia").first():
    # Filtered quickly using index
```

#### **Search Index**
```sql
CREATE INDEX idx_character_name ON character(name);
```

**Use**: Fast text search
```python
query = Character.query.filter(Character.name.contains(q))
-- Uses index for fast search
```

#### **Foreign Key Indexes**
```sql
CREATE INDEX idx_review_character_id ON review(character_id);
CREATE INDEX idx_rating_character_id ON rating(character_id);
```

**Use**: Fast JOINs
```python
# Fast because character_id is indexed
reviews = Review.query.filter_by(character_id=1).all()
```

#### **Range Query Index**
```sql
CREATE INDEX idx_battle_created_at ON battle(created_at);
```

**Use**: Fast sorting by date
```python
# Fast because created_at is indexed
recent_battles = Battle.query.order_by(Battle.created_at.desc()).limit(10)
```

### Index Trade-offs
| Advantage | Disadvantage |
|-----------|-------------|
| Faster SELECT | Slower INSERT/UPDATE/DELETE |
| Faster JOIN | Uses disk space |
| Faster WHERE | Maintenance overhead |

---

## 🔗 JOIN Operations

JOINs combine data from multiple tables.

### **INNER JOIN** (Only matches)
```sql
SELECT c.*, r.rating
FROM character c
INNER JOIN rating r ON c.id = r.character_id
-- Returns only characters that have ratings
```

**Code Example:**
```python
results = db.session.query(
    Character, Rating.rating
).join(Rating, Character.id == Rating.character_id).all()
```

### **LEFT JOIN** (All from left, matching from right)
```sql
SELECT c.*, r.rating
FROM character c
LEFT JOIN rating r ON c.id = r.character_id
-- Returns ALL characters, NULL if no rating
```

**Code Example:**
```python
results = db.session.query(
    Character, Rating.rating
).outerjoin(Rating).all()
```

### **Complex Multi-Table JOIN**
```sql
SELECT c.name, COUNT(rev.id) as review_count, AVG(r.rating) as avg_rating
FROM character c
LEFT JOIN review rev ON c.id = rev.character_id
LEFT JOIN rating r ON c.id = r.character_id
GROUP BY c.id
```

**Code Example:**
```python
results = db.session.query(
    Character.name,
    func.count(Review.id).label('review_count'),
    func.avg(Rating.rating).label('avg_rating')
).outerjoin(Review).outerjoin(Rating)\
 .group_by(Character.id).all()
```

### **Self-Join** (Join table to itself)
```sql
SELECT b1.character1_id, b2.character2_id
FROM battle b1
INNER JOIN battle b2 ON b1.character1_id = b2.character2_id
-- Find characters that fought each other
```

---

## 📊 Aggregations & GROUP BY

### **Aggregation Functions**

#### **COUNT()** - Count rows
```sql
SELECT COUNT(*) FROM character;
-- Returns: 12 (total characters)
```

#### **AVG()** - Average value
```sql
SELECT AVG(magic_power) FROM character;
-- Returns: 85.5 (average magic power)
```

#### **SUM()** - Total value
```sql
SELECT SUM(total_wins) FROM character_stats;
-- Returns: 15 (total wins across all)
```

#### **MIN/MAX()** - Extreme values
```sql
SELECT MIN(magic_power), MAX(magic_power) FROM character;
-- Returns: 50, 99 (range)
```

### **GROUP BY** - Group results

#### **Simple GROUP BY**
```sql
SELECT character_id, COUNT(*) as review_count
FROM review
GROUP BY character_id
ORDER BY review_count DESC
-- Lists each character with review count
```

**Code Example:**
```python
results = db.session.query(
    Review.character_id,
    func.count(Review.id).label('review_count')
).group_by(Review.character_id)\
 .order_by(desc('review_count')).all()
```

#### **GROUP BY with Multiple Columns**
```sql
SELECT character_id, user_id, COUNT(*) as interactions
FROM (
    SELECT character_id, user_id FROM review
    UNION ALL
    SELECT character_id, user_id FROM rating
) combined
GROUP BY character_id, user_id
-- Count user interactions per character
```

#### **GROUP BY with HAVING** - Filter grouped data
```sql
SELECT character_id, AVG(rating) as avg_rating
FROM rating
GROUP BY character_id
HAVING AVG(rating) >= 4.0
-- Only characters rated 4.0 or higher
```

---

## 🔐 Constraints & Integrity

### **Primary Key Constraint**
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
-- Uniquely identifies row
-- Automatically indexed
-- Cannot be NULL
```

### **Unique Constraint**
```sql
name VARCHAR(100) UNIQUE
-- No duplicate values
-- Can have multiple unique constraints
```

### **Foreign Key Constraint**
```sql
character_id INTEGER NOT NULL,
FOREIGN KEY (character_id) REFERENCES character(id)
-- Ensures character_id exists in character table
-- Prevents orphaned records
-- Enables CASCADE delete
```

**Code Example:**
```python
class Review(db.Model):
    character_id = db.Column(
        db.Integer, 
        db.ForeignKey('character.id'),  # Foreign key definition
        nullable=False
    )
```

### **Composite Unique Constraint**
```sql
UNIQUE (character_id, user_id)
-- One rating per (character, user) pair
```

**Code Example:**
```python
__table_args__ = (
    db.UniqueConstraint('character_id', 'user_id', 
                       name='unique_user_character_rating'),
)
```

### **NOT NULL Constraint**
```sql
name VARCHAR(100) NOT NULL
-- Field must have value
```

### **DEFAULT Constraint**
```sql
magic_power INTEGER DEFAULT 50
-- Auto-fills if not provided
```

---

## ⚡ Query Optimization

### **Query Analysis**

#### **Before Optimization** (N+1 Problem)
```python
characters = Character.query.all()
for char in characters:
    # This runs N separate queries!
    avg_rating = db.session.query(func.avg(Rating.rating))\
        .filter(Rating.character_id == char.id).scalar()
```

**Problem**: 1 + N queries (slow!)

#### **After Optimization** (Single JOIN)
```python
results = db.session.query(
    Character,
    func.avg(Rating.rating).label('avg_rating')
).outerjoin(Rating)\
 .group_by(Character.id).all()
```

**Solution**: 1 query (fast!)

### **Index Usage Tips**

1. **Always index Foreign Keys**
   ```sql
   CREATE INDEX idx_review_char_id ON review(character_id);
   ```

2. **Index Frequently Searched Columns**
   ```sql
   CREATE INDEX idx_char_name ON character(name);
   ```

3. **Consider Composite Indexes for Multi-column Filters**
   ```sql
   CREATE INDEX idx_char_stats ON character(magic_power, defense);
   ```

4. **Avoid Over-Indexing** (slows writes)
   ```sql
   -- Too many indexes = slow INSERT/UPDATE
   -- Balance read vs write performance
   ```

### **Query Writing Best Practices**

1. **Use JOINs instead of multiple queries**
2. **Filter early with WHERE clause**
3. **Use LIMIT for large result sets**
4. **Avoid SELECT * (specify columns)**
5. **Use aggregations in database, not code**

---

## 🎯 Advanced Topics

### **Denormalization for Performance**

The `CharacterStats` table is denormalized:

```python
class CharacterStats(db.Model):
    character_id = db.Column(db.Integer, unique=True)
    total_battles = db.Column(db.Integer, default=0)
    total_wins = db.Column(db.Integer, default=0)
    win_rate = db.Column(db.Float, default=0)
    avg_rating = db.Column(db.Float, default=0)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
```

**Purpose**: Cache frequently-accessed calculations
- Avoids complex aggregations on reads
- Trade-off: Need to update cache when data changes
- Worth it for frequently-read stats

### **Views (Stored Queries)**

Although SQLite doesn't support traditional views, you can simulate them:

```python
def get_top_characters_view(limit=10):
    """Virtual view: Top characters by rating"""
    return db.session.query(
        Character,
        func.avg(Rating.rating).label('avg_rating')
    ).outerjoin(Rating)\
     .group_by(Character.id)\
     .order_by(desc('avg_rating'))\
     .limit(limit).all()
```

---

## 📈 Scalability Considerations

### **Current Design** (SQLite)
- ✅ Good for: Learning, prototyping, <1000 concurrent users
- ❌ Not for: High concurrency, large datasets

### **For Production** (PostgreSQL/MySQL)
```python
# Change connection string
SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/elden'
# OR
SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/elden'
```

### **Performance Improvements**
1. Add connection pooling
2. Implement query caching
3. Use read replicas
4. Implement sharding for large tables
5. Archive old records

---

## 🏆 Summary

This project demonstrates:

✅ **Normalization**: 3NF schema design  
✅ **Relationships**: Foreign keys & constraints  
✅ **Performance**: Indexing strategy  
✅ **Queries**: JOINs & aggregations  
✅ **Integrity**: ACID compliance  
✅ **Optimization**: Query efficiency  

**Total concepts covered**: 30+

---

**Ready to master database design? 🗄️**
