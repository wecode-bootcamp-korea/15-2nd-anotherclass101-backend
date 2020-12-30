from django.db import models

from user.models import User
from product.models import Course


class Story(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    course     = models.ForeignKey(Course, on_delete=models.CASCADE)
    body       = models.CharField(max_length=150)
    image_url  = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liker      = models.ManyToManyField(User, through='StoryLike', related_name='liked_stories')

    class Meta:
        db_table = 'stories'


class StoryLike(models.Model):
    story      = models.ForeignKey(Story, on_delete=models.CASCADE)
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'story_likes'


class StoryComment(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    story      = models.ForeignKey(Story, on_delete=models.CASCADE)
    body       = models.CharField(max_length=150)
    image_url  = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'story_comments'


class CourseCommunity(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    course     = models.ForeignKey(Course, on_delete=models.CASCADE)
    body       = models.CharField(max_length=150)
    image_url  = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liker      = models.ManyToManyField(User, through='CourseCommunityLike', related_name='liked_communities')

    class Meta:
        db_table = 'course_communities'


class CourseCommunityLike(models.Model):
    community  = models.ForeignKey(CourseCommunity, on_delete=models.CASCADE)
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'course_community_likes'


class CourseCommunityComment(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    post       = models.ForeignKey(CourseCommunity, on_delete=models.CASCADE)
    body       = models.CharField(max_length=150)
    image_url  = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'course_community_comments'
