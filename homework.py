import pandas as pd


class Record:
    def __init__(self, amount, comment, date=pd.to_datetime('today').date()):
        self.amount = amount
        self.comment = comment

        if type(date) == str:
            self.date = pd.to_datetime(date).date()
        else:
            self.date = date


class Calculator:
    records = []
    today = pd.to_datetime('today').date()

    def __init__(self, limit):
        self.limit = limit

    def add_record(self, record_obj):
        self.records.append(record_obj)

    def get_today_stats(self):
        today_amount = 0
        for rec in self.records:
            if rec.date == self.today:
                today_amount += rec.amount

        return today_amount

    def get_week_stats(self):
        date_list = pd.date_range(end=self.today, periods=7)
        week_amount = 0
        for rec in self.records:
            if pd.Timestamp(rec.date) in date_list:
                week_amount += rec.amount

        return week_amount


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_scored = super().get_today_stats()
        if calories_scored < self.limit:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'денегностью не более {self.limit - calories_scored} '
                    'кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 78
    EURO_RATE = 92

    def get_today_cash_remained(self, currency):
        rubles_amount = super().get_today_stats()
        message = ''
        if rubles_amount < self.limit:
            message = 'На сегодня осталось '
            rubles_for_answer = self.limit - rubles_amount
        elif rubles_amount > self.limit:
            message = 'денег нет, держись: твой долг - '
            rubles_for_answer = rubles_amount - self.limit
        else:
            return 'денег нет, держись'

        if currency == 'eur':
            eur = rubles_for_answer / self.EURO_RATE
            return message + str(round(eur, 2)) + ' Euro'
        elif currency == 'usd':
            usd = rubles_for_answer / self.USD_RATE
            return message + str(round(usd, 2)) + ' USD'
        else:
            return message + str(rubles_for_answer) + ' руб'
