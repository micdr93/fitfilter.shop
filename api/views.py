from django.http import JsonResponse

def index(request):
    return JsonResponse({"message": "Fitfilter API is live"})
