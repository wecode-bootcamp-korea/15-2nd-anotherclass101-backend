from django.db import models

from user.models import User
from product.models import Course

class CourseCurriculum(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order  = models.IntegerField()
    name   = models.CharField(max_length=40)

    class Meta:
        db_table = 'course_curriculums'


class CourseSubCurriculum(models.Model):
    name       = models.CharField(max_length=40)
    order      = models.IntegerField()
    video      = models.URLField()
    note       = models.CharField(max_length=150)
    curriculum = models.ForeignKey(CourseCurriculum, on_delete=models.CASCADE)

    class Meta:
        db_table = 'course_sub_curriculums'


class SubCurriculumComment(models.Model):
    sub_curriculum = models.ForeignKey(CourseSubCurriculum, on_delete=models.CASCADE)
    user           = models.ForeignKey(User,on_delete=models.CASCADE)
    body           = models.CharField(max_length=150)
    image_url      = models.URLField(null=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sub_curriculum_comments'


class SubCurriculumCommentReply(models.Model):
    comment    = models.ForeignKey(SubCurriculumComment,on_delete=models.CASCADE)
    user       = models.ForeignKey(User,on_delete=models.CASCADE)
    body       = models.CharField(max_length=150)
    image_url  = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sub_curriculum_comment_replies'
