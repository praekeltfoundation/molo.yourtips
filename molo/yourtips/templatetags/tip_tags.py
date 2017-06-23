from django import template
from copy import copy
from molo.yourtips.models import YourTipsThankYou
from molo.core.models import ArticlePage
from molo.core.templatetags.core_tags import get_pages


register = template.Library()


@register.assignment_tag(takes_context=True)
def load_thank_you_page_for_yourtips(context, tip):

    page = tip.get_main_language_page()
    locale = context.get('locale_code')

    qs = YourTipsThankYou.objects.child_of(page).filter(
        languages__language__is_main_language=True)

    if not locale:
        return qs

    if qs:
        return get_pages(context, qs, locale)
    else:
        return []


@register.inclusion_tag(
    'yourtips/your_tips_tip_tag.html',
    takes_context=True
)
def your_tips_tip(context):
    context = copy(context)
    # TODO: Change this query - to allow overwrite
    latest_article = ArticlePage.objects.filter(
        tip_entry__isnull=False,
        featured_in_homepage_start_date__isnull=False
    ).order_by('-featured_in_homepage_start_date')

    context.update({
        'article_tip': latest_article.first()
    })
    return context


@register.inclusion_tag(
    'yourtips/your_tips_share_your_tip.html',
    takes_context=True
)
def your_tips_share_your_tip(context):
    pass
