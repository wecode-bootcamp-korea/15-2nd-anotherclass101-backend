import unittest, json, jwt, bcrypt

from my_settings import SECRET,ALGORITHM
from datetime import datetime
from django.test import TestCase, TransactionTestCase, Client
from request.models import CourseRequest
from user.models import (
    User,
    UserGrade,
    ApplyPath,
    Creator
)
from product.models import (
    Course,
    CourseStatus,
    Category,
    SubCategory,
    ProductImage,
    Product,
    ProductLike,
    CourseLevel
)

class ProductLikeViewTest(TransactionTestCase):
    def setUp(self):
        UserGrade.objects.create(
            id = 1,
            name = '기본',
            description = '기본회원입니다'
        )
        User.objects.create(
            id = 1,
            name = '테스트',
            email = 'test@naver.com',
            password = 'asdfasdf',
            nickname = '테스트',
            grade_id = 1
        )
        ApplyPath.objects.create(
            id = 1,
            reason = '사이트발견'
        )
        Creator.objects.create(
            id = 1,
            user_id = 1,
            apply_path_id = 1,
            information = '테스트용입니다'
        )
        Category.objects.create(
            id = 1,
            name = '카테고리')

        SubCategory.objects.create(
            id = 1,
            name = '서브카테고리',
            category_id = 1
        )
        Product.objects.create(
            id = 1,
            name = '테스트',
            creator_id = 1,
            price = 1000,
            sub_category_id = 1,
            refund_policy = '환불안됨',
        )
        CourseStatus.objects.create(
            id = 2,
            name = '오픈'
        )
        CourseLevel.objects.create(
            id = 1,
            name = '초급'
        )
        Course.objects.create(
            id = 1,
            kit_description = 'test',
            course_status_id = 2,
            benefit = 'test',
            product_id = 1,
            level_id = 1
        )

    def tearDown(self):
        UserGrade.objects.all().delete()
        User.objects.all().delete()
        ApplyPath.objects.all().delete()
        Creator.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Product.objects.all().delete()
        CourseStatus.objects.all().delete()
        CourseLevel.objects.all().delete()
        Course.objects.all().delete()
        CourseRequest.objects.all().delete()

    def test_product_like_post_success(self):
        client = Client()
        payload = {"id":1}
        headers = {"HTTP_AUTHORIZATION" : jwt.encode(payload, SECRET, algorithm=ALGORITHM)}
        data = {
            "user": 1,
            "product": 1
        }
        response = self.client.post('/product/like',data, content_type="application/json", **headers)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.json(),
             {'message': 'SUCCESS'}
        )

    def test_product_like_post_doesnotexist_fail(self):
        client  = Client()
        payload = {"id":1}
        headers = {"HTTP_AUTHORIZATION" : jwt.encode(payload, SECRET, algorithm=ALGORITHM)}
        data = {
            "user": 1,
            "product": 3
        }
        response = self.client.post('/product/like',data, content_type="application/json", **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
            {"message" : "DOESNOTEXIST"}
        )

    def test_product_like_post_invealid_user_fail(self):
        client   = Client()
        payload = {"id":2}
        headers = {"HTTP_AUTHORIZATION" : jwt.encode(payload, SECRET, algorithm=ALGORITHM)}
        data = {
            "user": 1,
            "product": 1
        }
        response = self.client.post('/product/like',data, content_type="application/json", **headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {
            "MESSAGE" : "INVALID_USER"
            })

    def test_product_like_post_keyerror_fail(self):
        client   = Client()
        payload = {"id":1}
        headers = {"HTTP_AUTHORIZATION" : jwt.encode(payload, SECRET, algorithm=ALGORITHM)}
        data = {
        "user": 1,
        "products": 1
        }
        response = self.client.post('/product/like',data, content_type="application/json", **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
        "message" : "KEY_ERROR"
        })

