from django.http import HttpResponse
from django.template import loader


def test_view1(request):
    template = loader.get_template('sign-in card/role_selection.html')
    context = {}
    return HttpResponse(template.render(context, request))

def test_view2(request):
    template = loader.get_template('sign-in card/account_activation_mentee.html')
    context = {}
    return HttpResponse(template.render(context, request))

def default(req):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, req))

def landing(req):
    template = loader.get_template('landing_page.html')
    context = {}
    return HttpResponse(template.render(context, req))

def role_test(req):
    template = loader.get_template('sign-in-card/experiment.html')
    context = {}
    return HttpResponse(template.render(context, req))