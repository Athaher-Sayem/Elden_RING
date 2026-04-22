"""
Database utilities and helper functions for the Elden Ring DBMS system.
"""

from models import db, Character, User, Review, Rating, Battle, CharacterStats
from sqlalchemy import func, desc, and_, or_
from datetime import datetime, timedelta


class DatabaseManager:
    """Utility class for advanced database operations"""
    
    @staticmethod
    def get_top_characters(metric='rating', limit=10):
        """
        Get top characters by various metrics.
        
        Args:
            metric: 'rating', 'reviews', 'battles', or 'power'
            limit: Number of results
            
        Returns:
            List of (Character, metric_value) tuples
        """
        if metric == 'rating':
            return db.session.query(
                Character,
                func.avg(Rating.rating).label('metric')
            ).outerjoin(Rating).group_by(Character.id)\
             .order_by(desc('metric')).limit(limit).all()
        
        elif metric == 'reviews':
            return db.session.query(
                Character,
                func.count(Review.id).label('metric')
            ).outerjoin(Review).group_by(Character.id)\
             .order_by(desc('metric')).limit(limit).all()
        
        elif metric == 'battles':
            return db.session.query(
                Character,
                func.count(Battle.id).label('metric')
            ).outerjoin(Battle, or_(
                Battle.character1_id == Character.id,
                Battle.character2_id == Character.id
            )).group_by(Character.id)\
             .order_by(desc('metric')).limit(limit).all()
        
        elif metric == 'power':
            return Character.query.order_by(
                desc(Character.magic_power + Character.physical_power)
            ).limit(limit).all()
        
        return []
    
    @staticmethod
    def get_character_battle_stats(char_id):
        """Get battle statistics for a character"""
        character = Character.query.get(char_id)
        if not character:
            return None
        
        battles = Battle.query.filter(or_(
            Battle.character1_id == char_id,
            Battle.character2_id == char_id
        )).all()
        
        wins = sum(1 for b in battles if b.winner_id == char_id)
        total_battles = len(battles)
        win_rate = (wins / total_battles * 100) if total_battles > 0 else 0
        
        return {
            'character_id': char_id,
            'total_battles': total_battles,
            'total_wins': wins,
            'win_rate': round(win_rate, 2),
            'character_name': character.name
        }
    
    @staticmethod
    def get_character_rating_stats(char_id):
        """Get rating statistics for a character"""
        character = Character.query.get(char_id)
        if not character:
            return None
        
        avg_rating = db.session.query(func.avg(Rating.rating))\
            .filter(Rating.character_id == char_id).scalar() or 0
        
        review_count = Review.query.filter_by(character_id=char_id).count()
        rating_count = Rating.query.filter_by(character_id=char_id).count()
        
        return {
            'character_id': char_id,
            'avg_rating': round(float(avg_rating), 2),
            'review_count': review_count,
            'rating_count': rating_count,
            'character_name': character.name
        }
    
    @staticmethod
    def compare_characters(char_ids):
        """Compare multiple characters across all metrics"""
        comparison = []
        
        for char_id in char_ids:
            character = Character.query.get(char_id)
            if not character:
                continue
            
            battle_stats = DatabaseManager.get_character_battle_stats(char_id)
            rating_stats = DatabaseManager.get_character_rating_stats(char_id)
            
            comparison.append({
                'character': character.to_dict(),
                'battle_stats': battle_stats,
                'rating_stats': rating_stats,
                'overall_score': character._calculate_overall_score()
            })
        
        return comparison
    
    @staticmethod
    def get_database_summary():
        """Get comprehensive database summary"""
        return {
            'total_characters': Character.query.count(),
            'total_users': User.query.count(),
            'total_reviews': Review.query.count(),
            'total_ratings': Rating.query.count(),
            'total_battles': Battle.query.count(),
            'avg_rating': round(float(
                db.session.query(func.avg(Rating.rating)).scalar() or 0
            ), 2),
            'database_created': datetime.now().isoformat(),
        }
    
    @staticmethod
    def search_characters_advanced(query, min_magic=0, max_magic=100, min_rating=0):
        """Advanced character search with multiple filters"""
        characters = Character.query
        
        if query:
            characters = characters.filter(or_(
                Character.name.ilike(f"%{query}%"),
                Character.title.ilike(f"%{query}%"),
                Character.weapon.ilike(f"%{query}%")
            ))
        
        if min_magic or max_magic:
            characters = characters.filter(
                Character.magic_power.between(min_magic, max_magic)
            )
        
        results = []
        for char in characters.all():
            avg_rating = db.session.query(func.avg(Rating.rating))\
                .filter(Rating.character_id == char.id).scalar() or 0
            
            if avg_rating >= min_rating:
                results.append(char)
        
        return results
    
    @staticmethod
    def get_users_with_activity():
        """Get users sorted by their activity level"""
        return db.session.query(
            User,
            func.count(Review.id).label('review_count'),
            func.count(Rating.id).label('rating_count')
        ).outerjoin(Review).outerjoin(Rating)\
         .group_by(User.id)\
         .order_by(desc(func.count(Review.id) + func.count(Rating.id)))\
         .all()
    
    @staticmethod
    def clear_demo_data():
        """Clear all data from database"""
        Review.query.delete()
        Rating.query.delete()
        Battle.query.delete()
        User.query.delete()
        Character.query.delete()
        CharacterStats.query.delete()
        db.session.commit()
    
    @staticmethod
    def export_statistics():
        """Export comprehensive statistics"""
        stats = {
            'timestamp': datetime.now().isoformat(),
            'database_summary': DatabaseManager.get_database_summary(),
            'top_rated': [
                {
                    'name': char.name,
                    'rating': float(rating)
                }
                for char, rating in DatabaseManager.get_top_characters('rating', 5)
            ],
            'top_reviewed': [
                {
                    'name': char.name,
                    'reviews': count
                }
                for char, count in DatabaseManager.get_top_characters('reviews', 5)
            ]
        }
        return stats


# Example usage in Flask app context:
if __name__ == '__main__':
    from app import app
    
    with app.app_context():
        # Get top characters
        top_rated = DatabaseManager.get_top_characters('rating', 5)
        print("Top Rated:", top_rated)
        
        # Get database summary
        summary = DatabaseManager.get_database_summary()
        print("Summary:", summary)
        
        # Get user activity
        users = DatabaseManager.get_users_with_activity()
        print("Active Users:", users)
