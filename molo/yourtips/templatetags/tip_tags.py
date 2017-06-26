from copy import copy

from django import template

from molo.core.templatetags.core_tags import get_pages
from molo.yourtips.models import (
    YourTipsThankYouPage, YourTipsEntryPage
)

register = template.Library()


@register.assignment_tag(takes_context=True)
def load_thank_you_page_for_yourtips(context, tip):

    page = tip.get_main_language_page()
    locale = context.get('locale_code')

    qs = YourTipsThankYouPage.objects.child_of(page).filter(
        languages__language__is_main_language=True
    )

    if not locale:
        return qs

    if qs:
        return get_pages(context, qs, locale)
    else:
        return []


@register.inclusion_tag(
    'yourtips/your_tips_latest_tip_tag.html',
    takes_context=True
)
def your_tips_latest_tip(context):

    context = copy(context)
    # TODO: Change this query - to allow overwrite
    latest_article = YourTipsEntryPage.objects.filter(
        tip_entries__isnull=False,
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


@register.inclusion_tag(
    'yourtips/your_tips_menu.html',
    takes_context=True
)
def your_tips_menu_in_section(context, section):
    context = copy(context)
    context.update({
        'section': 'your-tips'
    })
    return context

