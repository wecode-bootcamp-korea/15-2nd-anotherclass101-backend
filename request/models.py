from django.db      import models
from product.models import Course, SubCategory
from user.models    import User


class Tag(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'tags'
    def __str__(self):
        return self.name


class CourseRequest(models.Model):
    name                = models.CharField(max_length=20)
    cover_photo         = models.URLField()
    thumbnail           = models.URLField()
    creator_description = models.CharField(max_length=150)
    summary_photo       = models.URLField()
    specific_category   = models.CharField(max_length=150)
    sub_category        = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    expiry_date         = models.DateTimeField()
    created_at          = models.DateTimeField(auto_now_add=True)
    course              = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    tag                 = models.ManyToManyField(Tag)
    liker               = models.ManyToManyField(User, related_name='liked_requests')

    class Meta:
        db_table = 'course_requests'
    def __str__(self):
        return self.name


class RequestCard(models.Model):
    request  = models.ForeignKey(CourseRequest, on_delete=models.CASCADE)
    photo    = models.URLField()
    description = models.CharField(max_length=150)

    class Meta:
        db_table = 'request_cards'


class Support(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(CourseRequest, on_delete=models.CASCADE)

    class Meta:
        db_table = 'supports'


class RequestCurriculum(models.Model):
    name    = models.CharField(max_length=50)
    request = models.ForeignKey(CourseRequest, on_delete=models.CASCADE)
    voter   = models.ManyToManyField(User, related_name='request_votes')

    class Meta:
        db_table = 'request_curriculums'
    def __str__(self):
        return self.name
