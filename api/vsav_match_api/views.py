from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def test_me_view(request):
    return render( request, 'test.html', {
        'whatkind' : 'this_kind'
    })
