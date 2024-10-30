from django.http import HttpResponse
from django.http import JsonResponse

def custom404(request, exception=None):
    not_found_resp_message = {"success" : False, "message" : "Not Found!"}
    return JsonResponse(data=not_found_resp_message, status= 404)
 