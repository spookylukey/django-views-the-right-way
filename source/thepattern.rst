The Definitive Pattern
======================

The pattern
-----------

This is how you start writing any HTML-based view in Django:

.. code-block:: python

   from django.template.response import TemplateResponse

   def example_view(request, arg):
       return TemplateResponse(request, "example.html", {})


With the corresponding urls.py:

.. code-block:: python

   from django.urls import path

   from . import views

   urlpatterns = [
       path('example/<str:arg>/', views.example_view, name='example_name'),
   ]


Which bits do you change?

* ``example_view`` should be the name of your page e.g. ``home`` or ``kitten_list``.
* ``example.html`` should be the path to the template you are using.
* ``{}``, the third argument to ``TemplateResponse``, is the context data you
  want available in your template.
* ``arg`` is a placeholder for any number of optional URL arguments — parts of
  the URL path that you are matching with a `path converter
  <https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters>`_
  (here we used ``str``) and supplying to the view function as a parameter. You
  can remove it, or add more, but have to change the URLconf to match.

That's it!

But, you need a slightly deeper understanding if you're going to write good
Django views.

The explanation
---------------

Most pages won't have this longer section, but because this is foundational I'm
spending a bit more time.

First, it's vital to know what a view **is**. As the `Django docs state
<https://docs.djangoproject.com/en/stable/topics/http/views/>`_:

   A view...is a Python function that takes a Web request and returns a Web response

Given that definition, what does your most basic view function look like? Time
for Hello World! In your views.py, you'd have this:


.. code-block:: python

   from django.http import HttpResponse

   def hello_world(request):
       return HttpResponse("Hello world!")


This function expects to receive a ‘request’ object as its argument. This will
be an instance of `HttpRequest
<https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpRequest>`_,
which contains all the information about the request that the user's browser
sent. It then returns an `HttpResponse
<https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpResponse>`_
object as its return value. This contains all the data to be sent back to the
user's browser — HTTP headers and body, which is typically a web page. In our
case, we sent just the text "Hello world!". This request-response cycle is the
heart of the Django web framework.

In order to get Django to actually call our view function, we have to hook it
into a ``urlconf`` somewhere. This is covered in the `Django tutorial part 1
<https://docs.djangoproject.com/en/3.0/intro/tutorial01/#write-your-first-view>`_,
so I won't cover all the app layout stuff in detail — in brief, we'll have this
in our urls.py:


.. code-block:: python


   from django.urls import path

   from . import views

   urlpatterns = [
       path('hello/', views.hello_world, name='hello_world'),
   ]


In many cases, we want a single view function to actually match a family of URLs
which have some kind of parameter in them, and access that parameter in our view
function. Django has built-in support for this. Suppose we want to match URLs
like ``hello/XXX/`` where XXX could be any string. Then our URLconf becomes:

.. code-block:: python

   urlpatterns = [
       path('hello/<str:my_arg>', views.hello_world, name='hello_world'),
   ]

and our view signature:


.. code-block:: python

   def hello_world(request, my_arg):
       # etc


Now, for our classic web app, we are normally serving HTML i.e. web pages.
Further, our HTML normally has bits we want to insert into it — this is a
dynamic web site, not a static one — and we want to build it up in an ordered
way that will handle HTML escaping, and also provide a common set of page
elements (like navigation) for our different pages. So we'll almost always want
to use Django's template engine — covered in the `Django tutorial part 3
<https://docs.djangoproject.com/en/stable/intro/tutorial03/#write-views-that-actually-do-something>`_
. Instead of passing that "Hello world" string, we're going to have a
``hello_world.html`` template, and pass it some "context data" — any dynamic
information that needs to appear in the page.

So our revised view might look like this:

.. code-block:: python

   from django.http import HttpResponse
   from django.template import loader


   def hello_world(request):
       template = loader.get_template('hello_world.html')
       context = {}
       return HttpResponse(template.render(context, request))

Note that a template is not an essential part of a Django view — HTTP requests
and responses are the essential parts. Templates are just a way of building up
the body of the response. But for this kind of app, they are extremely common.
So, as the Django tutorial notes, there is a shortcut for this process of
loading a template, rendering it and putting it into a response — `render()
<https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#django.shortcuts.render>`_. With that, we can condense our view to this:

.. code-block:: python

   from django.http import HttpResponse
   from django.shortcuts import render


   def hello_world(request, my_arg):
       return render(request, 'hello_world.html', {})


The third parameter here is the empty context dictionary.

This is a great pattern for writing views. Django has one more trick up its
sleeve, however — `TemplateResponse
<https://docs.djangoproject.com/en/3.0/ref/template-response/#templateresponse-objects>`_.

