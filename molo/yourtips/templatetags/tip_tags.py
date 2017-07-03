from copy import copy

from django import template

from molo.yourtips.models import YourTipsEntry, YourTip, YourTipsArticlePage

register = template.Library()


@register.inclusion_tag(
    'yourtips/your_tips_on_homepage.html',
    takes_context=True
)
def your_tips_on_homepage(context):
    context = copy(context)

    tip_on_homepage = YourTipsArticlePage.objects.filter(
        featured_in_homepage=True).order_by(
            '-featured_in_homepage_start_date').first()

    if not tip_on_homepage:
        tip_on_homepage = YourTipsArticlePage.objects.all().order_by(
            '-latest_revision_created_at').first()

    context.update({
        'article_tip': tip_on_homepage,
        'your_tip_page_slug': get_your_tips_entry(context).slug
    })
    return context


@register.inclusion_tag(
    'yourtips/your_tips_on_tip_submission_form.html',
    takes_context=True
)
def your_tips_on_tip_submission_form(context):
    context = copy(context)

    most_recent_tip = YourTipsEntry.objects.all(
    ).order_by('-latest_revision_created_at').first()

    context.update({
        'most_recent_tip': most_recent_tip,
        'your_tip_page_slug': get_your_tips_entry(context).slug
    })
    return context


@register.simple_tag(takes_context=True)
def get_your_tips_entry(context):

    return YourTip.objects.first()
