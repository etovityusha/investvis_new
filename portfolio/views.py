from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import Profile
from portfolio import forms, models
from portfolio.services.stats import get_open_portfolio_rows_by_user, get_closed_portfolio_rows_by_user
from portfolio.services.analytics import scatter_plot_html, currencies_pie_html, sectors_pie_html,\
    income_composition_graph_html, closed_income_composition_graph_html


class ReportImport(LoginRequiredMixin, CreateView):
    form_class = forms.BrokerReportForm
    template_name = 'portfolio/import.html'
    success_url = reverse_lazy('deals')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(ReportImport, self).form_valid(form)


class DealList(LoginRequiredMixin, ListView):
    model = models.Deal
    template_name = 'portfolio/deals.html'
    context_object_name = 'deals'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DealList, self).get_context_data(**kwargs)
        context['title'] = 'Сделки'
        return context

    def get_queryset(self):
        return models.Deal.objects.filter(user_id=self.request.user)


class DealCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = forms.DealCreateForm
    template_name = 'portfolio/create_deal.html'
    success_url = reverse_lazy('deals')
    success_message = 'Сделка добавлена'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.currency = models.Stock.objects.get(ticker=obj.ticker).currency
        obj.source = 'F'
        obj.total_cost = obj.quantity * obj.price
        return super(DealCreate, self).form_valid(form)


@login_required
def portfolio_stats(request):
    portfolio_open = get_open_portfolio_rows_by_user(user=request.user)
    return render(request, 'portfolio/portfolio.html', {
        'portfolio_open': portfolio_open,
    })


@login_required
def analytics(request):
    portfolio_open = get_open_portfolio_rows_by_user(user=request.user)
    portfolio_closed = get_closed_portfolio_rows_by_user(user=request.user)
    if portfolio_open:
        base_currency = Profile.objects.get(user=request.user).analytics_currency
        scatter_plot = scatter_plot_html(portfolio_rows=portfolio_open, base_currency=base_currency)
        currencies_pie = currencies_pie_html(portfolio_rows=portfolio_open, base_currency=base_currency)
        sectors_pie = sectors_pie_html(portfolio_rows=portfolio_open, base_currency=base_currency)
        open_income = income_composition_graph_html(portfolio_rows=portfolio_open, base_currency=base_currency)
        if portfolio_closed:
            closed_income = closed_income_composition_graph_html(portfolio_rows=portfolio_closed, base_currency=base_currency)
        else:
            closed_income = False
        return render(request, 'portfolio/analytics.html', {
            'portfolio_open': portfolio_open,
            'scatter_plot': scatter_plot,
            'base_currency': base_currency,
            'currencies_pie': currencies_pie,
            'sectors_pie': sectors_pie,
            'open_income': open_income,
            'closed_income': closed_income,
        })
    else:
        return render(request, 'portfolio/analytics.html', {
            'portfolio_open': False
        })
