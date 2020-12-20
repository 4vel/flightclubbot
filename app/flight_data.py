from datetime import datetime


class FlightData:

    def __init__(self, price, origin_city, origin_airport, destination_city, destination_airport, out_date,
                 return_date):

        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.out_date_weekday_num = datetime.strptime(out_date, '%Y-%m-%d').weekday()
        self.return_date_weekday_num = datetime.strptime(return_date, '%Y-%m-%d').weekday()
        self.weekdays_dict = {
            0: "понедельник",
            1: "вторник",
            2: "среда",
            3: "четверг",
            4: "пятница",
            5: "суббота",
            6: "воскресенье",
        }
        self.out_date_weekday = self.weekdays_dict.get(self.out_date_weekday_num)
        self.return_date_weekday = self.weekdays_dict.get(self.return_date_weekday_num)
        self.duration_delta = datetime.strptime(return_date, '%Y-%m-%d') - datetime.strptime(out_date, '%Y-%m-%d')
        self.duration_days = self.duration_delta.days

    def check_weekend(self):
        """ Проверяет выходные """

        dts = datetime.strptime(self.out_date, '%Y-%m-%d')
        dte = datetime.strptime(self.return_date, '%Y-%m-%d')
        delta = dte - dts
        if 1 <= delta.days <= 2:
            if dts.weekday() in [4, 5]:
                return True
            else:
                return False
        else:
            return False

    def check_weekend_plus(self):
        """ Проверяет выходные плюс один день """

        dts = datetime.strptime(self.out_date, '%Y-%m-%d')
        dte = datetime.strptime(self.return_date, '%Y-%m-%d')
        delta = dte - dts
        if 1 <= delta.days <= 2:
            if 4 == dts.weekday() and dte.weekday() == 6:
                return True
            elif 5 == dts.weekday() and dte.weekday() == 0:
                return True
            else:
                return False
        else:
            return False
