from django.template.response import TemplateResponse

# The pattern:

def example_view(request, arg):
    return TemplateResponse(request, 'example.html', {})
