URL parameters in views
=======================

As described in the `Django tutorial for views
<https://docs.djangoproject.com/en/3.0/intro/tutorial03/>`_ and the `request
handling docs
<https://docs.djangoproject.com/en/3.0/topics/http/urls/#how-django-processes-a-request>`_,
if you want to capture part of a URL to be used in a view function, you can do
it by configuring your URLs.

Let's say we have an e-commerce site where we want to display products on
individual pages. We want ``/product/`` to be the prefix for all these pages,
and the next part to be the “slug” for the product — a URL-friendly version of
the name (e.g ``white-t-shirt`` instead of "White T-Shirt").

We can do that as follow:

.. code-block:: python

   # urls.py

   from django.urls import path

   from . import views

   urlpatterns = [
       path('products/<slug:product_slug>/', views.product_detail, name='product_detail'),
   ]

.. code-block:: python

   # views.py

   def product_detail(request, product_slug):
       return TemplateResponse(request, 'products/product_detail.html', {})


Note how the ``product_slug`` parameter has to be added to view function
signature, as well as in the URL conf. (We didn't actually use this
``product_slug`` parameter yet, that will be covered in the next section). If
you don't modify the view like this, it simply won't work — you'll get an
exception, because Django will attempt to call your function with parameters
that your function doesn't accept, which is an error in Python.

If you are used to CBVs, this is one of the more obvious differences. With a
CBV, you don't have to modify the function signature — because there isn't one
to modify. But with the CBV you have to write more code to get hold of that
parameter.

Be sure to check the Django docs about `path converters
<https://docs.djangoproject.com/en/3.0/topics/http/urls/#path-converters>`_ for
the different kind of things you might add into your URLs. If you are into type
hints, also see below for tips on how you can enhance this pattern.

Otherwise, onto :doc:`detail-view`.

Discussion: Generic code and function signatures
------------------------------------------------

Django's URL-to-function dispatching mechanism is very elegant and powerful,
converting parts of the URL into a function parameter that's just ready and
waiting to be used.

With the `path converters
<https://docs.djangoproject.com/en/3.0/topics/http/urls/#path-converters>`_
functionality added in 2.0 it got a whole lot better, because it will
automatically convert things to the correct type for you, reducing the amount of
type conversion you have to do in your function.

You can additionally make use of this by adding type hints:

.. code-block:: python

   def product_detail(request, name: str):
       pass  # etc

   # OR
   def product_detail(request, pk: int):
       pass  # etc

Now, you now longer have to check the URLconf to be sure of the type of the
argument, it's right there in your function.

Of course, wouldn't it be even cooler if we could automatically ensure that the
URL configuration matched the view function, both in terms of names and types of
arguments?

`OK, you've persuaded me, go on then!
<https://github.com/spookylukey/django-views-the-right-way/blob/master/code/the_right_way/url_checker.py>`_
(This code is pretty functional as it is already, but needs a fair amount of
work to be a proper package. If anyone would like to take that on as a project,
please go ahead, and I'll link it here! You can play around with it by checking
out the `example code
<https://github.com/spookylukey/django-views-the-right-way/tree/master/code>`_
that accompanies this guide).

Unfortunately, you lose a number of these advantages if you are using CBVs:

* The code to get hold of the parameter is bulkier:

  .. code-block:: python

     name = self.kwargs['name']

* It can be easy to make a typo here, without it being immediately obvious, especially
  if for some reason you write it like this:

  .. code-block:: python

     name = self.kwargs.get('name', None)

  If you use functions, you will almost always get an immediate error if your
  URL doesn't match your function signature.

* You don't have a signature that you can decorate with type hints. The
  signature that is externally visible for your view is ``view(request, *args,
  **kwargs)``, so it is impossible for the above code to type check, or check
  that you are attempting to get the right thing out of ``kwargs``.

The fundamental issue here is **generic code**. Generic code is useful precisely
because of its breadth — it can be used in a wide range of situations. However,
the downside of generic code is that it must cater for every situation, instead
of just yours. So it has to have a dictionary ``kwargs``, which isn't really
what you wanted. Generic code by definition lacks the personal touch.

Of course, there can be times when the advantages outweigh the disadvantages.
But make sure you know what you are missing!
