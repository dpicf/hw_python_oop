"""
Данный модуль содержит классы Record, Calculator, CaloriesCalculator,
CashCalculator. Данные классы нужны для подсчета расходов и доходов.
"""
import datetime as dt
from typing import Optional


class Record:
    """
    Класс Record создаёт объект со свойствами amount, comment, date.
    """

    def __init__(self, amount: int, comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    """
    Родительский класс Calculator содержит методы add_record, get_today_stats,
    get_week_stats. Содержит свойства limit и список объектов-записей records
    """

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.records: list[Record] = []

    def add_record(self, record: Record) -> None:
        """
        Метод add_record добавляет объекты к списку records
        """
        self.records.append(record)

    def get_today_stats(self) -> int:
        """
        Метод get_today_stats возвращает сумму набранных калорий
        или потраченных денег за сегодняшний день.
        """
        return sum(rec.amount for rec in self.records
                   if rec.date == dt.date.today())

    def get_week_stats(self) -> int:
        """
        Метод get_week_stats возвращает сумму набранных калорий
        или потраченных денег за прошедшую неделю.
        """
        week_ago: dt.date = dt.date.today() - dt.timedelta(days=7)
        return sum(rec.amount for rec in self.records
                   if dt.date.today() >= rec.date >= week_ago)


class CaloriesCalculator(Calculator):
    """
    Класс CaloriesCalculator наследует функционал родительского класса
    Calculator. Содержит метод get_calories_remained. Принимает как аргумент
    лимит калорий на сегодня.
    """

    def get_calories_remained(self) -> str:
        """
        Метод get_calories_remained возвращает строку-рекомендацию о
        потреблении калорий.
        """
        calories: int = self.get_today_stats()
        if calories < self.limit:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {self.limit - calories} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """
    Класс CashCalculator наследует функционал родительского класса Calculator.
    Содержит метод get_today_cash_remained. Принимает как аргумент лимит денег
    на сегодня. Также содержит курсы валют.
    """

    USD_RATE = 78.0
    EURO_RATE = 92.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency: str) -> str:
        """
        Метод get_calories_remained возвращает строку-рекомендацию о расходе
        денег. Принимает как аргумент код валюты в виде строки.
        """
        money: int = self.limit - self.get_today_stats()

        if money == 0:
            return 'Денег нет, держись'

        currencies: dict[str,
                         tuple(str, float)] = {'usd': ('USD', self.USD_RATE),
                                               'eur': ('Euro', self.EURO_RATE),
                                               'rub': ('руб', self.RUB_RATE)}

        if currency not in currencies:
            return f'Не знаю такую валюту: {currency}'

        currency_out: str
        rate: float
        currency_out, rate = currencies[currency]
        money_currency: float = money / rate

        if money_currency > 0:
            return f'На сегодня осталось {money_currency:.2f} {currency_out}'
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{abs(money_currency):.2f} {currency_out}')
