import jwt
import json

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from my_settings import SECRET, ALGORITHM
from user.models import User

def id_auth(func):

    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, SECRET, algorithms = ALGORITHM)
            user         = User.objects.get(id = payload["id"])
            request.user = user

            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)

        except jwt.InvalidTokenError:
            return JsonResponse({'MESSAGE': 'INVALID_ACCESS_TOKEN'}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'EXPIRED_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

    return wrapper
