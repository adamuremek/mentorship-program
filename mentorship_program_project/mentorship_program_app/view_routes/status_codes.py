from django.http import HttpResponse, HttpRequest

"""
file that includes request status codes for when things go wrong

NOTE: these need to include **kwargs to work properly in other views
"""


def bad_request_400(err_mssg: str="",**kwargs) -> None:
    response = HttpResponse(f"400 Bad Request => {err_mssg}")
    response.status_code = 400
    
    return response
    

#please make it pretty front end :)
def invalid_request_401(request,**kwargs):
    response = HttpResponse('Unauthorized') #better 401 page here
    
    response.status_code = 401
