import sched
import time
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from app.data_manager import DataManager
from app.flight_search import FlightSearch
from app.notification import NotificationManager
from config import BOT_TOKEN, ADMIN_ID

s = sched.scheduler(time.time, time.sleep)

data_manager = DataManager()
notification_manager = NotificationManager(BOT_TOKEN, ADMIN_ID)

data_package = {
    "sheet_data": data_manager.get_destination_data(),
    "flight_search": FlightSearch(),
    "notification_manager": notification_manager,
    "ORIGIN_CITY_IATA": "MOW",
    "tomorrow": datetime.now() + timedelta(days = 1),
    "six_month_from_today": datetime.now() + timedelta(days = (6 * 30)),
}


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

        if flight:
            # print(flight.price, destination["Lowest Price"])
            if flight.price < destination["Lowest Price"]:

                msg = ""
                if flight.check_weekend_plus():
                    msg += "Выходные плюс 1! \n"
                elif flight.check_weekend():
                    msg += "Выходные!\n"

                msg += f"Перелет из {flight.origin_city}-{flight.origin_airport} "
                msg += f"в {flight.destination_city}-{flight.destination_airport} за {flight.price} рублей.\n"
                msg += f"Даты: {flight.out_date} ({flight.out_date_weekday})"
                msg += f"- {flight.return_date} ({flight.return_date_weekday}).\n "
                msg += f"Продолжительность {flight.duration_days} д"

                if msg not in msg_cache:
                    data_pack["notification_manager"].send_sms(
                        message = msg
                    )
                    msg_cache.append(msg)


message_cache = []
sched = BlockingScheduler()


def checkflighs_short():
    search_flights(data_package, "short", message_cache)


def checkflights_long():
    search_flights(data_package, "long", message_cache)


def healthcheck():
    notification_manager.send_sms("💟")


sched.add_job(checkflighs_short, 'interval', minutes = 5)
sched.add_job(checkflights_long, 'interval', minutes = 3)
sched.add_job(healthcheck, 'interval', hours = 1)
sched.start()
