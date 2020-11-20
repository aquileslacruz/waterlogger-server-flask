from flask_server.models import Notification
from flask_server import db


def add_notification(user_id: int, drink_id: int):
    notification = Notification(user_id, drink_id)
    db.session.add(notification)
    db.session.commit()
    return notification


def delete_notification(user_id: int, notification_id: int):
    _ =  (
        db.session.query(Notification)
        .filter(
            Notification.user_id == user_id, 
            Notification.id == notification_id)
        .delete()
    )
    db.session.commit()
    return True


def get_user_notifications(user_id: int):
    return (
        db.session.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.id.desc())
        .all()
    )