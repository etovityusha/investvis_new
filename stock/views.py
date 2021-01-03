from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from stock.services import add_company, stock_info
from stock.forms import CompanyCreateForm
from stock.models import Stock


class AddCompany(LoginRequiredMixin, CreateView):
    form_class = CompanyCreateForm
    template_name = 'stock/create_company.html'
    success_url = reverse_lazy('deal_create')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj = add_company.download_and_save_stock_data(obj)
        obj.save()
        add_company.download_stock_quotations([obj.ticker_yf])
        return super(AddCompany, self).form_valid(form)


def ticker_page(request, ticker):
    """
    Рендер страницы компании. Включает:
        - информацию о компании
        - сделки пользователя, отправившего запрос
        - котировки
    """
    stock = Stock.objects.get(ticker=ticker)

    data = stock_info.get_data_about_stock(stock)
    quotations = stock_info.get_stock_quotations(stock, 30)
    deals = stock_info.get_deals_with_this_stock(stock, request.user)
    open_position = stock_info.get_open_position(stock, request.user)
    closed_position = stock_info.get_closed_position(stock, request.user)
    current_price, last_day_change_percent, last_day_change = stock_info.get_current_price_and_last_day_change(stock)
    graph = stock_info.graph(stock)
    return render(request, 'stock/ticker.html', {'data': data,
                                                 'quotations': quotations,
                                                 'deals': deals,
                                                 'open': open_position,
                                                 'closed': closed_position,
                                                 'current_price': current_price,
                                                 'last_day_change_percent': last_day_change_percent,
                                                 'last_day_change': last_day_change,
                                                 'graph': graph,
                                                 })
