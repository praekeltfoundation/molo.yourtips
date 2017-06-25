from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, StreamFieldPanel, FieldRowPanel,
    MultiFieldPanel, InlinePanel
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from molo.core import constants
from molo.core.blocks import MarkDownBlock
from molo.core.utils import generate_slug
from molo.core.models import (
    ArticlePage, SectionPage, TranslatablePageMixinNotRoutable,
    PreventDeleteMixin, Main, index_pages_after_copy,
)

SectionPage.subpage_types += [
    'yourtips.YourTips', 'yourtips.YourTipsIndexPage',
    'yourtips.YourTipsArticleIndexPage'
]


class YourTipsIndexPage(Page, PreventDeleteMixin):
    parent_page_types = ['core.Main']
    subpage_types = ['yourtips.YourTips', 'yourtips.YourTipsArticleIndexPage']

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
    parent_page_types = ['yourtips.YourTipsIndexPage', 'core.SectionPage']
    subpage_types = []

    def copy(self, *args, **kwargs):
        YourTipsArticleIndexPage.objects.child_of(YourTipsIndexPage).delete()
        super(YourTipsArticleIndexPage, self).copy(*args, **kwargs)

    @staticmethod
    def latest_articles():
        return YourTipsEntryPage.objects.filter(
            featured_in_homepage=True,
            languages__language__is_main_language=True).exclude(
            demote_date__gt=timezone.now()).order_by(
            '-featured_in_latest_start_date',
            '-promote_date', '-latest_revision_created_at').specific()


@receiver(index_pages_after_copy, sender=Main)
def create_yourtips_article_index_page(sender, instance, **kwargs):
    if not instance.get_children().filter(
            title='Read Tips').exists:
        yourtips_tip_article_page_index = YourTipsArticleIndexPage(
            title='Read Tips', slug=('read-tips-%s' % (
                generate_slug(instance.title), )))
        instance.add_child(instance=yourtips_tip_article_page_index)
        yourtips_tip_article_page_index.save_revision().publish()


class YourTipsPage(TranslatablePageMixinNotRoutable, Page):
    parent_page_types = [
        'yourtips.YourTipsIndexPage', 'core.SectionPage'
    ]
    subpage_types = [
        'yourtips.YourTipsThankYou'
    ]
    description = models.TextField(null=True, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', MarkDownBlock()),
        ('image', ImageChooserBlock()),
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

    def get_effective_extra_style_hints(self):
            return self.extra_style_hints

    def get_effective_image(self):
        return self.image

    def thank_you_page(self):
        qs = YourTipsThankYou.objects.live().child_of(self)
        if qs.exists():
            return qs.last()
        return None

    class Meta:
        verbose_name = 'YourTip'
        verbose_name_plural = 'YourTips'


YourTipsPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('description'),
    ImageChooserPanel('image'),
    StreamFieldPanel('content')
]

YourTipsPage.settings_panels = [
    MultiFieldPanel(
        [FieldRowPanel(
            [FieldPanel('extra_style_hints')], classname="label-above")],
        "Meta")
]


class YourTipsEntry(models.Model):
    submission_date = models.DateField(null=True, blank=True,
                                       auto_now_add=True)
    user_name = models.CharField(null=True, blank=True, max_length=30)
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
        FieldPanel('featured_in_latest_start_date'),
        FieldPanel('featured_in_latest_end_date'),
    ]

    def get_parent_page(self):
        return YourTipsArticleIndexPage.objects.all().ancestor_of(self).last()


YourTipsEntryPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('subtitle'),
    ImageChooserPanel('image'),
    StreamFieldPanel('body'),
    FieldPanel('tags'),
    MultiFieldPanel(
        [
            FieldPanel('commenting_state'),
            FieldPanel('commenting_open_time'),
            FieldPanel('commenting_close_time'),
        ],
        heading="Commenting Settings", ),
    MultiFieldPanel(
        [
            FieldPanel('social_media_title'),
            FieldPanel('social_media_description'),
            ImageChooserPanel('social_media_image'),
        ],
        heading="Social Media", ),
    InlinePanel('nav_tags', label="Tags for Navigation"),
    InlinePanel('reaction_questions', label="Reaction Questions"),
    InlinePanel('recommended_articles', label="Recommended articles"),
    InlinePanel('related_sections', label="Related Sections"),
]

YourTipsEntryPage.promote_panels = [
    MultiFieldPanel(
        ArticlePage.featured_latest_promote_panels, "Featuring in Latest"),
    MultiFieldPanel(
        ArticlePage.featured_section_promote_panels, "Featuring in Section"),
    MultiFieldPanel(
        YourTipsEntryPage.featured_homepage_promote_panels, "Featuring in Homepage"),
    MultiFieldPanel(ArticlePage.topic_of_the_day_panels, "Topic of the Day"),
    MultiFieldPanel(ArticlePage.metedata_promote_panels, "Metadata"),
    MultiFieldPanel(
        Page.promote_panels,
        "Common page configuration", "collapsible collapsed")
]


class YourTipsTermsAndConditions(ArticlePage):
    parent_page_types = ['yourtips.YourTips']
    subpage_types = []

    def get_parent_page(self):
        return YourTipsPage.objects.all().ancestor_of(self).last()


YourTipsTermsAndConditions.promote_panels = [
    MultiFieldPanel(
        Page.promote_panels,
        "Common page configuration", "collapsible collapsed")]


class YourTipsThankYou(ArticlePage):
    parent_page_types = ['yourtips.YourTips']
    subpage_types = []

    def get_parent_page(self):
        return YourTipsPage.objects.all().ancestor_of(self).last()


YourTipsThankYou.promote_panels = [
    MultiFieldPanel(
        Page.promote_panels,
        "Common page configuration", "collapsible collapsed")]
