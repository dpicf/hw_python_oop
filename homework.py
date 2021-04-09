import datetime as dt
from typing import Optional


class Record:
    def __init__(self, amount: int, comment: str, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit: int):
        self.limit = limit
        self.records: list = []

    def add_record(self, record: object) -> None:
        self.records.append(record)

    def get_today_stats(self) -> int:
        return sum(rec.amount for rec in self.records
                   if rec.date == dt.date.today())

    def get_week_stats(self) -> int:
        week_ago: dt.date = dt.date.today() - dt.timedelta(days=7)
        return sum(rec.amount for rec in self.records
                   if dt.date.today() >= rec.date >= week_ago)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        calories: int = self.get_today_stats()
        if calories < self.limit:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {self.limit - calories} '
                    'кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 78.0
    EURO_RATE = 92.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency: str) -> str:
        money: int = self.limit - self.get_today_stats()

        if money == 0:
            return 'Денег нет, держись'

        currencies: dict = {'usd': ('USD', self.USD_RATE),
                            'eur': ('Euro', self.EURO_RATE),
                            'rub': ('руб', self.RUB_RATE)}

        if currency not in currencies:
            return f'Не знаю такую валюту: {currency}'

        currency_out: str
        rate: float
        currency_out, rate = currencies[currency]
        money_currency: float = money / rate

        if money_currency > 0:
            return ('На сегодня осталось {:.2f} {}'
                    .format(money_currency, currency_out))
        else:
            return ('Денег нет, держись: твой долг - {:.2f} {}'
                    .format(abs(money_currency), currency_out))
