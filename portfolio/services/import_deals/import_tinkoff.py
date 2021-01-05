import pandas as pd
from stock.models import Currency


def get_deals(excel_report_path) -> pd.DataFrame:
    """
    Получает на вход отчёт брокера в формате Excel и возвращает датафрейм с совершенными сделками.
    """
    df = pd.read_excel(excel_report_path, decimal=",")
    return _delete_repo_deals(
        _transfrom_tickers_with_deals_with_currencies(
            _filter_and_rename_columns(
                _filter_rows_with_closed_transactions(df).append(
                    _filter_rows_with_outstanding_transactions(df))
            )
        )
    )


def _filter_rows_with_closed_transactions(df) -> pd.DataFrame:
    """
    Возвращает строки из раздела
    '1.1 Информация о совершенных и исполненных сделках на конец отчетного периода'.
    """
    return df.loc[range(
        df.index[df[df.columns[0]] == '1.1 Информация о совершенных и исполненных сделках на конец отчетного '
                                      'периода'][0] + 2,
        df.index[df[df.columns[0]] == '1.2 Информация о неисполненных сделках на конец отчетного периода'][0])]


def _filter_rows_with_outstanding_transactions(df) -> pd.DataFrame:
    """
    Возвращает строки из раздела
    '1.2 Информация о неисполненных сделках на конец отчетного периода'
    В нем содержатся состоявшиеся сделки, которые не попали в раздел 1.1 из-за режима торгов.
    """
    return df.loc[range(
        df.index[df[df.columns[0]] == '1.2 Информация о неисполненных сделках на конец отчетного периода'][0] + 2,
        df.index[df[df.columns[0]] == '1.3 Сделки за расчетный период, обязательства из которых прекращены  '
                                      'не в результате исполнения '][0])]


def _filter_and_rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Удаляет лишние столбцы и переименовывает их в общий вид.
    Столбец с датой переводит во временной ряд.
    """
    columns = df.columns
    df = df[[columns[5], columns[22], columns[33], columns[38], columns[43], columns[47], columns[63]]]
    df.columns = ['date', 'transaction_type', 'ticker', 'price', 'currency', 'quantity', 'cost']
    df.to_datetime(df['date'], format='%d.%m.%Y')
    return df.dropna()


def _transfrom_tickers_with_deals_with_currencies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Получает датафрейм со сделками. Идентифицирует сделки с валютой и переименовывает их тикеры на общие.
    Например, 'USD000UTSTOM' на 'USD'.
    """
    currencies = Currency.objects.all().values_list('currency_ticker', flat=True)
    tickers = list(df['ticker'])
    for i, ticker in enumerate(tickers):
        for currency in currencies:
            if currency in ticker:
                tickers[i] = currency
    df['ticker'] = tickers
    return df


def _sum_identical_deals(deals: pd.DataFrame) -> pd.DataFrame:
    """
    Брокер Тинькофф при совершении сделки через лимитированную заявку дробит сделки.
    Фукнция их объединяет.
    """
    for column_name in ('quantity', 'total_cost'):
        deals[column_name] = deals.\
            groupby(['date', 'transaction_type', 'ticker', 'price', 'currency'])[column_name].\
            transform('sum')
    return deals.drop_duplicates(subset=['date', 'transaction_type', 'price', 'ticker', 'currency'])


def _delete_repo_deals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Удаляет из датафрейма сделки РЕПО.
    Read more: https://ru.wikipedia.org/wiki/%D0%A1%D0%B4%D0%B5%D0%BB%D0%BA%D0%B0_%D0%A0%D0%95%D0%9F%D0%9E
    """
    return df[df['transaction_type'].isin(['Покупка', 'Продажа'])]
