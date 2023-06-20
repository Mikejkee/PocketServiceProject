import logging

from django.views.generic import TemplateView
from PocketServiceApp.models import Client


showcase_dict = {
    0: 'Найти бригаду для ремонта квартиры',
    1: 'Найти рабочего для ремонта техники',
    2: 'Найти рабочего для ремонта мебели',
    3: 'Найти мастера для услуг красоты',
}


class IndexView(TemplateView):
    template_name = 'index.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['telegram_id'] = self.request.GET.get('TelegramId')
        return context


class ShowcaseView(TemplateView):
    template_name = 'showcase.html'

    def get_context_data(self, **kwargs):
        context = super(ShowcaseView, self).get_context_data(**kwargs)
        context['telegram_id'] = self.request.GET.get('TelegramId')
        showcase_type = int(self.request.GET.get('ShowcaseType'))
        context['showcase_message'] = showcase_dict[showcase_type]
        context['showcase_type'] = showcase_type
        return context
