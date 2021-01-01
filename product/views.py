import json,bcrypt,re,jwt

from django.views import View
from django.http import JsonResponse

from django.db.models import Count, Sum
from operator import itemgetter
from user.utils import id_auth
from my_settings import SECRET, ALGORITHM
from user.models import Creator,User
from request.models import CourseRequest
from product.models import (
    Course,
    CourseStatus,
    Category,
    SubCategory,
    ProductImage,
    Product,
    ProductLike
)

 #클래스 좋아요 기능
class ProductLikeView(View):
    @id_auth
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user    = request.user
            product = Product.objects.get(id = data['product'])

            if ProductLike.objects.filter(user = user, product = product).exists():
                return JsonResponse({'message':'ALREADY_LIKE'},status = 400)
            ProductLike.objects.create(user = user, product = product)
            return JsonResponse({"message":"SUCCESS"},status = 201)
        except Product.DoesNotExist:
            return JsonResponse({"message":"DOESNOTEXIST"}, status=404)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"message":"INVALID_DATA"}, status=400)

 #좋아요 취소
    @id_auth
    def delete(self, request):
        try:
            data    = json.loads(request.body)
            user    = request.user
            product = Product.objects.get(id = data['product'])

            if ProductLike.objects.filter(user_id = user, product_id = product).exists():
               ProductLike.objects.get(user = user, product = product).delete()
               return JsonResponse({'message':'SUCCESS'}, status = 204)
            return JsonResponse({'message':'NOT_EXIST'}, status = 400)
        except Exception as ex:
            return JsonResponse({"message":"ERROR_" + ex.args[0]}, status=400)

#크리에이터 메인화면 보여주기
class CourseListView(View):
    def get(self, request, category_pk):
        products = Product.objects.prefetch_related('course_set','course_set__course_status','course_set__courserequest_set','productlike_set').select_related('sub_category','creator', 'creator__user','sub_category__category').filter(sub_category__category_id = category_pk, course__course_status_id = 1).order_by('-id')
        if not products.exists():
            return JsonResponse({'message':'PRODUCT_NOT_FOUND'},status=404)
        results = [{
            'id'            : product.id,
            'alt'           : product.name,
            'cover_image'   : product.course_set.get().courserequest_set.all()[0].thumbnail,
            'sub_category'  : product.sub_category.name,
            'course_status' : product.course_set.get().course_status.name,
            'creator'       : product.creator.user.nickname,
            'name'          : product.name,
            'price'         : product.price,
            'like'          : product.productlike_set.filter(product_id = product.id).count(),
            'created_at'    : product.course_set.get().courserequest_set.all()[0].created_at
        }for product in products] 
        return JsonResponse({'message':'SUCCESS', 'results': results}, status=200)    

class EarlybirdView(View):
    def get(self, request):
        products = Product.objects.prefetch_related('course_set','course_set__course_status','course_set__courserequest_set','productlike_set').select_related('sub_category','creator', 'creator__user','sub_category__category').filter(course__course_status_id = 2)
        
        if not products.exists():
            return JsonResponse({'message':'PRODUCT_NOT_FOUND'},status=404)
        results = [{
            'id'            : product.id,
            'alt'           : product.name,
            'cover_image'   : product.course_set.get().courserequest_set.all()[0].thumbnail,
            'sub_category'  : product.sub_category.name,
            'course_status' : product.course_set.get().course_status.name,
            'creator'       : product.creator.user.nickname,
            'name'          : product.name,
            'price'         : product.price,
            'like'          : product.productlike_set.filter(product_id = product.id).count(),
            'created_at'    : product.course_set.get().courserequest_set.all()[0].created_at
        }for product in products]      
        return JsonResponse({'MESSAGE' : 'SUCCESS', 'results' : results}, status=200)


#like 기준 높은거 보여주기
class OrderByLikeView(View):
    def get(self, request):         
        products = Product.objects.select_related('sub_category','creator', 'creator__user','sub_category__category').prefetch_related('course_set','course_set__course_status','course_set__courserequest_set','productlike_set').filter(course__course_status_id = 1)

        if not products.exists():
            return JsonResponse({'message':'PRODUCT_NOT_FOUND'},status=404)

        results = [{
            'id'            : product.id,
            'alt'           : product.name,
            'cover_image'   : product.course_set.get().courserequest_set.all()[0].thumbnail,
            'sub_category'  : product.sub_category.name,
            'course_status' : product.course_set.get().course_status.name,
            'creator'       : product.creator.user.nickname,
            'name'          : product.name,
            'price'         : product.price,
            'like'          : product.productlike_set.filter(product_id = product.id).count(),
            'created_at'    : product.course_set.get().courserequest_set.all()[0].created_at
        }for product in products]

        result = sorted(results, key=lambda x:x['like'], reverse=True)
                    
        return JsonResponse({'message':'SUCCESS', 'results': result}, status=200)




