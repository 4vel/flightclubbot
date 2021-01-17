from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from flight_app.data_manager import DataManager
from flight_app.flight_search import FlightSearch
from flight_app.notification import NotificationManager
from config import BOT_TOKEN, ADMIN_ID, conn_string
from db.models import DataAccessLayer, TableUsers

data_manager = DataManager()
sched = BlockingScheduler()
notification_manager = NotificationManager(BOT_TOKEN)
message_cache = []

def get_data_pack(db_session, user_id):
    """
    data_package представляет собой словарь в котором находятся объекты для

    :param db_session:
    :param user_id:
    :return:
    """

    data_package = {
        "user": user_id,
        "sheet_data": data_manager.get_destination_data_db(db_session, user_id),
        "flight_search": FlightSearch(),
        "notification_manager": notification_manager,
        "ORIGIN_CITY_IATA": data_manager.get_origin_airport(db_session, user_id),
        "tomorrow": datetime.now() + timedelta(days = 1),
        "six_month_from_today": datetime.now() + timedelta(days = (6 * 30)),
    }
    return data_package


def get_list_of_users(db_session):
    """ Возвращает список пользователей """

    return [u.user_id for u in db_session.query(TableUsers).distinct()]


def search_flights(data_pack, period, msg_cache):
    for destination in data_pack["sheet_data"]:

        if period == "long":
            flight = data_pack["flight_search"].check_flights(
                data_pack["ORIGIN_CITY_IATA"],
                destination["IATA Code"],
                from_time = data_pack["tomorrow"],
                to_time = data_pack["six_month_from_today"]
            )
        else:
            flight = data_pack["flight_search"].check_flights_short(
                data_pack["ORIGIN_CITY_IATA"],
                destination["IATA Code"],
                from_time = data_pack["tomorrow"],
                to_time = data_pack["six_month_from_today"]
            )
        print(flight)
        if flight:
            print(flight.price, destination["Lowest Price"])
            if flight.price < destination["Lowest Price"]:

                msg = ""
                if flight.check_weekend_plus():
                    msg += "Выходные плюс 1! \n"
                elif flight.check_weekend():
                    msg += "Выходные!\n"

                msg += f"Перелет из {flight.origin_city}-{flight.origin_airport} "
                msg += f"в {flight.destination_city}-{flight.destination_airport} за {flight.price} рублей.\n"
                # msg += f" Авиакомпания {flight.airline} рейс {flight.flight_no }.\n"
                msg += f"Даты: {flight.out_date} ({flight.out_date_weekday})"
                msg += f"- {flight.return_date} ({flight.return_date_weekday}).\n "
                msg += f"Продолжительность {flight.duration_days} д"

                if msg not in msg_cache:
                    data_pack["notification_manager"].send_sms(data_pack['user'], message = msg)
                    msg_cache.append(msg)




def checkflighs_short(db_session):
    """
    Ищет билеты туда и обратно на несколько дней
    формируем список юзеров
    по каждому юзеру формируем датапаки
    проходимся search_flights по каждому
    """

    list_of_users = get_list_of_users(db_session)
    list_of_users_datapackages = []

    for user in list_of_users:
        data_pack = get_data_pack(db_session, user)
        if data_pack.get("sheet_data"):
            list_of_users_datapackages.append(data_pack)

    for dp in list_of_users_datapackages:
        search_flights(dp, "short", message_cache)


def checkflights_long(db_session):
    """
    Ищет билеты туда и обратно на продолжительный период
    формируем список юзеров
    по каждому юзеру формируем датапаки
    проходимся search_flights по каждому
    """

    list_of_users = get_list_of_users(db_session)
    list_of_users_datapackages = []

    for user in list_of_users:
        data_pack = get_data_pack(db_session, user)
        if data_pack.get("sheet_data"):
            list_of_users_datapackages.append(data_pack)

    for dp in list_of_users_datapackages:
        search_flights(dp, "long", message_cache)


def healthcheck():
    """Отправляет сердечко админу"""

    notification_manager.send_sms(ADMIN_ID, "💟")


if __name__ == "__main__":
    dal = DataAccessLayer(conn_string)
    session = dal.get_session()
    data_manager = DataManager()
    notification_manager = NotificationManager(BOT_TOKEN)

    sched.add_job(checkflighs_short, 'interval', minutes = 5, args = [session])
    sched.add_job(checkflights_long, 'interval', minutes = 7, args = [session])
    sched.add_job(healthcheck, 'interval', hours = 24)
    sched.start()