The issue with just using ``render`` is that you get a plain ``HttpResponse``
object back that has no memory that it ever came from a template. Sometimes,
however, it is useful to have functions return a value that does remember what
it's "made of" — something that stores the template it is from, and the context.
This can be really useful in testing, but also if we want to something outside
of our view function (such as decorators or middleware) to check or even change
whats in the response before it finally gets 'rendered' and sent to the user.
We'll cover use case of this later in the guide.

For now, you can just accept that ``TemplateResponse`` is a more useful return
value than a plain ``HttpResponse``.

With that substitution, we've arrived at the pattern you'll want to memorise for
views:

.. code-block:: python

   from django.template.response import TemplateResponse

   def example_view(request, arg):
       return TemplateResponse(request, "example.html", {})


You need to know what each bit is, as described above. **But that is the end of
the lesson**. You can skip to the next part. Or you can even just stop reading —
you now know all the essentials of writing HTML views in Django.

You don't need to learn any of the CBV APIs - TemplateView, RedirectView,
ListView, DetailView, FormView, MultipleObjectMixin and all their inheritance
trees or method flowcharts. They will only make your life harder. Print out
their documentation, put in a shed — or rather, a warehouse `given how much
there is <https://ccbv.co.uk/>`_ — fill the warehouse with dynamite and `don't
look back <https://www.youtube.com/watch?v=Sqz5dbs5zmo>`_.


Discussion - boilerplate
------------------------

The CBV equivalent to the view I wrote above is as follows:

.. code-block:: python

   from django.views.generic import TemplateView

    class ExampleView(TemplateView):
        template_name = "example.html"


.. code-block:: python

   urlpatterns = [
       path('example/<str:arg>/', views.ExampleView.as_view(), name='example_name'),
   ]


Why is this worse than the FBV?

First of all, **it's barely any shorter**.

CBVs have some massive downsides, which include a huge amount of complexity. In
the face of this, the major selling point of CBVs is that they are supposed to
remove duplication and boilerplate. But, we only had 2 lines to begin with, and
we still have 2 lines. We could just about squeeze it to one long one using
``TemplateView.as_view(template_name="example.html")`` but that's not how you
normally write it.

Given the downside, I expected the upside to be a lot more convincing. Maybe
it's better when it comes to DetailView etc? We'll see about that. (TODO)

But let's add a more realistic situation – we actually want some context data.
Let's say it's just a single piece of information, like a title, using some
generic 'page' template.

FBV version:

.. code-block:: python

   def my_view(request):
       return TemplateResponse(request, "page.html", {
           'title': 'My Title',
       })

CBV version:

.. code-block:: python

   class MyView(TemplateView):
       template_name = "page.html"

       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           context['title'] = 'My Title'
           return context

For this trivial task, we've had to define a new, bulky method, and now we find
**it's a lot longer** than the FBV, in addition to being much more complex and
indirect.

In fact, you'll find many people don't actually start with the bare
``TemplateView`` subclass. If you `search GitHub
<https://github.com/search?q=get_context_data&type=Code>`_ for
``get_context_data``, you'll find hundreds and hundreds of examples that look
like this:

.. code-block:: python

   class HomeView(TemplateView):
       # ...

       def get_context_data(self):
           context = super(HomeView, self).get_context_data()
           return context

This doesn't make much sense, until you realise that people are using
boilerplate generators/snippets to create new CBVs — such as `this for emacs
<https://github.com/pashinin/emacsd/blob/c8e50e6bb573641f3ffd454236215ea59e4eca13/snippets/python-mode/class>`_
and `this for vim
<https://github.com/ppiet/dotfiles/blob/e92c4b31d253e48027b72335f071281352b05f01/vim/UltiSnips/python.snippets>`_,
and `this for Sublime Text
<https://github.com/mvdwaeter/dotfiles/blob/60673ae395bf493fd5fa6addeceac662218e1703/osx/Sublime%20Text/get_context_data.sublime-snippet>`_.

In other words:

* The boilerplate you need for a basic CBV is bigger than for an FBV
* It's so big and tedious that people use snippets library to write it for them.

Discussion - starting points
----------------------------

Some people will say we can use the CBV for the really simple cases, and then
switch to FBV later as needed. But in reality that doesn't happen... TODO


And the CBV was a bad starting point. With the FBV, we just added the context
data right into the context dictionary we had already created. There was an
obvious place for the thing we wanted to add, because the logic of the view
isn't hidden away somewhere in a base class.

With the CBV, if you start with the minimal version, you have to do a lot more
work to add a basic customisation.

You find this again and again with CBVs. As soon as you need any logic, you have
to start defining methods, which brings you pain:

* You've got to know which methods to define, which involves knowing this
  massive API.
* You could easily get it wrong in a way which introduces terrifying bugs. (TODO
  link)
* You've got to add the method, which is a whole bunch of boilerplate.
