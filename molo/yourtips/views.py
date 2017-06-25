from django.shortcuts import get_object_or_404

from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse

from molo.yourtips.forms import YourTipsEntryForm
from molo.yourtips.models import YourTipsPage


class YourTipsEntryView(CreateView):
    form_class = YourTipsEntryForm
    template_name = 'yourtips/your_tips_entry.html'

    def get_context_data(self, *args, **kwargs):
        context = super(
            YourTipsEntryView, self).get_context_data(*args, **kwargs)
        tip = get_object_or_404(
            YourTipsPage, slug=self.kwargs.get('slug'))
        context.update({'tip': tip})
        return context

    def get_success_url(self):
        return reverse(
            'molo.yourtips:thank_you',
            args=[self.object.tip.slug])

    def form_valid(self, form):
        tip = get_object_or_404(
            YourTipsPage, slug=self.kwargs.get('slug'))
        form.instance.tip = (
            tip.get_main_language_page().specific)
        if self.request.user.is_anonymous():
            form.instance.user = None
        else:
            form.instance.user = self.request.user
        return super(YourTipsEntryView, self).form_valid(form)


class ThankYouView(TemplateView):
    template_name = 'yourtips/thank_you.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ThankYouView, self).get_context_data(*args, **kwargs)
        tip = get_object_or_404(
            YourTipsPage, slug=self.kwargs.get('slug'))
        context.update({'tip': tip})
        return context
