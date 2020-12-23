from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from stock.services import add_company, stock_info
from stock.forms import CompanyCreateForm


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
    data = stock_info.get_data_about_stock(ticker)
    quotations = stock_info.get_stock_quotations(ticker, 30)
    deals = stock_info.get_deals_with_this_stock(ticker, request.user)
    return render(request, 'stock/ticker.html', {'data': data,
                                                     'quotations': quotations,
                                                     'deals': deals,
                                                     })