class CourseListViewTest(TransactionTestCase):
    def setUp(self):
        UserGrade.objects.create(
            id = 1,
            name = '기본',
            description = '기본회원입니다'
        )
        User.objects.create(
            id = 1,
            name = '테스트',
            email = 'test@naver.com',
            password = 'asdfasdf',
            nickname = '테스트',
            grade_id = 1
        )
        ApplyPath.objects.create(
            id = 1,
            reason = '사이트발견'
        )
        Creator.objects.create(
            id = 1,
            user_id = 1,
            apply_path_id = 1,
            information = '테스트용입니다'
        )
        Category.objects.create(
            id = 1,
            name = '카테고리')

        SubCategory.objects.create(
            id = 1,
            name = '서브카테고리',
            category_id = 1
        )
        Product.objects.create(
            id = 1,
            name = '테스트',
            creator_id = 1,
            price = 1000,
            sub_category_id = 1,
            refund_policy = '환불안됨',
        )
        CourseStatus.objects.create(
            id = 1,
            name = '오픈'
        )
        CourseLevel.objects.create(
            id = 1,
            name = '초급'
        )

        Course.objects.create(
            id = 1,
            kit_description = 'test',
            course_status_id = 1,
            benefit = 'test',
            product_id = 1,
            level_id = 1
        )
        CourseRequest.objects.create(
            id = 1,
            cover_photo = "https://file3.instiz.net/data/cached_img/upload/2018/06/22/14/eb6f4005da542f4dc5276a034e519607.jpg",
            thumbnail = "https://file3.instiz.net/data/cached_img/upload/2018/06/22/14/eb6f4005da542f4dc5276a034e519607.jpg",
            summary_photo = "https://file3.instiz.net/data/cached_img/upload/2018/06/22/14/eb6f4005da542f4dc5276a034e519607.jpg",
            specific_category = 'text',
            course_id = 1,
            expiry_date = str(datetime.now()),
            created_at = str(datetime.now())
        )

    def tearDown(self):
        UserGrade.objects.all().delete()
        User.objects.all().delete()
        ApplyPath.objects.all().delete()
        Creator.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Product.objects.all().delete()
        CourseStatus.objects.all().delete()
        CourseLevel.objects.all().delete()
        Course.objects.all().delete()
        CourseRequest.objects.all().delete()

    def test_course_list_view_get(self):
        client = Client()
        response  = client.get('/product/category/1', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results'][0]['id'], 1)

    def test_course_list_view_get_fail(self):
        client   = Client()
        response = client.get('/product/category/100', content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "message" : 'PRODUCT_NOT_FOUND'
            })

class EarlybirdListViewTest(TransactionTestCase):
    def setUp(self):
        UserGrade.objects.create(
            id = 1,
            name = '기본',
            description = '기본회원입니다'
        )
        User.objects.create(
            id = 1,
            name = '테스트',
            email = 'test@naver.com',
            password = 'asdfasdf',
            nickname = '테스트',
            grade_id = 1
        )
        ApplyPath.objects.create(
            id = 1,
            reason = '사이트발견'
        )
        Creator.objects.create(
            id = 1,
            user_id = 1,
            apply_path_id = 1,
            information = '테스트용입니다'
        )
        Category.objects.create(
            id = 1,
            name = '카테고리')

        SubCategory.objects.create(
            id = 1,
            name = '서브카테고리',
            category_id = 1
        )
        Product.objects.create(
            id = 1,
            name = '테스트',
            creator_id = 1,
            price = 1000,
            sub_category_id = 1,
            refund_policy = '환불안됨',
        )
        CourseStatus.objects.create(
            id = 2,
            name = '오픈'
        )
        CourseLevel.objects.create(
            id = 1,
            name = '초급'
        )
        Course.objects.create(
            id = 1,
            kit_description = 'test',
            course_status_id = 2,
            benefit = 'test',
            product_id = 1,
            level_id = 1
        )
        CourseRequest.objects.create(
            id = 1,
            cover_photo = "https://file3.instiz.net/data/cached_img/upload/2018/06/22/14/eb6f4005da542f4dc5276a034e519607.jpg",
            thumbnail = "https://file3.instiz.net/data/cached_img/upload/2018/06/22/14/eb6f4005da542f4dc5276a034e519607.jpg",
            summary_photo = "https://file3.instiz.net/data/cached_img/upload/2018/06/22/14/eb6f4005da542f4dc5276a034e519607.jpg",
            specific_category = 'text',
            course_id = 1,
            expiry_date = str(datetime.now()),
            created_at = str(datetime.now())
        )

    def tearDown(self):
        UserGrade.objects.all().delete()
        User.objects.all().delete()
        ApplyPath.objects.all().delete()
        Creator.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Product.objects.all().delete()
        CourseStatus.objects.all().delete()
        CourseLevel.objects.all().delete()
        Course.objects.all().delete()
        CourseRequest.objects.all().delete()

    def test_earlybird_view_get_success(self):
        client = Client()
        response  = client.get('/product/status', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results'][0]['id'], 1)

    def test_earlybird_view_get_fail(self):
        client   = Client()
        Product.objects.all().delete()
        response = client.get('/product/status', content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "message" : 'PRODUCT_NOT_FOUND'
            })

