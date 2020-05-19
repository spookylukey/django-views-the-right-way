# Other views in the-pattern.html

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.template.response import TemplateResponse


def hello_world(request):
    return HttpResponse('Hello world!')


def hello_world_2(request, my_arg):
    return HttpResponse(f'Hello world, {my_arg}')


def hello_world_3(request, my_arg):
    template = loader.get_template('hello_world.html')
    context = {}
    return HttpResponse(template.render(context, request))


def hello_world_4(request, my_arg):
    return render(request, 'hello_world.html', {})


def hello_world_5(request, my_arg):
    return TemplateResponse(request, 'hello_world.html', {})
