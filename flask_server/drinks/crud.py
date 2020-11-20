from flask_server.models import Drink, Follow
from flask_server.users.crud import get_user_followers
from flask_server.notifications.crud import add_notification
from flask_server import db


def create_drink(user_id: int, glasses: int):
    # Create Drink
    drink = Drink(user_id, glasses)
    db.session.add(drink)
    db.session.commit()
    db.session.refresh(drink)

    # Notify the followers
    followers = get_user_followers(user_id)
    for follower in followers:
        add_notification(follower.id, drink.id)
    
    return drink