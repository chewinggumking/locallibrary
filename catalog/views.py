from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.

def helloWorld(request):
    message_to_u = """<h1>HELLO WORLD</h1>
    <p>This is the catalog app landing page</p>
    """
    return HttpResponse(message_to_u)
