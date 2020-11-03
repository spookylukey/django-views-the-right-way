Redirects
=========

To implement redirects in Django, you need to know how they work in HTTP.

In HTTP, a redirect is an HTTP response with a status code in the 300-399 range,
and a ``Location`` header that tells a browser which URL to go to. If your view
returns a response like this, the browser will immediately make another request,
to the specified URL.

The `different 3XX codes have different meanings
<https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#3xx_Redirection>`_ —
make sure you use the right one.

That is 95% of what you need to know at the HTTP level. In Django, the most
common functionality has been wrapped up for you in `HttpResponseRedirect
<https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpResponseRedirect>`_.

So this view, for example, does an unconditional, temporary redirect:

.. code-block:: python

   def my_view(request):
       return HttpResponseRedirect('/other/url/', status=307)

In addition, Django provides some shortcuts:

* `redirect
  <https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#redirect>`_, a
  utility that returns an HTTP response object and has built-in logic for
  redirecting to named views, and other things.

* `RedirectView
  <https://docs.djangoproject.com/en/stable/ref/class-based-views/base/#redirectview>`_
  — a class that provides an entire view that does redirection, and has a few
  neat features like being able to look up view by name, including arguments
  from a path, and also copy the query string. I recommend using this if the
  only thing that your view does is a redirect. Otherwise just use
  ``HttpResponse`` objects directly.

  For example, if you have an old URL at ``/old-path/<number>/`` and want to
  permanently redirect it to ``/new-path/<number>/``, you can use do it from
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


That's it! On to :doc:`forms`.


Discussion: CBV configuration in urls.py
----------------------------------------

If you can reduce a set of common functionality down to something that can be
configured directly in ``urls.py``, I think this is quite a nice pattern for
making very simple views.

For redirects, ``RedirectView`` can work nicely. In my opinion once you get more
complicated and need other logic, a function that uses ``HttpResponse`` objects
will serve you better, or perhaps a function that **delegates** to
``RedirectView``, rather than subclassing it.

Delegating to ``RedirectView`` is not perhaps the most obvious thing, due to how
``as_view()`` works. It looks like this:

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


Discussion: FBV configuration in urls.py
----------------------------------------

We should note that the pattern of defining views entirely within ``urls.py``
can be achieved just as well using functions as with ``View`` sub-classes.

Here are two methods for doing this:

Additional keyword parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See the docs for `passing extra options to view functions
<https://docs.djangoproject.com/en/stable/topics/http/urls/#views-extra-options>`_.

So, for example, if we want to reproduce the functionality of
``RedirectView``, complete with “configure it within urls.py”, we could have a
view function like this:

.. code-block:: python

    def do_redirect(request, *args, pattern_name=None, permanent=False, query_string=True, **kwargs):
       url = reverse(pattern_name, args=args, kwargs=kwargs)
       # More of ``RedirectView`` logic here, using ``permanent`` and
       # ``query_string`` etc.
       return HttpResponseRedirect(url)

.. code-block:: python

   # urls.py

    urls = [
        path('old-path/<int:pk>/', do_redirect, {
            'pattern_name': 'my_view',
            'permanent': True,
            'query_string': True,
        }),
    ]

Mass-produced views — “view factories”
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One of the issues with the above is you have a possibility of a clash between
the contents of the configured ``kwargs`` and the other keyword arguments the
view accepts. We can solve this using a function that returns a view function
(in the same way that ``RedirectView.as_view()`` returns a view function). I call
this a “view factory”. The outer function has keyword arguments for configuring
the view, the inner function is the view itself:

.. code-block:: python

    def make_redirector(pattern_name=None, permanent=False, query_string=False):
       def redirector(request, *args, **kwargs):
           url = reverse(pattern_name, args=args, kwargs=kwargs)
           # More of ``RedirectView`` logic here, using ``permanent`` and
           # ``query_string`` etc.
           return HttpResponseRedirect(url)
       return redirector

.. code-block:: python

   # urls.py

    urls = [
        path('old-path/<int:pk>/', make_redirector(
            pattern_name='my_view',
            permanent=True,
            query_string=True,
        )),
    ]

This technique of “mass producing” view functions can be used to great effect in
many other situations, especially if you have lots of extremely similar views
that just need to be differently configured.

Unlike the example above where the view function accepts ``*args, **kwargs``,
the inner view function can have a signature that is as specific as you need it
to be, so this will play well with :ref:`type-checked parameters
<type-checked-parameters>` if you want it to.
