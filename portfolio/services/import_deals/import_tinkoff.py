import pandas as pd
from stock.models import Currency


def get_deals(excel_report_path) -> pd.DataFrame:
    """
    Получает на вход отчёт брокера в формате Excel и возвращает датафрейм с совершенными сделками
    """
    df = pd.read_excel(excel_report_path, decimal=",")
    df.columns = df.iloc[6]
    df = df.loc[range(
        df.index[df['Номер сделки'] == '1.1 Информация о совершенных и исполненных сделках на конец отчетного периода'][
            0] + 2,
        df.index[df['Номер сделки'] == '1.2 Информация о неисполненных сделках на конец отчетного периода'][0])]
    df = df[
        ['Дата заклю\nчения', 'Вид сделки', 'Код актива', 'Цена за едини\nцу', 'Валю\nта цены', 'Количество',
         'Сумма сделки']].reset_index(drop=True)
    df.columns = (['date', 'transaction_type', 'ticker', 'price', 'currency', 'quantity', 'total_cost'])
    df = df[(df['transaction_type'] == 'Покупка') | (df['transaction_type'] == 'Продажа')]

    currencies = Currency.objects.all().values_list('currency_ticker', flat=True)
    tickers = list(df['ticker'])
    for i, ticker in enumerate(tickers):
        for currency in currencies:
            if currency in ticker:
                tickers[i] = currency
    df['ticker'] = tickers
    return df
