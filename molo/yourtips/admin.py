import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
from django.conf.urls import patterns
from django.template.defaultfilters import truncatechars
from django.shortcuts import get_object_or_404, redirect

from wagtail.wagtailcore.utils import cautious_slugify

from molo.core.models import ArticlePage
from molo.yourtips.models import (YourTipsEntry,
                                   YourTips,
                                   YourTipsIndexPage)


@staff_member_required
def convert_to_article(request, entry_id):
    def get_entry_author(entry):
        written_by_user = 'Written by: %s' % entry.user.username
        written_by_anon = 'Written by: Anonymous'
        if entry.hide_real_name:
            return written_by_anon
        return written_by_user

    entry = get_object_or_404(YourTipsEntry, pk=entry_id)
    if not entry.converted_article_page:
        tip_page_index_page = (
            YourTipsIndexPage.objects.live().first())
        article = ArticlePage(
            title=entry.tip_name,
            slug='yourtips-entry-%s' % cautious_slugify(entry.tip_name),
            body=json.dumps([
                {"type": "paragraph", "value": get_entry_author(entry)},
                {"type": "paragraph", "value": entry.tip_text}
            ])
        )
        tip_page_index_page.add_child(instance=article)
        article.save_revision()
        article.unpublish()

        entry.converted_article_page = article
        entry.save()
        return redirect('/admin/pages/%d/move/' % article.id)
    return redirect('/admin/pages/%d/edit/' % entry.converted_article_page.id)


class YourTipsEntryForm(forms.ModelForm):

    class Meta:
        model = YourTipsEntry
        fields = ['tip_name', 'tip_text', 'user', 'hide_real_name',
                  'is_read', 'is_shortlisted']


class YourTipsEntryAdmin(admin.ModelAdmin):
    list_display = ['tip_name', 'truncate_text', 'user', 'hide_real_name',
                    'submission_date', 'is_read', 'is_shortlisted',
                    '_convert']
    list_filter = ['is_read', 'is_shortlisted',
                   'submission_date']
    list_editable = ['is_read', 'is_shortlisted']
    date_hierarchy = 'submission_date'
    form = YourTipsEntryForm
    readonly_fields = ('tip_name', 'tip_text', 'user',
                       'hide_real_name', 'submission_date')

    def truncate_text(self, obj, *args, **kwargs):
        return truncatechars(obj.tip_text, 30)

    def get_urls(self):
        urls = super(YourTipsEntryAdmin, self).get_urls()
        entry_urls = patterns(
            '', (r'^(?P<entry_id>\d+)/convert/$', convert_to_article)
        )
        return entry_urls + urls

    def _convert(self, obj, *args, **kwargs):
        if obj.converted_article_page:
            return (
                '<a href="/admin/pages/%d/edit/">Article Page</a>' %
                obj.converted_article_page.id)
        return (
            ' <a href="%d/convert/" class="addlink">Convert to article</a>' %
            obj.id)

    _convert.allow_tags = True
    _convert.short_description = ''


class YourTipsAdmin(admin.ModelAdmin):
    list_display = ['status']
    list_filter = ['title']
    search_fields = ['title', 'content', 'description']

    def status(self, obj, *args, **kwargs):
        if obj.live:
            return 'First published on ' + str(obj.first_published_at.date())
        return 'Unpublished'


admin.site.register(YourTipsEntry, YourTipsEntryAdmin)
admin.site.register(YourTips, YourTipsAdmin)
