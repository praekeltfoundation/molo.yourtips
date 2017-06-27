from django.core.urlresolvers import reverse

from molo.yourtips.tests.base import BaseYourTipsTestCase
from molo.yourtips.models import (
    YourTipsPage, YourTipsEntry, YourTipsEntryPage
)


class TestYourTipsViewsTestCase(BaseYourTipsTestCase):

    def test_yourtips_page(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        tip = YourTipsPage(
            title='Your Tips Page',
            description='Your Tips page description',
            slug='your-tips-page')
        self.tip_index.add_child(instance=tip)
        tip.save_revision().publish()
        self.tip_index.save()

        response = self.client.get(tip.url)
        self.assertContains(response, 'Your Tips Page')

    def test_yourtips_thank_you_page(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        tip = YourTipsPage(
            title='Test Tip',
            description='This is the description',
            slug='test-tip')
        self.tip_index.add_child(instance=tip)
        tip.save_revision().publish()

        response = self.client.post(
            reverse('molo.yourtips:tip_entry', args=[tip.slug]), {
                'tip_text': 'The text',
                'allow_share_on_social_media': 'true'})
        self.assertEqual(
            response['Location'],
            '/yourtips/thankyou/test-tip/')

    def test_yourtips_recent_tip_view(self):
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
        article = YourTipsEntryPage.objects.get(title='Tip-%s' % entry.id)
        article.save_revision().publish()

        response = self.client.get(reverse('molo.yourtips:recent_tips'))
        self.assertContains(response, 'Test')
        self.assertContains(response, 'test body')
