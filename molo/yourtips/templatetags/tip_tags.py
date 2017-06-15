from django import template
from molo.yourtips.models import YourTipsThankYou
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
