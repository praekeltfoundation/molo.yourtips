from daterange_filter.filter import DateRangeFilter

from django.template.defaultfilters import truncatechars

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)
from wagtail.contrib.modeladmin.views import IndexView

from molo.yourtips.admin import YourTipsPageAdmin
from molo.yourtips.models import YourTipsEntry, \
    YourTipsPage


class DateFilter(DateRangeFilter):
    template = 'admin/yourtips/yourtips_date_range_filter.html'


class YourTipsEntriesModelAdmin(ModelAdmin):
    model = YourTipsEntry
    menu_label = 'Entries'
    menu_icon = 'edit'
    add_to_settings_menu = False
    list_display = [
        'tip', 'submission_date', 'user', 'optional_name',
        'allow_share_on_social_media', '_convert'
    ]
    list_filter = [('submission_date', DateFilter)]

    def _convert(self, obj, *args, **kwargs):
        if obj.converted_article_page:
            return (
                '<a href="/admin/pages/%d/edit/">Article Page</a>' %
                obj.converted_article_page.id)
        return (
            '<a href="/django-admin/yourtips/yourtipsentry'
            '/%d/convert/" class="addlink">Convert to article</a>' %
            obj.id)

    _convert.allow_tags = True
    _convert.short_description = ''

    def tip(self, obj, *args, **kwargs):
        return truncatechars(obj.tip_text, 30)


class ModelAdminTipPageTemplate(IndexView):
    def get_template_names(self):
        return 'admin/yourtips/model_admin_tip_page_template.html'


class YourTipsModelAdmin(ModelAdmin, YourTipsPageAdmin):
    model = YourTipsPage
    menu_label = 'Your Tips Page'
    menu_icon = 'doc-full'
    index_view_class = ModelAdminTipPageTemplate
    add_to_settings_menu = False
    list_display = ['title', 'status']

    def get_queryset(self, request):
        qs = super(YourTipsModelAdmin, self).get_queryset(request)
        main = request.site.root_page
        return qs.descendant_of(main)


class YourTipsAdminGroup(ModelAdminGroup):
    menu_label = 'YourTips'
    menu_icon = 'folder-open-inverse'
    menu_order = 400
    items = (YourTipsEntriesModelAdmin, YourTipsModelAdmin)


modeladmin_register(YourTipsAdminGroup)
