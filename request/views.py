import re
import json

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction
from django.shortcuts import get_object_or_404

import boto3
from PIL import Image
from io  import BytesIO
import uuid

from product.models import Product, Course, Category, SubCategory, CourseLevel, CourseStatus
from request.models import CourseRequest, RequestCard, Tag, RequestCurriculum
from user.models    import User, Creator
from user.utils     import id_auth

from my_settings import AWS_KEY_ID, AWS_ACCESS_KEY, AWS_BUCKET_NAME


class RequestView(View):
    @id_auth
    def post(self, request):
        if Creator.objects.filter(user = request.user).exists():
            creator = Creator.objects.get(user = request.user)

            with transaction.atomic():
                product_creating = Product.objects.create(creator = creator)
                course_creating  = Course.objects.create(course_status_id=4, product=product_creating)
                request_creating = CourseRequest.objects.create(course=course_creating)
            return JsonResponse({"message": "SUCCESS"}, status = 201)
        else:
            return JsonResponse({"message": "INVALID_CREATOR"}, status = 400)

    @id_auth
    def get(self, request):
        if Creator.objects.filter(user = request.user).exists(): 
            creator  = Creator.objects.get(user=request.user)
            requests = CourseRequest.objects.select_related('course', 'course__product').prefetch_related('course__course_status').filter(course__in = Course.objects.filter(product__in = Product.objects.filter(creator = creator)))

            result = [
                        {
                            "id"        : request.id,
                            "thumbnail" : request.thumbnail,
                            "name"      : request.course.product.name,
                            "status"    : request.course.course_status.name,
                         } for request in requests
                      ]
            return JsonResponse({"result": result}, status = 200)
        else:
            return JsonResponse({"message": "NOT_CREATOR_USER"}, status = 400)


class SingleRequestCreateView(View):
    @id_auth
    def get(self, request):
        if not Creator.objects.filter(user = request.user).exists():
            Creator.objects.create(user = request_user,  apply_path_id = 1)
        
        with transaction.atomic():
            product, created = Product.objects.get_or_create(creator = get_object_or_404(Creator, user = request.user))
            if created:
                    course  = Course.objects.create(course_status_id = 4, product = product)
                    request = CourseRequest.objects.create(course = course)
            else:
                    course  = Course.objects.get(product = product)
                    request = CourseRequest.objects.select_related('course', 'course__product', 'course__product__creator__user').get(course = course)

        result = {
                        "nickname"          : request.course.product.creator.user.nickname,
                        "category_id"       : request.course.product.sub_category.category.id,
                        "category"          : request.course.product.sub_category.category.name,
                        "sub_category_id"   : request.course.product.sub_category.id,
                        "sub_category"      : request.course.product.sub_category.name,
                        "category_detail"   : request.specific_category,
                        "level_id"          : request.course.level.id,
                        "level"             : request.course.level.name
                }

        return JsonResponse({"result": result}, status = 200)


class CategoryListView(View):
    def get(self, request):
        sub_category_list = []
        for category_id in range(1, 4):
            sub_categories = SubCategory.objects.filter(category = get_object_or_404(Category, id = category_id))
            sub_category = [{
                                "id"     : sub_category.id,
                                "name"   : sub_category.name,
                            } for sub_category in sub_categories]
            sub_category_list.append(sub_category)

        return JsonResponse({"creative": sub_category_list[0], "career": sub_category_list[1], "money": sub_category_list[2]}, status = 200)


class RequestBasicInfoView(View):
#    @id_auth
    def post(self, request):
        request_edit = get_object_or_404(
                CourseRequest.objects.select_related('course__product__creator__user', 'course__product__sub_category', 'course__level'), 
                course__in = Course.objects.filter(product__in = Product.objects.filter(creator = get_object_or_404(Creator, user = request.user))))
      
        request_edit.course.product.creator.user.nickname = request.POST['nickname']
        request_edit.course.product.creator.user.save()
        request_edit.course.product.sub_category_id = get_object_or_404(SubCategory, name = request.POST['sub_category']).id
        request_edit.course.product.save()
        request_edit.course.level_id = get_object_or_404(CourseLevel, name = request.POST['level']).id
        request_edit.course.save()
        request_edit.specific_category = request.POST['category_detail']
        request_edit.save()

        return JsonResponse({"message": "SUCCESS"}, status = 200)

    @id_auth
    def get(self, request):
        request_edit = get_object_or_404(
                CourseRequest.objects.select_related('course__product__sub_category', 'course__product__creator__user'), 
                course__in = Course.objects.filter(product__in = Product.objects.filter(creator = get_object_or_404(Creator, user = request.user)))
                )
       
        result = {
                        "nickname"          : request_edit.course.product.creator.user.nickname,
                        "category_id"       : request_edit.course.product.sub_category.category.id,
                        "category"          : request_edit.course.product.sub_category.category.name,
                        "sub_category_id"   : request_edit.course.product.sub_category.id,
                        "sub_category"      : request_edit.course.product.sub_category.name,
                        "category_detail"   : request_edit.specific_category,
                        "level_id"          : request_edit.course.level.id,
                        "level"             : request_edit.course.level.name
        }

        return JsonResponse({"result": result}, status = 200)


