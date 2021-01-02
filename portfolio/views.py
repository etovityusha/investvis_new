from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms, models
from .services.stats import get_open_portfolio_rows_by_user



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


class DealCreate(LoginRequiredMixin, CreateView):
    form_class = forms.DealCreateForm
    template_name = 'portfolio/create_deal.html'
    success_url = reverse_lazy('deals')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.currency = models.Stock.objects.get(ticker=obj.ticker).currency
        obj.nkd = 0
        obj.cost_without_nkd = obj.quantity * obj.price
        obj.total_cost = obj.cost_without_nkd + obj.nkd
        return super(DealCreate, self).form_valid(form)


@login_required
def portfolio_stats(request):
    portfolio_open = get_open_portfolio_rows_by_user(user=request.user)
    return render(request, 'portfolio/portfolio.html', {'portfolio_open': portfolio_open})
