from django.db.models import Q

from stock.models import CurrencyCourse, Currency

import pandas as pd
from decimal import Decimal
import plotly.express as px
import plotly.graph_objects as go


def _get_current_currency_courses(base_currency):
    return CurrencyCourse.objects.all().filter(Q(currency1=base_currency) | Q(currency2=base_currency))


def _get_current_currency_course(courses, base_cur: Currency, second_cur: Currency) -> Decimal:
    if base_cur == second_cur:
        return Decimal('1')
    for course in courses:
        if course.currency1 == base_cur and course.currency2 == second_cur:
            return 1 / course.close
        elif course.currency2 == base_cur and course.currency1 == second_cur:
            return course.close


def scatter_plot_html(portfolio_rows, base_currency):
    courses = _get_current_currency_courses(base_currency)
    df = pd.DataFrame(columns=['Тикер', 'Стоимость', 'Изменение', 'Сектор'])
    i = 0
    for row in portfolio_rows:
        cost = row.cost
        if row.currency != base_currency:
            cur_course = _get_current_currency_course(courses, base_currency, row.currency)
            cost *= cur_course
        df.loc[i] = [row.ticker, cost, row.change, row.sector]
        i += 1
    df = df.dropna()
    df['Стоимость'] = pd.to_numeric(df["Стоимость"], downcast="float")
    fig = px.scatter(df, x='Стоимость', y='Изменение', color='Сектор', hover_name='Тикер', size='Стоимость', text='Тикер',
                     hover_data={
                         'Изменение': ':.2f',
                         'Стоимость': ':.2f',
                         'Тикер': False,
                     },
                     height=600, size_max=40)

    fig.update_layout(legend={'title': {'font': {'size': 14}, 'text': 'Сектор: '},
                              'orientation': "h",
                              'yanchor': "bottom",
                              'y': 1.02,
                              'xanchor': "right",
                              'x': 1},
                      hoverlabel={
                          'bgcolor': 'white',
                          'font_size': 16,
                          'font_family': "Rockwell"
                      },
                      xaxis_title=f"Стоимость в {base_currency}",
                      yaxis_title="Изменение стоимости, %", )
    return fig.to_html(full_html=False, include_plotlyjs='cdn')


def currencies_pie_html(portfolio_rows, base_currency):
    stocks_sum = {}
    for row in portfolio_rows:
        if row.currency.currency_ticker not in stocks_sum.keys():
            stocks_sum[row.currency.currency_ticker] = row.cost
        else:
            stocks_sum[row.currency.currency_ticker] += row.cost

    stocks_sum = {k: v for k, v in stocks_sum.items() if v != 0}
    courses = _get_current_currency_courses(base_currency)

    for key, value in stocks_sum.items():
        course = _get_current_currency_course(courses, base_cur=base_currency,
                                              second_cur=Currency.objects.get(currency_ticker=key))
        stocks_sum[key] *= course

    trace = [go.Pie(labels=list(stocks_sum.keys()), values=list(stocks_sum.values()))]
    fig = go.Figure(data=trace)
    colors = px.colors.qualitative.Safe
    fig.update_traces(hoverinfo='label+percent', texttemplate="<b>%{label}</b><br> %{value:.2f}",
                      textfont_size=16,
                      marker=dict(colors=colors, line=dict(color='#000000', width=1)))
    fig.update_layout(showlegend=False)
    return fig.to_html(full_html=False, include_plotlyjs=False)


def sectors_pie_html(portfolio_rows, base_currency):
    sectors = {}
    courses = _get_current_currency_courses(base_currency)
    for row in portfolio_rows:
        course = _get_current_currency_course(courses, base_cur=base_currency, second_cur=row.currency)
        cost = row.cost * course
        if row.sector.sector_rus not in sectors.keys():
            sectors[row.sector.sector_rus] = cost
        else:
            sectors[row.sector.sector_rus] += cost

    sectors = {k: v for k, v in sectors.items() if v != 0}
    trace = [go.Pie(labels=list(sectors.keys()), values=list(sectors.values()))]
    fig = go.Figure(data=trace)
    colors = px.colors.qualitative.Safe
    fig.update_traces(hoverinfo='label+percent', texttemplate="<b>%{label}</b><br> %{value:.2f}",
                      textfont_size=14,
                      marker=dict(colors=colors, line=dict(color='#000000', width=1)))
    fig.update_layout(showlegend=False)
    return fig.to_html(full_html=False, include_plotlyjs=False)


def income_composition_graph_html(portfolio_rows, base_currency):
    profits = {}
    courses = _get_current_currency_courses(base_currency)
    for row in portfolio_rows:
        profit = (row.current_price - row.average_buy_price) * row.quantity
        profits[row.ticker] = round(profit * _get_current_currency_course(courses, base_currency, row.currency), 1)
    profits = dict(sorted(profits.items(), key=lambda item: item[1], reverse=True))

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative" for i in range(len(list(profits.keys())))] + ['total'],
        x=list(profits.keys()) + ['total'],
        textposition="outside",
        textangle=-90,
        texttemplate='%{text:.2s}',
        text=list(profits.values()) + [sum(list(profits.values()))],
        y=list(profits.values()) + [sum(list(profits.values()))],
    ))

    fig.update_layout(
        title="Состав дохода (открытые позиции)",
        showlegend=False
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)


def closed_income_composition_graph_html(portfolio_rows, base_currency):
    profits = {}
    courses = _get_current_currency_courses(base_currency)
    for row in portfolio_rows:
        profit = row.income
        profits[row.ticker] = round(profit * _get_current_currency_course(courses, base_currency, row.currency), 1)
    profits = dict(sorted(profits.items(), key=lambda item: item[1], reverse=True))

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative" for i in range(len(list(profits.keys())))] + ['total'],
        x=list(profits.keys()) + ['total'],
        textposition="outside",
        textangle=-90,
        texttemplate='%{text:.2s}',
        text=list(profits.values()) + [sum(list(profits.values()))],
        y=list(profits.values()) + [sum(list(profits.values()))],
    ))

    fig.update_layout(
        title="Состав дохода (закрытые позиции)",
        showlegend=False
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)
