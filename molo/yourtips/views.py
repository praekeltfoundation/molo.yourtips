from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, render

from molo.core.templatetags.core_tags import get_pages

from molo.yourtips.forms import YourTipsEntryForm
from molo.yourtips.models import YourTipsPage, YourTipsEntryPage

from el_pagination.decorators import page_template


class YourTipsEntryView(CreateView):
    form_class = YourTipsEntryForm
    template_name = 'yourtips/your_tips_entry.html'

    def get_context_data(self, *args, **kwargs):
        context = super(
            YourTipsEntryView, self).get_context_data(*args, **kwargs)
        tip_page = get_object_or_404(
            YourTipsPage, slug=self.kwargs.get('slug'))
        context.update({'tip_page': tip_page})
        return context

    def get_success_url(self):
        return reverse(
            'molo.yourtips:thank_you',
            args=[self.object.tip_page.slug])

    def form_valid(self, form):
        tip_page = get_object_or_404(
            YourTipsPage, slug=self.kwargs.get('slug'))
        form.instance.tip_page = (
            tip_page.get_main_language_page().specific)
        if self.request.user.is_anonymous():
            form.instance.user = None
        else:
            form.instance.user = self.request.user
        return super(YourTipsEntryView, self).form_valid(form)


class ThankYouView(TemplateView):
    template_name = 'yourtips/thank_you.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ThankYouView, self).get_context_data(*args, **kwargs)
        tip_page = get_object_or_404(
            YourTipsPage, slug=self.kwargs.get('slug'))
        context.update({'tip_page': tip_page})
        return context


class YourTipsRecentView(ListView):
    template_name = "yourtips/recent_tips.html"

    def get_queryset(self, *args, **kwargs):
        main = self.request.site.root_page
        context = {'request': self.request}
        locale = self.request.LANGUAGE_CODE
        articles = YourTipsEntryPage.objects.all(
        ).descendant_of(main).order_by('-latest_revision_created_at')
        return get_pages(context, articles, locale)

    def get_context_data(self, *args, **kwargs):
        context = super(YourTipsRecentView, self).get_context_data(
            *args, **kwargs
        )
        return context


@page_template('yourtips/recent_tip_for_paging.html')
def recent_tips_index(
    request,
    extra_context=None,
    template=('yourtips/recent_tip_for_paging.html')
):

    main = request.site.root_page
    context = {'request': request}
    locale = request.LANGUAGE_CODE

    articles = YourTipsEntryPage.objects.all().descendant_of(main).order_by(
        'latest_revision_created_at'
    )
    object_list = get_pages(context, articles, locale)
    locale_code = request.GET.get('locale')

    return render(
        request, template, {
            'object_list': object_list,
            'locale_code': locale_code
        }
    )
