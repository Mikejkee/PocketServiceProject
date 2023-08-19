import logging

from django.views.generic import TemplateView
from PocketServiceApp.models import Person, Agent, Client


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
        telegram_id = self.request.GET.get('TelegramId')
        user = Person.objects.filter(telegram_id=str(telegram_id)).last()
        roles = user.role

        role_type_agent = roles.filter(role_type='Агент').last()
        if role_type_agent:
            agent = Agent.objects.filter(telegram_id=str(telegram_id)).last()
            context['company_name'] = agent.company.name

        role_type_head_agent = roles.filter(role_type='Управляющий организации').last()


        context['telegram_id'] = telegram_id
        context['role_type_agent'] = role_type_agent
        context['role_type_head_agent'] = role_type_head_agent

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
