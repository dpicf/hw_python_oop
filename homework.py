import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

    def __eq__(self, other):
        return (self.amount == other.amount
                and self.comment == other.comment
                and self.date == other.date)


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()

    def add_record(self, record_obj):
        if record_obj not in self.records:
            self.records.append(record_obj)

    def get_today_stats(self):
        today_amount = 0
        for rec in self.records:
            if rec.date == self.today:
                today_amount += rec.amount
        return today_amount

    def get_week_stats(self):
        week_ago = self.today - dt.timedelta(days=7)
        week_amount = 0
        for rec in self.records:
            if self.today >= rec.date >= week_ago:
                week_amount += rec.amount
        return week_amount


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_scored = super().get_today_stats()
        if calories_scored < self.limit:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {self.limit - calories_scored} '
                    'кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 78.0
    EURO_RATE = 92.0

    def get_today_cash_remained(self, currency):
        rubles_amount = super().get_today_stats()
        message = ''
        if rubles_amount < self.limit:
            message = 'На сегодня осталось '
            rubles_for_answer = self.limit - rubles_amount
        elif rubles_amount > self.limit:
            message = 'Денег нет, держись: твой долг - '
            rubles_for_answer = rubles_amount - self.limit
        else:
            return 'Денег нет, держись'

        if currency == 'eur':
            eur = rubles_for_answer / self.EURO_RATE
            return message + str(round(eur, 2)) + ' Euro'
        elif currency == 'usd':
            usd = rubles_for_answer / self.USD_RATE
            return message + str(round(usd, 2)) + ' USD'
        else:
            return message + str(rubles_for_answer) + ' руб'
