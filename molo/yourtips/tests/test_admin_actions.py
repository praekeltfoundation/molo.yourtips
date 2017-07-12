import datetime

from molo.yourtips.models import (
    YourTip, YourTipsEntry, YourTipsArticlePage
)
from molo.yourtips.tests.base import BaseYourTipsTestCase
from molo.yourtips.admin import (
    download_as_csv,
    YourTipsEntryAdmin,
    YourTipsArticlePageAdmin
)


class TestAdminActions(BaseYourTipsTestCase):
    def test_download_tip_entries_as_csv(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        tip_page = YourTip(
            title='Test Tip',
            description='This is the description',
            slug='test-tip')
        self.tip_index.add_child(instance=tip_page)
        tip_page.save_revision().publish()

        YourTipsEntry.objects.create(
            optional_name='Test',
            tip_text='test body',
            allow_share_on_social_media=True,
        )

        response = download_as_csv(YourTipsEntryAdmin,
                                   None,
                                   YourTipsEntry.objects.all())
        date = str(datetime.datetime.now().date())
        expected_output = ('Content-Type: text/csv\r\nContent-Disposition:'
                           ' attachment;filename=export.csv\r\n\r\nid,'
                           'submission_date,optional_name,user,tip_text,'
                           'allow_share_on_social_media,'
                           'converted_article_page\r\n1,' +
                           date + ',Test,,test body,True,\r\n')
        self.assertEquals(str(response), expected_output)

    def test_download_article_page_as_csv(self):
            self.client.login(
                username=self.superuser_name,
                password=self.superuser_password
            )

            tip_page = YourTip(
                title='Test Tip',
                description='This is the description',
                slug='test-tip')
            self.tip_index.add_child(instance=tip_page)
            tip_page.save_revision().publish()

            entry = YourTipsEntry.objects.create(
                optional_name='Test',
                tip_text='test body',
                allow_share_on_social_media=True,
            )
            self.client.get(
                '/django-admin/yourtips/yourtipsentry/%d/convert/' % entry.id
            )

            converted_tip = YourTipsArticlePage.objects.first()
            converted_tip_time = converted_tip.latest_revision_created_at.\
                strftime("%Y-%m-%d %X.%f+00:00")

            response = download_as_csv(YourTipsArticlePageAdmin,
                                       None,
                                       YourTipsArticlePage.objects.all())
            out = ('Content-Type: text/csv\r\nContent-Disposition:'
                   ' attachment;filename=export.csv\r\n\r\nid,path,'
                   'depth,numchild,title,slug,content_type,live,'
                   'has_unpublished_changes,url_path,owner,seo_title,'
                   'show_in_menus,search_description,go_live_at,expire_at'
                   ',expired,locked,first_published_at,'
                   'latest_revision_created_at,page_ptr,subtitle,'
                   'uuid,featured_in_latest,featured_in_latest_start_date,'
                   'featured_in_latest_end_date,featured_in_section,'
                   'featured_in_section_start_date,'
                   'featured_in_section_end_date,featured_in_homepage,'
                   'featured_in_homepage_start_date,'
                   'featured_in_homepage_end_date,image,social_media_title,'
                   'social_media_description,social_media_image,body,'
                   'commenting_state,commenting_open_time,'
                   'commenting_close_time,feature_as_topic_of_the_day,'
                   'promote_date,demote_date,articlepage_ptr\r\n'
                   '22,00010001000800010001,5,0,Tip-1,yourtips-entry-1,'
                   'your tips article page,False,True,'
                   '/main/your-tips/read-tips/yourtips-entry-1/,,,'
                   'False,,,,False,False,,' + converted_tip_time +
                   ',Tip-1,,,False,,,False,,,False,,,,,,,'
                   '"<div class=""block-paragraph""><p>test body</p></div>'
                   '\n<div class=""block-heading"">By Test</div>",,,,False,'
                   ',,Tip-1\r\n')
            self.assertEquals(str(response), out)

    def test_convert_to_article(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        entry = YourTipsEntry.objects.create(
            optional_name='Test',
            tip_text='test body',
            allow_share_on_social_media=True,
        )

        self.client.get(
            '/django-admin/yourtips/yourtipsentry/%d/convert/' % entry.id
        )
        article = YourTipsArticlePage.objects.get(title='Tip-%s' % entry.id)
        entry = YourTipsEntry.objects.get(pk=entry.pk)
        self.assertEquals(entry.converted_article_page, article)
        self.assertEquals(article.body.stream_data, [
            {"type": "paragraph", "value": entry.tip_text},
            {"type": "heading", "value": "By Test"}
        ])

        self.assertEquals(YourTipsArticlePage.objects.all().count(), 1)

        # second time it should redirect to the edit page
        response = self.client.get(
            '/django-admin/yourtips/yourtipsentry/%d/convert/' %
            entry.id)
        self.assertEquals(
            response['Location'],
            '/admin/pages/%d/edit/' % article.id)
        self.assertEquals(YourTipsArticlePage.objects.all().count(), 1)
