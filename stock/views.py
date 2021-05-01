from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from stock.services import add_company, stock_info
from stock.forms import CompanyCreateForm
from stock.models import Stock, StockPrice


class AddCompany(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = CompanyCreateForm
    template_name = 'stock/create_company.html'
    success_url = reverse_lazy('deal_create')
    success_message = "Акция успешно добавлена!"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj = add_company.download_and_save_stock_data(obj)
        obj.save()
        add_company.download_stock_quotations([obj.ticker_yf])
        return super(AddCompany, self).form_valid(form)


class StockDetail(DetailView):
    """
    Рендер страницы компании. Включает:
        - информацию о компании
        - сделки пользователя, отправившего запрос
        - котировки
    """
    model = Stock
    template_name = 'stock/ticker.html'
    slug_field = 'ticker'
    slug_url_kwarg = 'ticker'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = stock_info.get_data_about_stock(self.object)
        context['quotations'] = stock_info.get_stock_quotations(self.object, 30)
        context['deals'] = stock_info.get_deals_with_this_stock(self.object, self.request.user)
        context['open_position'] = stock_info.get_open_position(self.object, self.request.user)
        context['closed_position'] = stock_info.get_closed_position(self.object, self.request.user)
        context['current_price'], context['last_day_change_percent'], context['last_day_change'] = stock_info.\
            get_current_price_and_last_day_change(self.object)
        context['data_plot'] = [[el.date_to_timestamp_in_ms, round(float(el.close), 2)] for el in
                                StockPrice.objects.filter(ticker=self.object.pk).order_by('date')]
        return context
