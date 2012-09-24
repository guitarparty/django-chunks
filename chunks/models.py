# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Chunk(models.Model):
    """
    A Chunk is a piece of content associated
    with a unique key that can be inserted into
    any template with the use of a special template
    tag
    """
    key = models.CharField(_(u'Key'), help_text=_(u"A unique name for this chunk of content"), blank=False, max_length=255)
    content = models.TextField(_(u'Content'), blank=True)
    description = models.CharField(_(u'Description'), blank=True, max_length=64, help_text=_(u"Short Description"))
    lang_code = models.CharField(verbose_name=_(u"language"), help_text="Language code, if this chunk is translated. Same format as LANGUAGE_CODE setting, e.g. sv-se, or de-de, etc.", blank=True, max_length=5, default=settings.LANGUAGE_CODE)

    def __unicode__(self):
        return u"%s (%s)" % (self.key, self.lang_code)
