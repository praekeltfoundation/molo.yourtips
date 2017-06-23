from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, StreamFieldPanel, FieldRowPanel,
    MultiFieldPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from molo.core import constants
from molo.core.blocks import MarkDownBlock
from molo.core.utils import generate_slug
from molo.core.models import (
    ArticlePage, SectionPage, TranslatablePageMixinNotRoutable,
    PreventDeleteMixin, Main, index_pages_after_copy,
)

SectionPage.subpage_types += ['yourtips.YourTips']


class YourTipsIndexPage(Page, PreventDeleteMixin):
    parent_page_types = ['core.Main']
    subpage_types = ['yourtips.YourTips']

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


class YourTips(TranslatablePageMixinNotRoutable, Page):
    parent_page_types = [
        'yourtips.YourTipsIndexPage', 'core.SectionPage'
    ]
    subpage_types = [
        'yourtips.YourTipsTermsAndConditions',
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


YourTips.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('description'),
    ImageChooserPanel('image'),
    StreamFieldPanel('content')
]

YourTips.settings_panels = [
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
        'core.ArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tip_entry',
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


class YourTipsTermsAndConditions(ArticlePage):
    parent_page_types = ['yourtips.YourTips']
    subpage_types = []

    def get_parent_page(self):
        return YourTips.objects.all().ancestor_of(self).last()


YourTipsTermsAndConditions.promote_panels = [
    MultiFieldPanel(
        Page.promote_panels,
        "Common page configuration", "collapsible collapsed")]


class YourTipsThankYou(ArticlePage):
    parent_page_types = ['yourtips.YourTips']
    subpage_types = []

    def get_parent_page(self):
        return YourTips.objects.all().ancestor_of(self).last()


YourTipsThankYou.promote_panels = [
    MultiFieldPanel(
        Page.promote_panels,
        "Common page configuration", "collapsible collapsed")]
