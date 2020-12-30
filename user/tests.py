import json
import bcrypt
import jwt

from django.test import TestCase, Client, TransactionTestCase
from random import randint
from unittest.mock import patch
from unittest.mock import Mock, MagicMock, call

from user.models import User, PhoneVerification, UserGrade
from my_settings import (
                            SECRET,
                            ALGORITHM,
                        )


class SendSmsTest(TransactionTestCase):

    def test_send_sms(self):
        client = Client()
        data   = {
            'phone' : '01085327254'
        }

        response = client.post('/user/sms', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'SUCCESS'})


class CheckSmsTest(TransactionTestCase):

    def setUp(self):
        data = {
            'phone': '01085327254'
        }
        phone = data['phone']

        code = str(randint(100000, 999999))

        PhoneVerification.objects.update_or_create(
            phone=phone,
            code=code,
            id = 1
        )

        UserGrade.objects.create(
            id=1,
            name='기본',
            description='기본회원입니다'
        )

        User.objects.create(
            id=1,
            name='테스트',
            email='test@naver.com',
            password='asdfasdf',
            nickname='테스트',
            grade_id=1
        )

    def tearDown(self):
        PhoneVerification.objects.all().delete()
        User.objects.all().delete()

    def test_check_sms(self):
        client = Client()
        data   = {
            'phone' : '01085327254',
            'code'  : PhoneVerification.objects.get(phone = '01085327254').code
        }

        response = client.post('/user/sms_verification', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS'})


class SignUpTest(TestCase):

    def setUp(self):
        hashed_pw = bcrypt.hashpw('wecode1@'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        data = {
            'phone': '01085327254'
        }
        phone = data['phone']
        code = str(randint(100000, 999999))

        UserGrade.objects.create(
            id=1,
            name='기본',
            description='기본회원입니다'
        )

        PhoneVerification.objects.update_or_create(
            phone=phone,
            code=code,
            id=1
        )

        User.objects.create(
            id=1,
            name='테스트',
            email='test@naver.com',
            password=hashed_pw,
            nickname='테스트',
            grade_id=1
        )

    def tearDown(self):
        PhoneVerification.objects.all().delete()
        User.objects.all().delete()
        UserGrade.objects.all().delete()

    def test_singup(self):
        client = Client()
        data   = {
            'name' : 'kim',
            'email' : 'we@naver.com',
            'password' : 'wecode1@',
            'phone' : '01235327230'
        }

        response = client.post('/user/signup', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'SUCCESS'})


class SignInTest(TestCase):

    def setUp(self):
        hashed_pw = bcrypt.hashpw('wecode1@'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


        UserGrade.objects.create(
            id=1,
            name='기본',
            description='기본회원입니다'
        )

        User.objects.create(
            name='kim',
            email='kim@naver.com',
            password=hashed_pw,
            number='01988332223',
            grade_id = 1
        )

        PhoneVerification.objects.update_or_create(
            phone="01044442222",
            code="000022",
            id=1
        )

    def tearDown(self):
        UserGrade.objects.all().delete()
        User.objects.all().delete()
        PhoneVerification.objects.all().delete()

    def test_signin(self):
        client = Client()
        data = {
            'email'    : 'kim@naver.com',
            'password' : 'wecode1@'
        }

        response = client.post('/user/signin', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'access_token': response.json()['access_token']})

