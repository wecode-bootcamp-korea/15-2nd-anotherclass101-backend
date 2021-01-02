from random import randint

import json
import jwt
import bcrypt

from io import BytesIO
from PIL import Image as img

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import JsonResponse
from django.test import TestCase, Client

from .models import CourseRequest, Tag, RequestCard, RequestCurriculum
from .views import RequestView, RequestBasicInfoView, RequestTitleView
from product.models import Product, Course, Category, SubCategory, CourseStatus, CourseLevel
from user.models import User, Creator, UserGrade, ApplyPath

from my_settings import SECRET, ALGORITHM


class RequestTest(TestCase):
    def setUp(self):
        UserGrade.objects.create(
                id = 1,
                name = '1',
                description = '1',
        )

        User.objects.create(
                id          = 1,
                name        = 'requesttest',
                email       = 'test@test.com',
                grade_id    = 1
        )
        ApplyPath.objects.create(
                id     = 1,
                reason = 'test',
        )
        Creator.objects.create(
                id    = 1,
                user_id  =1,
                apply_path_id = 1,
                information = 'test',
        )
        CourseStatus.objects.create(
                id   = 4,
                name = '1'
        )
        Category.objects.create(
                id   = 1,
                name = 'test_category',
        )
        SubCategory.objects.create(
                id   = 1,
                name = 'test_sub_category',
                category_id = 1,
        )
        CourseLevel.objects.create(
                id   = 1,
                name = 'test_level',
        )

        self.token = jwt.encode({'user_id': User.objects.get(name='requesttest').id}, SECRET, algorithm=ALGORITHM)

    def tearDown(self):
        User.objects.all().delete
        UserGrade.objects.all().delete
        ApplyPath.objects.all().delete
        Creator.objects.all().delete
        CourseStatus.objects.all().delete
        Product.objects.all().delete
        Course.objects.all().delete
        CourseRequest.objects.all().delete

    def test_requset_create_read(self):
        client = Client()
        header = {"HTTP_Authorization": self.token}
        token  = header['HTTP_Authorization']
        payload = jwt.decode(token, SECRET, algorithms = ALGORITHM)
        user   = User.objects.get(id = payload['user_id'])

        response = client.post('/request/main', **header, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

        response = client.get('/request/main', **header, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': [{'id': 2, 'thumbnail': 'https://ac101-image.s3.us-east-2.amazonaws.com/add-photo-portrait.png', 'name': None, 'status': '1'}]})


class RequestBasicTest(TestCase):
    def setUp(self):
        UserGrade.objects.create(
                id = 1,
                name = '1',
                description = '1',
        )
        User.objects.create(
                id          = 1,
                name        = 'requesttest',
                email       = 'test@test.com',
                grade_id    = 1,
                nickname    = 'test_1nickname'
        )
        ApplyPath.objects.create(
                id     = 1,
                reason = 'test',
        )
        Creator.objects.create(
                id    = 1,
                user_id  = 1,
                apply_path_id = 1,
                information = 'test',
        )
        CourseStatus.objects.create(
                id   = 4,
                name = '1'
        )
        CourseLevel.objects.create(
                id   = 1,
                name = 'test_level',
        )
        Category.objects.create(
                id   = 1,
                name = 'test_category',
        )
        SubCategory.objects.create(
                id   = 1,
                name = 'test_sub_category',
                category_id = 1,
        )
        Product.objects.create(
                id   = 1,
                creator_id = 1
        )
        Course.objects.create(
                id   = 1,
                course_status_id = 4,
                product_id = 1,
        )
        CourseRequest.objects.create(
                id   = 1,
                course_id = 1
        )
        self.token = jwt.encode({'user_id': User.objects.get(name='requesttest').id}, SECRET, algorithm=ALGORITHM)


    def tearDown(self):
        User.objects.all().delete
        UserGrade.objects.all().delete
        ApplyPath.objects.all().delete
        Creator.objects.all().delete
        CourseStatus.objects.all().delete
        Product.objects.all().delete
        Course.objects.all().delete
        CourseRequest.objects.all().delete
        CourseLevel.objects.all().delete
        Category.objects.all().delete
        SubCategory.objects.all().delete

    def test_basic_update_read(self):
        data = {
            'nickname'       : 'test_nickname',
            'category'       : 1,
            'sub_category'   : 'test_sub_category',
            'category_detail': 'test_specific',
            'level'          : 'test_level',
        }
        client  = Client()
        header  = {"HTTP_Authorization": self.token}
        token   = header['HTTP_Authorization']
        payload = jwt.decode(token, SECRET, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['user_id'])
      
        response = client.post('/request/basicinfo', data,  **header, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

        response = client.get('/request/basicinfo', **header, content_type='application/json')
        self.assertEqual(response.status_code, 200)


class RequestTitleTest(TestCase):
    def setUp(self):
        UserGrade.objects.create(
                id = 1,
                name = '1',
                description = '1',
        )
        User.objects.create(
                id          = 1,
                name        = 'requesttest',
                email       = 'test@test.com',
                grade_id    = 1
        )
        ApplyPath.objects.create(
                id     = 1,
                reason = 'test',
        )
        Creator.objects.create(
                id    = 1,
                user_id  =1,
                apply_path_id = 1,
                information = 'test',
        )
        Category.objects.create(
                id   = 1,
                name = 'test_category',
        )
        SubCategory.objects.create(
                id   = 1,
                name = 'test_sub_category',
                category_id = 1,
        )
        CourseLevel.objects.create(
                id = 1,
                name = 'test_level',
        )
        CourseStatus.objects.create(
                id   = 4,
                name = '1'
        )
        Product.objects.create(
                id   = 1,
                creator_id = 1
        )
        Course.objects.create(
                id   = 1,
                course_status_id = 4,
                product_id = 1,
        )
        CourseRequest.objects.create(
                id   = 1,
                course_id = 1
        )
        self.token = jwt.encode({'user_id': User.objects.get(name='requesttest').id}, SECRET, algorithm=ALGORITHM)


    def tearDown(self):
        User.objects.all().delete
        UserGrade.objects.all().delete
        ApplyPath.objects.all().delete
        Creator.objects.all().delete
        CourseStatus.objects.all().delete
        Product.objects.all().delete
        Course.objects.all().delete
        CourseRequest.objects.all().delete
        CourseLevel.objects.all().delete
        Category.objects.all().delete
        SubCategory.objects.all().delete
    
    def test_title_update_read(self):
        client = Client()
        stream = BytesIO()
        self.maxDiff = None
        image  = img.new("RGB", (100, 100))
        image.save(stream, format = 'jpeg')
        
        cover_photo = [SimpleUploadedFile('cover_photo.jpg', stream.getvalue(), content_type = "image/jpg")]
        thumbnail   = [SimpleUploadedFile('thumbnail.jpg', stream.getvalue(), content_type = "image/jpg")]

        data = {
                'title'       : 'test_title',
                'cover_photo' : cover_photo,
                'thumbnail'   : thumbnail,
        }

        header  = {"HTTP_Authorization": self.token}
        token   = header['HTTP_Authorization']
        payload = jwt.decode(token, SECRET, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['user_id'])
 
        response = client.post('/request/title', data,  **header, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

        response = client.get('/request/title', **header, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['result']['title'], 'test_title')

class RequestIntroTest(TestCase):
    def setUp(self):
        UserGrade.objects.create(
                id = 1,
                name = '1',
                description = '1',
        )
        User.objects.create(
                id          = 1,
                name        = 'requesttest',
                email       = 'test@test.com',
                grade_id    = 1
        )
        ApplyPath.objects.create(
                id     = 1,
                reason = 'test',
        )
        Creator.objects.create(
                id    = 1,
                user_id  =1,
                apply_path_id = 1,
                information = 'test',
        )
        CourseStatus.objects.create(
                id   = 4,
                name = '1'
        )
        CourseLevel.objects.create(
                id   = 1,
                name = 'test_level',
        )
        Category.objects.create(
                id   = 1,
                name = 'test_category',
        )
        SubCategory.objects.create(
                id   = 1,
                name = 'test_sub_category',
                category_id = 1,
        )

        Product.objects.create(
                id   = 1,
                creator_id = 1
        )
        Course.objects.create(
                id   = 1,
                course_status_id = 4,
                product_id = 1,
        )
        CourseRequest.objects.create(
                id   = 1,
                course_id = 1
        )
        
        self.token = jwt.encode({'user_id': User.objects.get(name='requesttest').id}, SECRET, algorithm=ALGORITHM)

    def tearDown(self):
        User.objects.all().delete
        UserGrade.objects.all().delete
        ApplyPath.objects.all().delete
        Creator.objects.all().delete
        CourseStatus.objects.all().delete
        Product.objects.all().delete
        Course.objects.all().delete
        CourseRequest.objects.all().delete
        CourseLevel.objects.all().delete
        Category.objects.all().delete
        SubCategory.objects.all().delete
    
    def test_intro_update_read(self):
        client = Client()
        stream = BytesIO()

        self.maxDiff = None
        image  = img.new("RGB", (100, 100))
        image.save(stream, format = 'jpeg')
        
        descriptions = []
        photos = []
        
        numbers = randint(1, 9)

        for number in range(1,numbers):
            photos.append(SimpleUploadedFile(f'photo_{number}.jpg', stream.getvalue(), content_type = "image/jpg"))
            descriptions.append(f'description_{number}')
        
        data = {
                'descriptions'  : descriptions,
                'photos'        : photos,
                }

        header  = {"HTTP_Authorization": self.token}
        token   = header['HTTP_Authorization']
        payload = jwt.decode(token, SECRET, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['user_id'])
        
        response = client.post('/request/intro', data,  **header, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

        response = client.get('/request/intro', **header, format='multipart')
        self.assertEqual(response.status_code, 200)


class SingleRequestCreateTest(TestCase):
    def setUp(self):
        UserGrade.objects.create(
                id = 1,
                name = '1',
                description = '1',
        )
        User.objects.create(
                id          = 1,
                name        = 'requesttest',
                email       = 'test@test.com',
                grade_id    = 1
        )
        ApplyPath.objects.create(
                id     = 1,
                reason = 'test',
        )
        CourseStatus.objects.create(
                id   = 4,
                name = '1'
        )
        
        self.token = jwt.encode({'user_id': User.objects.get(name='requesttest').id}, SECRET, algorithm=ALGORITHM)
    
    def tearDown(self):
        User.objects.all().delete
        UserGrade.objects.all().delete
        ApplyPath.objects.all().delete
        CourseStatus.objects.all().delete

    def create_single_request(self):
        client  = Client()
        header  = {"HTTP_Authorization": self.token}
        token   = header['HTTP_Authorization']
        payload = jwt.decode(token, SECRET, algorithms = ALGORITHM)
        user    = User.objects.get(id = payload['user_id'])

        response = client.get('/request/create', **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200) 
