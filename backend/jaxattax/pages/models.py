from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    template = 'layouts/pages/home.html'


@register_setting(icon="link")
class SocialMedia(BaseSetting):
    twitter_handle = models.CharField(null=True, max_length=30)
    facebook_url = models.URLField(null=True)
    tiktok_url = models.URLField(null=True)

    @property
    def twitter_url(self):
        return 'https://twitter.com/' + self.twitter_handle
