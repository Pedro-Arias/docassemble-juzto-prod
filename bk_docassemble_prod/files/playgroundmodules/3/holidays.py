import pandas as pd
import datetime
from datetime import timedelta
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, Easter, Day
from pandas.tseries.offsets import CustomBusinessDay

# https://es.linkedin.com/pulse/calendario-con-festivos-colombianos-en-python-lema-daniel
# https://github.com/pandas-dev/pandas/blob/main/pandas/tseries/holiday.py

def strict_next_monday(dt: datetime) -> datetime:
    """
    Si el festivo cae en un día diferente a lunes, se corre al próximo lunes
    """
    if dt.weekday() > 0:
        return dt + timedelta(7-dt.weekday())
    return dt


class ColombianBusinessCalendar(AbstractHolidayCalendar):

    rules = [
        # festivos fijos
        Holiday('Año nuevo', month=1, day=1),
        Holiday('Día del trabajo', month=5, day=1),
        Holiday('Día de la independencia', month=7, day=20),
        Holiday('Batalla de Boyacá', month=8, day=7),
        Holiday('Inmaculada Concepción', month=12, day=8),
        Holiday('Navidad', month=12, day=25),
        # festivos relativos a la pascua
        Holiday('Jueves santo', month=1, day=1, offset=[Easter(), Day(-3)]),
        Holiday('Viernes santo', month=1, day=1, offset=[Easter(), Day(-2)]),
        Holiday('Ascención de Jesús', month=1,
                day=1, offset=[Easter(), Day(43)]),
        Holiday('Corpus Christi', month=1, day=1, offset=[Easter(), Day(64)]),
        Holiday('Sagrado Corazón de Jesús', month=1,
                day=1, offset=[Easter(), Day(71)]),
        # festivos desplazables (Emiliani)
        Holiday('Epifanía del señor', month=1, day=6,
                observance=strict_next_monday),
        Holiday('Día de San José', month=3, day=19,
                observance=strict_next_monday),
        Holiday('San Pedro y San Pablo', month=6,
                day=29, observance=strict_next_monday),
        Holiday('Asunción de la Virgen', month=8,
                day=15, observance=strict_next_monday),
        Holiday('Día de la raza', month=10, day=12,
                observance=strict_next_monday),
        Holiday('Todos los santos', month=11, day=1,
                observance=strict_next_monday),
        Holiday('Independencia de Cartagena', month=11,
                day=11, observance=strict_next_monday)
    ]

def compute_date(my_date, increment_days):
    the_date = my_date.date()
    Colombian_BD = CustomBusinessDay(calendar=ColombianBusinessCalendar())
    s = pd.date_range(start=the_date,periods=increment_days, freq=Colombian_BD)
    qty_days = s.to_pydatetime()
    last_date = qty_days[-1]
    return last_date

def difference_bussiness_days(start_date, end_date):
    start_date = start_date.date()
    end_date = end_date.date()
    Colombian_BD = CustomBusinessDay(calendar=ColombianBusinessCalendar())
    s = pd.date_range(start=start_date,end=end_date, freq=Colombian_BD)
    qty_days = s.to_pydatetime()
    return qty_days.size-1

def range_bussiness_days(start_date,end_date):
    start_date = start_date.date()
    end_date = end_date.date()
    Colombian_BD = CustomBusinessDay(calendar=ColombianBusinessCalendar())
    s = pd.date_range(start=start_date,
                      end=end_date, freq=Colombian_BD)
    qty_days = s.to_pydatetime()
    return qty_days

def is_bussiness_days(my_date):
    my_date = my_date.date()
    head_date = (my_date - Day(4))
    tail_date = (my_date + Day(4))
    
    range_date = range_bussiness_days(head_date,tail_date)
    for bussiness_date in range_date:
        if bussiness_date.date() == my_date:
            return True
    return False