from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def main(request):
    '''
    Render the main page
    '''
    html ='''
    <!doctype html>
    <html>
    <head>
    <title> My Blog </title>
    <meta charset='utf-8'>
    </head>
    <body>
        這是HTML版本的Hello World!
    </body>
    </html>
    '''
    return HttpResponse(html)