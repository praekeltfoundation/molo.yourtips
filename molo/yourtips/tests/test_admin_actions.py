from molo.core.models import ArticlePage

from molo.yourtips.models import YourTipsEntry
from molo.yourtips.tests.base import BaseYourTipsTestCase


class TestAdminActions(BaseYourTipsTestCase):

    def test_convert_to_article(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        entry = YourTipsEntry.objects.create(
            user=self.user,
            tip_name='Test page 0',
            tip_text='test body',
            terms_or_conditions_approved=True,
            hide_real_name=True
        )

        response = self.client.get(
            '/django-admin/yourtips/yourtipsentry/%d/convert/' %
            entry.id)
        article = ArticlePage.objects.get(title='Test page 0')
        entry = YourTipsEntry.objects.get(pk=entry.pk)
        self.assertEquals(entry.tip_name, article.title)
        self.assertEquals(entry.converted_article_page, article)
        self.assertEquals(article.body.stream_data, [
            {"type": "paragraph", "value": "Written by: Anonymous"},
            {"type": "paragraph", "value": entry.tip_text}
        ])

        self.assertEquals(ArticlePage.objects.all().count(), 1)
        self.assertEquals(
            response['Location'],
            '/admin/pages/%d/move/' % article.id)

        # second time it should redirect to the edit page
        response = self.client.get(
            '/django-admin/yourtips/yourtipsentry/%d/convert/' %
            entry.id)
        self.assertEquals(
            response['Location'],
            '/admin/pages/%d/edit/' % article.id)
        self.assertEquals(ArticlePage.objects.all().count(), 1)