class OrderByLikeViewTest(TransactionTestCase):
    def setUp(self):
        UserGrade.objects.create(
            id = 1,
            name = '기본',
            description = '기본회원입니다'
        )
        User.objects.create(
            id = 1,
            name = '테스트',
            email = 'test@naver.com',
            password = 'asdfasdf',
            nickname = '테스트',
            grade_id = 1
        )
        ApplyPath.objects.create(
            id = 1,
            reason = '사이트발견'
        )
        Creator.objects.create(
            id = 1,
            user_id = 1,
            apply_path_id = 1,
            information = '테스트용입니다'
        )
        Category.objects.create(
            id =2,
            name = '카테고리')

        SubCategory.objects.create(
            id = 1,
            name = '서브카테고리',
            category_id = 2
        )
        Product.objects.create(
            id = 1,
            name = '테스트',
            creator_id = 1,
            price = 1000,
            sub_category_id = 1,
            refund_policy = '환불안됨',
        )
        CourseStatus.objects.create(
            id = 1,
            name = '오픈'
        )
        CourseLevel.objects.create(
            id = 1,
            name = '초급'
        )
        Course.objects.create(
            id = 1,
            kit_description = 'test',
            course_status_id = 1,
            benefit = 'test',
            product_id = 1,
            level_id = 1
        )
        CourseRequest.objects.create(
            id = 1,
            cover_photo = "https://file3.instiz.net/data/cached_img/upload/2018/06/22/14/eb6f4005da542f4dc5276a034e519607.jpg",
            thumbnail = "https://file3.instiz.net/data/cached_img/upload/2018/06/22/14/eb6f4005da542f4dc5276a034e519607.jpg",
            summary_photo = "https://file3.instiz.net/data/cached_img/upload/2018/06/22/14/eb6f4005da542f4dc5276a034e519607.jpg",
            specific_category = 'text',
            course_id = 1,
            expiry_date = str(datetime.now()),
            created_at = str(datetime.now())
        )

    def tearDown(self):
        UserGrade.objects.all().delete()
        User.objects.all().delete()
        ApplyPath.objects.all().delete()
        Creator.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Product.objects.all().delete()
        CourseStatus.objects.all().delete()
        CourseLevel.objects.all().delete()
        Course.objects.all().delete()
        CourseRequest.objects.all().delete()

    def test_order_by_like_view_get_success(self):
        client = Client()
        response  = client.get('/product/orderbylike', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results'][0]['id'], 1)

    def test_order_by_like_view_get_fail(self):
        client   = Client()
        Product.objects.all().delete()
        response = client.get('/product/status', content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "message" : 'PRODUCT_NOT_FOUND'
            })
