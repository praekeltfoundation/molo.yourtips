import datetime

from molo.yourtips.models import (
    YourTipsPage, YourTipsEntry, YourTipsEntryPage
)
from molo.yourtips.tests.base import BaseYourTipsTestCase
from molo.yourtips.admin import (
    download_as_csv,
    YourTipsEntryAdmin
)


class TestAdminActions(BaseYourTipsTestCase):

    def test_download_as_csv(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        tip_page = YourTipsPage(
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

        response = self.client.get(
            '/django-admin/yourtips/yourtipsentry/%d/convert/' % entry.id
        )
        article = YourTipsEntryPage.objects.get(title='Tip-%s' % entry.id)
        entry = YourTipsEntry.objects.get(pk=entry.pk)
        self.assertEquals(entry.converted_article_page, article)
        self.assertEquals(article.body.stream_data, [
            {"type": "paragraph", "value": entry.tip_text},
            {"type": "paragraph", "value": "By Test"}
        ])

        self.assertEquals(YourTipsEntryPage.objects.all().count(), 1)

        # second time it should redirect to the edit page
        response = self.client.get(
            '/django-admin/yourtips/yourtipsentry/%d/convert/' %
            entry.id)
        self.assertEquals(
            response['Location'],
            '/admin/pages/%d/edit/' % article.id)
        self.assertEquals(YourTipsEntryPage.objects.all().count(), 1)
