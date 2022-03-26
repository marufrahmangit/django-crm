import random
from django.core.mail import send_mail
from django.views import generic
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganizerAndLoginRequiredMixin


class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

    context_object_name = 'agents'


class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'

    def get_queryset(self):
        return Agent.objects.all()

    context_object_name = 'agent'


class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(1, 100000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organization=self.request.user.userprofile
        )
        send_mail(
            subject='You are invited to be an agent',
            message='You were added as an agent on DJCRM. Please login to see updates.',
            from_email='test@email.com',
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

    def get_success_url(self):
        return reverse('agents:agent-list')


class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

    def get_success_url(self):
        return reverse('agents:agent-list')


