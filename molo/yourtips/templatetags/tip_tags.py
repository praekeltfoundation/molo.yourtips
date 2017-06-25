from copy import copy

from django import template
from django.utils import timezone

from molo.core.templatetags.core_tags import get_pages
from molo.yourtips.models import (
    YourTipsThankYou, YourTipsEntryPage, YourTipsArticleIndexPage
)

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
    latest_article = YourTipsEntryPage.objects.filter(
        tip_entries__isnull=False,
        featured_in_homepage_start_date__isnull=False
    ).order_by('-featured_in_homepage_start_date')

    tip_article_index = YourTipsArticleIndexPage.objects.get(
        title='Read Tips', slug='read-tips'
    )

    print tip_article_index.latest_articles()
    context.update({
        'article_tip': latest_article.first()
    })
    return context


@register.inclusion_tag(
    'yourtips/your_tips_recent_tips_tag.html',
    takes_context=True
)
def your_tips_recent_tips(context):

    context = copy(context)
    # TODO: Change this query - to allow overwrite
    latest_article = YourTipsEntryPage.objects.filter(
        tip_entries__isnull=False,
        featured_in_homepage_start_date__isnull=False
    ).order_by('-featured_in_homepage_start_date')

    tip_article_index = YourTipsArticleIndexPage.objects.get(
        title='Read Tips', slug='read-tips'
    )

    print tip_article_index.latest_articles()
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
    print context
    return context


# @register.inclusion_tag(
#     'yourtips/your_tips_recent_tag_for_section.html',
#     takes_context=True
# )
# def your_tips_menu_in_section(context, section):
#     context = copy(context)
#     locale_code = context.get('locale_code')
#     page = section.get_main_language_page()
#     if page:
#         competitions = (
#             YourWordsCompetition.objects.child_of(page).filter(
#                 languages__language__is_main_language=True).specific())
#     else:
#         competitions = YourWordsCompetition.objects.none()
#
#     context.update({
#         'competitions': get_pages(context, competitions, locale_code),
#         'section': section
#     })
#     return context
