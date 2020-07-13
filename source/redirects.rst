Redirects
=========

To implement redirects in Django, you need to know how they work in HTTP.

In HTTP, a redirect is an HTTP response with a status code in the 300-399 range,
and a ``Location`` header that tells a browser which URL to go to. If your view
returns a response like this, the browser will immediately make another request,
to the specified URL.

The `different 3XX codes have different meanings
<https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#3xx_Redirection>`_ -
make sure you use the right one.

That is 95% of what you need to know at the HTTP level. In Django, the most
common functionality has been wrapped up for you in `HttpResponseRedirect
<https://docs.djangoproject.com/en/3.0/ref/request-response/#django.http.HttpResponseRedirect>`_.

So this view, for example, does an unconditional, temporary redirect:

.. code-block:: python

   def my_view(request):
       return HttpResponseRedirect('/other/url/', status=307)

In addition, Django provides some shortcuts:

* `redirect
  <https://docs.djangoproject.com/en/3.0/topics/http/shortcuts/#redirect>`_, a
  utility that returns an HTTP response object and has built-in logic for
  redirecting to named views, and other things.

* `RedirectView
  <https://docs.djangoproject.com/en/3.0/ref/class-based-views/base/#redirectview>`_
  — a class that provides an entire view that does redirection, and has a few
  neat features like being able to look up view by name, including arguments
  from a path, and also copy the query string. I recommend using this if the
  only thing that your view does is a redirect, otherwise just use
  ``HttpResponse`` objects directly.

  For example, if you have an old URL at ``old-path/<number>/`` and want to
  permanently redirect it to ``new-path/<number>/``, you can use do it from
  ``urls.py`` like this:

   .. code-block:: python


      urls = [
          path('old-path/<int:pk>/', RedirectView.as_view(
              pattern_name='my_view',
              permanent=True,
              query_string=True,
          ),
          path('new-path/<int:pk>/', views.my_view, name='my_view'),
      ]


Discussion: configuration in urls.py
------------------------------------

If you can reduce a set of common functionality down to something that can be
configured directly in ``urls.py``, I think this is quite a nice pattern for
making very simple views.

For redirects, ``RedirectView`` can work nicely. In my opinion once you get more
complicated and need other logic, a function that uses ``HttpResponse`` objects
will serve you better, or perhaps a function that **delegates** to
``RedirectView``, rather than subclassing it.

Delegating to ``RedirectView`` is not perhaps the most obvious thing, due to how
``as_view``. It looks like this:

.. code-block:: python

   # urls.py
      urls = [
          path('old-path/<int:pk>/', views.my_old_view)
          path('new-path/<int:pk>/', views.my_view, name='my_view'),
      ]

.. code-block:: python

   def my_old_view(request, pk):
       return RedirectView.as_view(
              pattern_name='my_view',
              permanent=True,
              query_string=True,
       )(request, pk)


We should note that the pattern of defining views entirely within ``urls.py``
can be achieved just as well using functions as well as ``View`` sub-classes.

Two methods:

* view factory

* extra keyword arguments in urls.py

TODO
