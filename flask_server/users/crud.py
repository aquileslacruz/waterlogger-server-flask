from flask_server.models import User, Follow
from flask_server import db


def get_users_count():
    return db.session.query(User).count()


def get_users(page: int, limit: int):
    return db.session.query(User).offset((page - 1) * limit).limit(limit).all()


def create_user(
    username: str, password: str, first_name: any = None, last_name: any = None
):
    user = User(username, password, first_name=first_name, last_name=last_name)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_id(user_id: int):
    return db.session.query(User).filter(User.id == user_id).first()


def edit_user_by_id(user_id: int, data: dict):
    user = db.session.query(User).filter(User.id == user_id).first()
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.is_admin = data.get("is_admin", user.is_admin)
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return user


def delete_user_by_id(user_id: int):
    db.session.query(User).filter(User.id == user_id).delete()
    db.session.commit()
    return True


def follow_user(user: User, follow_id: int):
    follow = Follow(user.id, follow_id)
    db.session.add(follow)
    db.session.commit()
    return True


def unfollow_user(user: User, follow_id: int):
    db.session.query(Follow).filter(
        Follow.user_id == user.id, Follow.follow_id == follow_id
    ).delete()
    db.session.commit()
    return True


def get_user_followers(user_id: int):
    followers = (
        db.session.query(Follow)
        .filter(Follow.follow_id == user_id)
        .all()
    )
    return (
        db.session.query(User)
        .filter(User.id.in_([e.user_id for e in followers]))
        .all()
    )


def get_user_follows(user_id: int):
    follows = db.session.query(Follow).filter(Follow.user_id == user_id).all()
    return (
        db.session.query(User)
        .filter(User.id.in_([e.follow_id for e in follows]))
        .all()
    )


def search_by_username(user: User, query: str, skip: int = 0, limit: int = 10):
    return (
        db.session.query(User)
        .filter(User.username.startswith(queyr), User.id != user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
