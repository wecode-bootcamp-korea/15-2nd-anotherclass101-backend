from django.db      import models
from product.models import Course
from user.models    import User
class Tag(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'tags'
    def __str__(self):
        return self.name


class RequestFormStatus(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'request_form_status'
    def __str__(self):
        return self.name


class CourseRequest(models.Model):
    cover_photo         = models.URLField(max_length=2000, default='https://ac101-image.s3.us-east-2.amazonaws.com/add-photo-portrait.png', null=True)
    thumbnail           = models.URLField(max_length=2000, default='https://ac101-image.s3.us-east-2.amazonaws.com/add-photo-portrait.png', null=True)
    summary_photo       = models.URLField(max_length=2000, default='https://ac101-image.s3.us-east-2.amazonaws.com/add-photo-portrait.png', null=True)
    specific_category   = models.CharField(max_length=150, null=True)
    expiry_date         = models.DateTimeField(null=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    course              = models.ForeignKey(Course, on_delete=models.CASCADE)
    tag                 = models.ManyToManyField(Tag)
    liker               = models.ManyToManyField(User, related_name='liked_requests')
    form_status         = models.ManyToManyField(RequestFormStatus)
    
    class Meta:
        db_table = 'course_requests'
    def __str__(self):
        return self.name


class RequestCard(models.Model):
    request  = models.ForeignKey(CourseRequest, on_delete=models.CASCADE)
    photo    = models.URLField(max_length=2000, default='https://ac101-image.s3.us-east-2.amazonaws.com/add-photo-portrait.png', null=True)
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
