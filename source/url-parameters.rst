URL parameters in views
=======================

As described in the `Django tutorial for views
<https://docs.djangoproject.com/en/stable/intro/tutorial03/>`_ and the `request
handling docs
<https://docs.djangoproject.com/en/stable/topics/http/urls/#how-django-processes-a-request>`_,
if you want to capture part of a URL to be used in a view function, you can do
it by configuring your URLs.

Let's say we have an e-commerce site where we want to display products on
individual pages. We want ``/product/`` to be the prefix for all these pages,
and the next part to be the “slug” for the product — a URL-friendly version of
the name (e.g ``white-t-shirt`` instead of "White T-Shirt").

We can do that as follows:

.. code-block:: python

   # urls.py

   from django.urls import path

   from . import views

   urlpatterns = [
       path('products/<slug:slug>/', views.product_detail, name='product_detail'),
   ]

.. code-block:: python

   # views.py

   def product_detail(request, slug):
       return TemplateResponse(request, 'shop/product_detail.html', {})


Note how the ``slug`` parameter has to be added to view function signature, as
well as in the URL conf. In the URL pattern, the first ``slug`` is the path
converter type. The second ``slug`` is the name of the parameter in the
``product_detail`` view, and we could have chosen something different.

If you don't modify the view like this, it simply won't work — you'll get an
exception, because Django will attempt to call your function with parameters
that your function doesn't accept, which is an error in Python.

If you are used to CBVs, this is one of the more obvious differences. With a
CBV, you don't have to modify the function signature — because there isn't one
to modify. But with the CBV you have to write more code to get hold of that
parameter.

Be sure to check the Django docs about `path converters
<https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters>`_ for
the different kind of things you might add into your URLs. If you are into type
hints, also see below for tips on how you can enhance this pattern.

Otherwise, onto :doc:`detail-view`, where we will actually use the ``slug``
parameter.


Discussion: Generic code and function signatures
------------------------------------------------

Django's URL-to-function dispatching mechanism is very elegant and powerful,
converting parts of the URL into a function parameter that's just ready and
waiting to be used.

With the `path converters
<https://docs.djangoproject.com/en/stable/topics/http/urls/#path-converters>`_
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

Now, you no longer have to check the URLconf to be sure of the type of the
argument, it's right there in your function.

The elegance of URL parameters as part of the function signature contrasts with
CBVs, where you have to do extra work get to hold of the parameter:

  .. code-block:: python

     name = self.kwargs['name']


.. _type-checked-parameters:

Discussion: Type-checked parameters
-----------------------------------

Of course, if we add type hints, wouldn't it be even cooler if we could
automatically ensure that the URL configuration matched the view function, both
in terms of names and types of arguments?

`OK, you've persuaded me, go on then!
<https://github.com/spookylukey/django-views-the-right-way/blob/master/code/the_right_way/url_checker.py>`_
(This code is pretty functional as it is already, and I've enjoyed using it in
my projects. But needs a fair amount of work to be a proper package. If anyone
would like to take that on as a project, please go ahead, and I'll link it here!
You can play around with it by checking out the `example code
<https://github.com/spookylukey/django-views-the-right-way/tree/master/code>`_
that accompanies this guide).

Unfortunately, you lose out here if you are using CBVs, because you don't have a
signature that you can decorate with type hints. The signature that is
externally visible for your view is ``view(request, *args, **kwargs)``, so it is
impossible for the above type-checking code to work.

The fundamental issue here is **generic code**. Generic code is useful precisely
because of its breadth — it can be used in a wide range of situations. However,
the downside of generic code is that it must cater for every situation, instead
of just yours. So CBVs have to have a ``kwargs`` dictionary, which isn't really
what you wanted. Generic code by definition lacks the personal touch.

Of course, there can be times when the advantages outweigh the disadvantages.
But make sure you know what you are missing!
