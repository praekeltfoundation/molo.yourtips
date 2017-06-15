from django.core.urlresolvers import reverse

from molo.yourtips.tests.base import BaseYourTipsTestCase
from molo.yourtips.models import YourTips


class TestYourTipsViewsTestCase(BaseYourTipsTestCase):

    def test_yourtips_page(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        tip = YourTips(
            title='Test Tip',
            description='This is the description',
            slug='test-tip')
        self.tip_index.add_child(instance=tip)
        tip.save_revision().publish()
        self.tip_index.save()

        response = self.client.get(tip.url)
        self.assertContains(response, 'Test Tip')
        self.assertContains(response, 'This is the description')

    def test_yourtips_thank_you_page(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        tip = YourTips(
            title='Test Tip',
            description='This is the description',
            slug='test-tip')
        self.tip_index.add_child(instance=tip)
        tip.save_revision().publish()

        response = self.client.post(
            reverse('molo.yourtips:tip_entry', args=[tip.slug]), {
                'tip_name': 'This is a story',
                'tip_text': 'The text',
                'terms_or_conditions_approved': 'true'})
        self.assertEqual(
            response['Location'],
            '/yourtips/thankyou/test-tip/')
