from db.models import TableUserAirports


def add_destination(session, user, airport, price):
    """
    Добавляет направление и пороговую цену для юзера

    :param user:
    :param airport:
    :param price:
    :return:
    """
    uap = TableUserAirports(user, airport, int(price))
    session.add(uap)
    session.commit()


def check_existing_destination(session, user, airport):
    """
    Проверяет есть ли уже у этого юзера такое направление
    :param user:
    :param airport:
    :param price:
    :return:
    """
    result = session.query(TableUserAirports).filter_by(airport_code=airport, user_id=user)
    if list(result):
        return True
    else:
        return False


def remove_existing_destination(session, user, airport):
    """
    Удаляет существующее направление
    :param user:
    :param airport:
    :param price:
    :return:
    """

    session.query(TableUserAirports).filter_by(airport_code=airport, user_id=user).delete()
    session.commit()
