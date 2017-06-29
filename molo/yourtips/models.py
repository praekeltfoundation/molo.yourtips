from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from secretballot import enable_voting_on

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, StreamFieldPanel, FieldRowPanel,
    MultiFieldPanel
)

from molo.core import constants
from molo.core.blocks import MarkDownBlock
from molo.core.utils import generate_slug
from molo.core.models import (
    ArticlePage, TranslatablePageMixinNotRoutable,
    PreventDeleteMixin, Main, index_pages_after_copy,
)


class YourTipsIndexPage(Page, PreventDeleteMixin):
    parent_page_types = ['core.Main']
    subpage_types = [
        'yourtips.YourTipsPage', 'yourtips.YourTipsArticleIndexPage'
    ]

    def copy(self, *args, **kwargs):
        site = kwargs['to'].get_site()
        main = site.root_page
        YourTipsIndexPage.objects.child_of(main).delete()
        super(YourTipsIndexPage, self).copy(*args, **kwargs)

    @staticmethod
    def get_effective_commenting_settings(self):
        commenting_settings = dict()
        commenting_settings['state'] = constants.COMMENTING_DISABLED
        return commenting_settings


@receiver(index_pages_after_copy, sender=Main)
def create_yourtips_index_page(sender, instance, **kwargs):
    if not instance.get_children().filter(
            title='Your tips').exists:
        yourtips_tip_page_index = YourTipsIndexPage(
            title='Your tips', slug=('yourtips-%s' % (
                generate_slug(instance.title), )))
        instance.add_child(instance=yourtips_tip_page_index)
        yourtips_tip_page_index.save_revision().publish()


class YourTipsArticleIndexPage(Page, PreventDeleteMixin):
    parent_page_types = ['yourtips.YourTipsIndexPage']
    subpage_types = []

    def copy(self, *args, **kwargs):
        YourTipsArticleIndexPage.objects.child_of(YourTipsIndexPage).delete()
        super(YourTipsArticleIndexPage, self).copy(*args, **kwargs)


@receiver(index_pages_after_copy, sender=Main)
def create_yourtips_article_index_page(sender, instance, **kwargs):
    if not instance.get_children().filter(
            title='Tips').exists:
        yourtips_tip_article_page_index = YourTipsArticleIndexPage(
            title='Tips', slug=('tips-%s' % (
                generate_slug(instance.title), )))
        instance.add_child(instance=yourtips_tip_article_page_index)
        yourtips_tip_article_page_index.save_revision().publish()


class YourTipsPage(TranslatablePageMixinNotRoutable, Page):
    parent_page_types = [
        'yourtips.YourTipsIndexPage'
    ]
    description = models.TextField(null=True, blank=True)

    content = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', MarkDownBlock()),
        ('list', blocks.ListBlock(blocks.CharBlock(label="Item"))),
        ('numbered_list', blocks.ListBlock(blocks.CharBlock(label="Item"))),
        ('page', blocks.PageChooserBlock()),
    ], null=True, blank=True)

    extra_style_hints = models.TextField(
        default='',
        null=True, blank=True,
        help_text=_(
            "Styling options that can be applied to this section "
            "and all its descendants"))

    homepage_action_copy = models.CharField(
        default='Do you have advice you can share with other youth on relationships?',
        max_length=255)

    def get_effective_extra_style_hints(self):
            return self.extra_style_hints

    class Meta:
        verbose_name = 'YourTip'
        verbose_name_plural = 'YourTips'


YourTipsPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('description'),
    StreamFieldPanel('content')
]

YourTipsPage.settings_panels = [
    MultiFieldPanel(
        [FieldRowPanel(
            [FieldPanel('extra_style_hints'),
             FieldPanel('homepage_action_copy')
             ], classname="label-above")
        ],
        "Meta")
]


class YourTipsEntry(models.Model):
    submission_date = models.DateField(null=True, blank=True,
                                       auto_now_add=True)
    optional_name = models.CharField(null=True, blank=True, max_length=30)
    user = models.ForeignKey('auth.User', blank=True, null=True)
    tip_text = models.CharField(max_length=140)
    allow_share_on_social_media = models.BooleanField()

    converted_article_page = models.ForeignKey(
        'yourtips.YourTipsEntryPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tip_entries',
        help_text=_('Article page to which the entry was converted to')
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('tip_text')
            ],
            heading="Entry Settings",)
    ]

    class Meta:
        verbose_name = 'YourTips Entry'
        verbose_name_plural = 'YourTips Entries'


class YourTipsEntryPage(ArticlePage):
    parent_page_types = ['yourtips.YourTipsArticleIndexPage']
    subpage_types = []

    featured_homepage_promote_panels = [
        FieldPanel('featured_in_homepage'),
        FieldPanel('featured_in_homepage_start_date'),
        FieldPanel('featured_in_homepage_end_date'),
    ]


YourTipsEntryPage.promote_panels = [
    MultiFieldPanel(
        YourTipsEntryPage.featured_homepage_promote_panels,
        "Featuring in Homepage"
    ),
    MultiFieldPanel(ArticlePage.topic_of_the_day_panels, "Topic of the Day"),
]
enable_voting_on(YourTipsEntryPage)