class RequestTitleView(View):
    s3_client = boto3.client('s3', aws_access_key_id = AWS_KEY_ID, aws_secret_access_key= AWS_ACCESS_KEY)

    @id_auth
    def post(self, request):
        request_edit = get_object_or_404(
                CourseRequest.objects.select_related('course__product'), 
                course__in = Course.objects.filter(product__in = Product.objects.filter(creator = get_object_or_404(Creator, user = request.user)))
        )
 
        request_edit.course.product.name = request.POST['title']
        request_edit.course.product.save()
            
        file_urls = []

        for file in request.FILES.getlist('cover_photo'):
            filename = str(uuid.uuid1()).replace('-','')
            self.s3_client.upload_fileobj(
                    file,
                    AWS_BUCKET_NAME,
                    filename,
                    ExtraArgs = {
                        "ContentType": file.content_type
                    }
            )
            file_urls.append(f"https://{AWS_BUCKET_NAME}.s3.us-east-2.amazonaws.com/{filename}")

        for file in request.FILES.getlist('thumbnail'):
            filename = str(uuid.uuid1()).replace('-','')
            self.s3_client.upload_fileobj(
                    file,
                    AWS_BUCKET_NAME,
                    filename,
                    ExtraArgs = {
                        "ContentType": file.content_type
                    }
            )
            file_urls.append(f"https://{AWS_BUCKET_NAME}.s3.us-east-2.amazonaws.com/{filename}")

        request_edit.cover_photo = file_urls[0]
        request_edit.thumbnail   = file_urls[1]
        request_edit.save()

        return JsonResponse({"message": "SUCCESS"}, status = 200)


    @id_auth
    def get(self, request):
        request_edit = get_object_or_404(
                CourseRequest.objects.select_related('course__product'), 
                course__in = Course.objects.filter(product__in = Product.objects.filter(creator = get_object_or_404(Creator, user = request.user)))
                )

        result = {
                    "title"       : request_edit.course.product.name,
                    "cover_photo" : request_edit.cover_photo,
                    "thumbnail"   : request_edit.thumbnail
        }
        return JsonResponse({"result": result}, status = 200)


class RequestIntroView(View):
    s3_client = boto3.client('s3', aws_access_key_id = AWS_KEY_ID, aws_secret_access_key= AWS_ACCESS_KEY)

    @id_auth
    def post(self, request):
        request_edit = get_object_or_404(
                CourseRequest.objects.select_related('course__course_status'), 
                course__in = Course.objects.filter(product__in = Product.objects.filter(creator = get_object_or_404(Creator, user = request.user)))
        )

        assert len(request.POST.getlist('descriptions')) == len(request.FILES.getlist('photos')), "NUMBER OF PHOTOS AND DESCRIPTIONS IS NOT MATCHED"
            
        count = len(request.POST.getlist('descriptions'))

        file_urls = []

        for file in request.FILES.getlist('photos'):
            filename = str(uuid.uuid1()).replace('-','')
            self.s3_client.upload_fileobj(
                file,
                AWS_BUCKET_NAME,
                filename,
                ExtraArgs = {
                    "ContentType": file.content_type
                }
            )
            file_urls.append(f"https://{AWS_BUCKET_NAME}.s3.us-east-2.amazonaws.com/{filename}")

        for number in range(0, count):
            RequestCard.objects.create(request = request_edit, photo = file_urls[number], description = request.POST.getlist('descriptions')[number])

        return JsonResponse({"message": "SUCCESS"}, status = 200)

    @id_auth
    def get(self, request):
        request_cards = RequestCard.objects.filter(
            request = get_object_or_404(
                CourseRequest.objects.select_related('course__product'), 
                course__in = Course.objects.filter(product__in = Product.objects.filter(creator = get_object_or_404(Creator, user = request.user)))
        ))

        results = [{
                        "id"          : request_card.id,
                        "photo"       : request_card.photo,
                        "description" : request_card.description,
                    } for request_card in request_cards][-3:]
        
        return JsonResponse({"result": results}, status = 200)
