import json
import re
import bcrypt
import jwt
import hashlib
import hmac
import base64
import requests
import time
import boto3
import uuid

from random import randint
from datetime import datetime, timedelta

from django.views import View
from django.http  import JsonResponse, HttpResponse

from .models     import User, PhoneVerification
from .utils      import id_auth
from my_settings import (
                            serviceId,
                            AUTH_SECRET_KEY,
                            AUTH_ACCESS_KEY,
                            SMS_SEND_PHONE_NUMBER,
                            SECRET,
                            ALGORITHM,
                            AWS_ACCESS_KEY_ID,
                            AWS_SECRET_ACCESS_KEY,
)


class SignUpView(View):

    def validate_email(self, email):
        REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        return re.match(REGEX_EMAIL, email)

    def validate_password(self, password):
        REGEX_PASSWORD_1 = '^(?=.*[0-9])(?=.*[a-zA-Z]).{8,32}$'
        REGEX_PASSWORD_2 = '^(?=.*[!@#$%^&*()_+])(?=.*[a-zA-Z]).{8,32}$'
        REGEX_PASSWORD_3 = '^(?=.*[0-9])(?=.*[!@#$%^&*()_+]).{8,32}$'
        REGEX_PASSWORD_4 = '^(?=.*[0-9])(?=.*[!@#$%^&*()_+])(?=.*[a-zA-Z]).{8,32}$'

        return re.match(REGEX_PASSWORD_1, password) or re.match(REGEX_PASSWORD_2, password) or \
               re.match(REGEX_PASSWORD_3, password) or re.match(REGEX_PASSWORD_4, password)

    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'EXISTS_EMAIL'}, status=401)

            if not self.validate_email(data['email']):
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=401)

            if not self.validate_password(data['password']):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

            hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            name  = data['name']
            email = data['email']
            phone = data['phone']

            if User.objects.filter(number=phone).exists():
                User.objects.filter(number=phone).update(
                    name     = name,
                    email    = email,
                    password = hashed_pw,
                )

                PhoneVerification.objects.get(phone=phone).delete()
                return JsonResponse({'message': 'SUCCESS'}, status=201)

            else:
                return JsonResponse({'message': 'INVALID_NUMBER'}, status=401)

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: =>  {e}'}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'message': f'JSON_ERROR: =>  {e}'}, status=400)


class SignInView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(hours=24)}, SECRET,
                                              algorithm=ALGORITHM)
                    return JsonResponse({'ACCESS_TOKEN': access_token}, status=201)

                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

            return JsonResponse({'message': 'INVALID_EMAIL'}, status=401)

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: =>  {e}'}, status=400)

        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: =>  {e}'}, status=400)


class SMSVerificationView(View):

    def send_verification(self, phone, code):
        SMS_URL = 'https://sens.apigw.ntruss.com/sms/v2/services/' + f'{serviceId}' + '/messages'
        timestamp = str(int(time.time() * 1000))
        secret_key = bytes(AUTH_SECRET_KEY, 'utf-8')

        method = 'POST'
        uri = '/sms/v2/services/' + f'{serviceId}' + '/messages'
        message = method + ' ' + uri + '\n' + timestamp + '\n' + AUTH_ACCESS_KEY

        message = bytes(message, 'utf-8')

        signingKey = base64.b64encode(
            hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': AUTH_ACCESS_KEY,
            'x-ncp-apigw-signature-v2': signingKey,
        }

        body = {
            'type': 'SMS',
            'contentType': 'COMM',
            'countryCode': '82',
            'from': f'{SMS_SEND_PHONE_NUMBER}',
            'content': f'인녕하세요. ac101 입니다. 인증번호 [{code}]를 입력해주세요.',
            'messages': [
                {
                    'to': phone
                }
            ]
        }

        encoded_data = json.dumps(body)
        res = requests.post(SMS_URL, headers=headers, data=encoded_data)
        return HttpResponse(res.status_code)

    def post(self, request):
        try:
            data = json.loads(request.body)
            phone = data['phone']

            code = str(randint(100000, 999999))

            PhoneVerification.objects.update_or_create(
                phone=phone,
                defaults={
                    'phone': phone,
                    'code' : code
                }
            )

            self.send_verification(
                phone=phone,
                code=code
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: =>  {e}'}, status=400)

        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: =>  {e}'}, status=400)


class SMSVerificationConfirmView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            phone = data['phone']
            verification_number = data['code']

            if verification_number == PhoneVerification.objects.get(phone=phone).code:
                if not User.objects.filter(number=phone).exists():
                    User.objects.create(number=phone)
                    return JsonResponse({'message': 'SUCCESS'}, status=200)

                else:
                    return JsonResponse({'message': 'REGISTERED_NUMBER'}, status=401)
            return JsonResponse({'message': 'INVALID_NUMBER'}, status=401)

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: =>  {e}'}, status=400)

        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: =>  {e}'}, status=400)


class KakaoSignInView(View):

    def get(self, request):
        try:
            access_token = request.headers['Authorization']
            kakao_header = {'Authorization': f'Bearer {access_token}'}
            url = 'https://kapi.kakao.com/v2/user/me'
            response = requests.get(url, headers=kakao_header)
            data = response.json()

            if not data.get('id'):
                return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)

            email = data['kakao_account']['email']
            name  = data['kakao_account']['profile']['nickname']

            user, created = User.objects.get_or_create(email=email, name=name)

            access_token = jwt.encode({'id': user.id}, SECRET, algorithm=ALGORITHM)

            return JsonResponse({'ACCESS_TOKEN': access_token}, status=201)

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: =>  {e}'}, status=400)

        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: =>  {e}'}, status=400)


class ProfileView(View):

    #@id_auth
    def post(self, request):
        data = json.loads(request.body)

        #user = request.user
        user_id = 11
        name           = data['name']
        nickname       = data['nickname']

        try:
            User.objects.filter(id = user_id).update(
                name          = name,
                nickname      = nickname,
            )

            return JsonResponse({'message': "SUCCESS"}, status=201)

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: =>  {e}'}, status=400)

        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: =>  {e}'}, status=400)


class ProfileDataView(View):

    @id_auth
    def get(self,request):
        user = request.user
        db_user = User.objects.get(id = user.id)
        try:
            result = {
                "name"     : db_user.name,
                "nickname" : db_user.nickname,
                "image"    : db_user.profile_image,
                "email"    : db_user.email,
                "phone"    : db_user.number,
            }

            return JsonResponse({'result': result}, status=200)

        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR: =>  {e}'}, status=400)

        except ValueError as e:
            return JsonResponse({'message': f'VALUE_ERROR: =>  {e}'}, status=400)


class ProfileImageView(View):

    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )

    @id_auth
    def post(self, request):
        user = request.user
        file  = request.FILES['file']

        if file:
            filename = str(uuid.uuid1()).replace('-','')
            self.s3_client.upload_fileobj(
                file,
                'ac101',
                filename,
                ExtraArgs = {
                    'ContentType': 'image/jpeg'
                }
            )
            file_url = f"https://s3.ap-northeast-2.amazonaws.com/ac101/{filename}"

            User.objects.filter(id = user.id).update(
                profile_image = file_url
            )

            return JsonResponse({'message': 'SUCCESS'}, status=200)
