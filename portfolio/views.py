from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms


class ReportImport(LoginRequiredMixin, CreateView):
    form_class = forms.BrokerReportForm
    template_name = 'portfolio/import.html'
    success_url = reverse_lazy('deals')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(ReportImport, self).form_valid(form)
