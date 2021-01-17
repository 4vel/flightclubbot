import logging
from db.models import TableUsers, TableUserAirports

logging.basicConfig(level = logging.INFO)


class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data_db(self, db_session, user_id):
        """ Возвращает список словарей
        destination["IATA Code"]
        destination["Lowest Price"]
        """

        destination_rows = db_session.query(TableUserAirports).filter_by(user_id = user_id)

        destination_data = []
        for row in destination_rows:
            destination_dict = {"IATA Code": row.airport_code, "Lowest Price": int(row.price)}
            destination_data.append(destination_dict)
        return destination_data

    def get_origin_airport(self, db_session, user_id):
        """ Получает аэропорт отправления юзера"""

        user_row = db_session.query(TableUsers).filter_by(user_id = user_id).first()
        return user_row.user_base_airport
