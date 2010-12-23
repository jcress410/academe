from datetime import datetime

from django.db import models
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.sitemaps import ping_google
from django.contrib.comments.moderation import CommentModerator, moderator
from django.db.models import permalink

from tagging.models import Tag, TaggedItem
from tagging.fields import TagField

import settings

from managers import PostManager, PublishedPostManager, PostImageManager

__doc__="""

Significant portions of this file are copy-pasted from blogYall
http://www.davisd.com/django-blogyall/

often with slight modification. License information at the bottom of this
file
"""


class Series(models.Model):
    """
    Series of Posts
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)
    preface = models.TextField(blank=True)
    created_on = models.DateTimeField(default=datetime.now)

    @permalink
    def get_absolute_url(self):
        return ('blog.views.series_detail', [self.slug, ])

    class Meta:
        ordering = ('-created_on',)
        verbose_name_plural = 'series'

    def __unicode__(self):
        return unicode(self.title)


class Category(models.Model):
    """
    Category
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)

    @permalink
    def get_absolute_url(self):
        return ('blog.views.category_detail', [self.slug, ])

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return unicode(self.title)


class Post(models.Model):
    """
    Class defining a blog post
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique_for_date='publish_date')
    author = models.ForeignKey(User)
    publish_date = models.DateTimeField(default=datetime.now)
    last_modified = models.DateTimeField(default=datetime.now)
    is_published = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True,
        related_name='posts')
    series = models.ForeignKey(Series, blank=True, null=True,
        related_name='posts')
    tags = TagField()
    meta_keywords = models.CharField(max_length=255, blank=True)
    summary = models.TextField(
        help_text='Also doubles as the meta description')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    comments = generic.GenericRelation(Comment, object_id_field="object_pk")

    @permalink
    def get_absolute_url(self):
        return ('blog.views.post_detail', [
            '%04d' % self.publish_date.year,
            '%02d' % self.publish_date.month,
            '%02d' % self.publish_date.day,
            self.slug, ])

    objects = PostManager()
    published = PublishedPostManager()

    def save(self, *args, **kwargs):
        if (
            getattr(settings, 'BLOG_PING_GOOGLE', False) == True) \
            and (getattr(settings, 'DEBUG', True) == False):
            if self.is_published \
                and self.publish_date <= datetime.now():
                if not self.pk:
                    try:
                        ping_google()
                    except:
                        pass
                else:
                    old_post = Post.objects.get(pk=self.pk)
                    if old_post.is_published == False:
                        try:
                            ping_google()
                        except:
                            pass
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-publish_date',)
        get_latest_by = 'publish_date'

    def __unicode__(self):
        if self.is_published:
            return self.title
        else:
            return '%s (DRAFT)' % (self.title,)

    @property
    def post_categories_string(self):
        """
        Return the post categories in string format
        """
        return ', '.join([c.title for c in self.categories.all()])

    def get_previous_post(self):
        """
        Get the previous post by publish_date
        """
        return self.get_previous_by_publish_date(is_published=True,
            publish_date__lt=datetime.now)

    def get_next_post(self):
        """
        Get the next post by publish_date
        """
        return self.get_next_by_publish_date(is_published=True,
            publish_date__lt=datetime.now)


class PublishedPost(Post):
    """
    Published Post Proxy model
    """
    objects = PublishedPostManager()

    class Meta:
        proxy = True


class PostImage(models.Model):
    """
    Blog Post Image
    """
    post = models.ForeignKey(Post, related_name="images")
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    image = models.ImageField(upload_to="apps/blogyall/images")
    gallery_position = models.PositiveIntegerField(blank=True, null=True,
        help_text="Post Images without a Gallery Position will not appear"\
                "in the post's gallery images")

    objects = PostImageManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('post', 'gallery_position', 'title',)


class PostModerator(CommentModerator):
    """
    Blog post comment moderator
    """
    enable_field='allow_comments'
    email_notification = getattr(settings,
            'BLOG_COMMENTS_EMAIL_NOTIFICATION', False)
    if getattr(settings, 'BLOG_COMMENTS_AUTO_MODERATE', False):
        auto_moderate_field='publish_date'
        moderate_after=getattr(settings, 'BLOG_COMMENTS_MODERATE_AFTER', None)
    if getattr(settings, 'BLOG_COMMENTS_AUTO_CLOSE', False):
        auto_close_field='publish_date'
        close_after=getattr(settings, 'BLOG_COMMENTS_CLOSE_AFTER', None)

moderator.register(Post, PostModerator)

"""
Copyright (c) 2010, David Davis <davisd@davisd.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.
* Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
