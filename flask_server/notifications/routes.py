from flask_server.utilities import token_required
from flask_server.users.crud import get_user_by_id
from .schemas import NotificationSchema
from . import crud, notifications_blueprint


@notifications_blueprint.route('/', methods=['GET'])
@token_required
def get_my_notifications(user):
    notifications = crud.get_user_notifications(user.id)
    data = [{
        'id': notification.id,
        'user': notification.drink.user.get_name(),
        'glasses': notification.drink.glasses,
        'datetime': notification.drink.datetime
    } for notification in notifications]
    return NotificationSchema().dumps(data, many=True), 200


@notifications_blueprint.route('/<int:notification_id>/', methods=['DELETE'])
@token_required
def delete_notification(user, notification_id):
    crud.delete_notification(user.id, notification_id)
    return 'Deleted', 202