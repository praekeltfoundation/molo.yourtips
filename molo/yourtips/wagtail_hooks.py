from daterange_filter.filter import DateRangeFilter
from molo.yourtips.admin import YourTipsAdmin
from molo.yourtips.models import YourTipsEntry, \
    YourTips
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)
from wagtail.contrib.modeladmin.views import IndexView


class DateFilter(DateRangeFilter):
    template = 'admin/yourtips/yourtips_date_range_filter.html'


class YourTipsEntriesModelAdmin(ModelAdmin):
    model = YourTipsEntry
    menu_label = 'Entries'
    menu_icon = 'edit'
    add_to_settings_menu = False
    list_display = ['tip_name', 'user', 'hide_real_name',
                    'submission_date', 'is_read', 'is_shortlisted',
                    '_convert']

    list_filter = [('submission_date', DateFilter), 'is_read',
                   'is_shortlisted']

    search_fields = ('tip_name',)

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


class ModelAdminTipPageTemplate(IndexView):
    def get_template_names(self):
        return 'admin/yourtips/model_admin_tip_page_template.html'


class YourTipsModelAdmin(ModelAdmin, YourTipsAdmin):
    model = YourTips
    menu_label = 'Your Tip'
    menu_icon = 'doc-full'
    index_view_class = ModelAdminTipPageTemplate
    add_to_settings_menu = False
    list_display = ['title', 'status']

    search_fields = ('tip_name',)

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