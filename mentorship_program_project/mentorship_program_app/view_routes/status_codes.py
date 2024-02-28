from django.http import HttpResponse, HttpRequest


def bad_request_400(err_mssg: str="") -> None:
    response = HttpResponse(f"400 Bad Request => {err_mssg}")
    response.status_code = 400
    
    return response
    

#please make it pretty front end :)
def invalid_request_401(request):
    response = HttpResponse('Unauthorized') #better 401 page here
    
    response.status_code = 401
