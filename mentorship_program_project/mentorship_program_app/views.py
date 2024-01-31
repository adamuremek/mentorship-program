from django.http import HttpResponse
from django.template import loader


def test_view1(request):
    template = loader.get_template('sign-in card/role_selection.html')
    context = {

    }
    return HttpResponse(template.render(context, request))