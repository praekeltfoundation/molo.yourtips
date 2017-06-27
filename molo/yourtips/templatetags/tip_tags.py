from copy import copy

from django.core.exceptions import MultipleObjectsReturned
from django import template

from molo.yourtips.models import (
    YourTipsEntryPage, YourTipsPage
)

register = template.Library()


@register.inclusion_tag(
    'yourtips/your_tips_on_homepage.html',
    takes_context=True
)
def your_tips_on_homepage(context):
    context = copy(context)

    try:
        tip_on_homepage = YourTipsEntryPage.objects.get(
            featured_in_homepage=True
        )
    except (YourTipsEntryPage.DoesNotExist, MultipleObjectsReturned):
        tip_on_homepage = YourTipsEntryPage.objects.all(
        ).order_by('-featured_in_homepage_start_date').first()

    context.update({
        'article_tip': tip_on_homepage,
        'your_tip_page_slug': YourTipsPage.objects.first().slug
    })
    return context


@register.inclusion_tag(
    'yourtips/your_tips_create_tip_on_homepage.html',
    takes_context=True
)
def your_tips_create_tip_on_homepage(context):
    context = copy(context)
    context.update({
        'your_tip_page_slug': YourTipsPage.objects.first().slug
    })
    return context


@register.inclusion_tag(
    'yourtips/your_tips_create_tip_on_article.html',
    takes_context=True
)
def your_tips_create_tip_on_article(context):
    context = copy(context)
    context.update({
        'your_tip_page_slug': YourTipsPage.objects.first().slug
    })
    return context


@register.inclusion_tag(
    'yourtips/your_tips_section_menu.html',
    takes_context=True
)
def your_tips_menu_in_section(context, section):
    if section.slug == 'your-tips':
        context = copy(context)
        context.update({
            'section': section,
            'show_tips_menu': True
        })
    return context
