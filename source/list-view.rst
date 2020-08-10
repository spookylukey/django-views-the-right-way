Displaying a list of objects
============================

To continue the example of an e-commerce site, let's implement our product
listing page. Our first version of the code is just this:

.. code-block:: python

   def product_list(request):
       return TemplateResponse(request, 'shop/product_list.html', {
           'products': Product.objects.all(),
       })

A typical product listing page normally would have some more requirements, often
including at least pagination. Django comes with a helpful `Paginator
<https://docs.djangoproject.com/en/stable/topics/pagination/#using-paginator-in-a-view-function>`_
class, with helpful docs showing you how to use it. With that added, you have
something like this:

.. code-block:: python

   from django.core.paginator import Paginator

   def product_list(request):
       products = Product.objects.all()
       paginator = Paginator(products, 5)  # Show 5 products per page.
       page_number = request.GET.get('page')
       page_obj = paginator.get_page(page_number)
       return TemplateResponse(request, 'shop/product_list.html', {
           'page_obj': page_obj,
       })

That's basically it! Your real view might have additional needs, like filtering
and ordering. These can be handled by responding to query string parameters and
modifying your ``products`` QuerySet above.

There is a bit of boilerplate here for doing pagination. If you have a
standardised convention of using ``page`` as your query string parameter for
paging, you could pull some of this boilerplate out into a utility like
``paged_object_list_context`` (left as an exercise for you) to produce something
a bit shorter:

.. code-block:: python

   def product_list(request):
       products = Product.objects.all()
       context = {}
       context.update(paged_object_list_context(request, products, paginate_by=5))
       return TemplateResponse(request, 'shop/product_list.html', context)


Next up: :doc:`delegation`


Discussion: Discovering re-usable units of code
-----------------------------------------------

I very deliberately left “write some code yourself” as an exercise. Adding these
kind of utilities to your code is what every developer should learn to do, and
in a project you would expect to have a small library of this kind of thing that
is specific to your project and encapsulates your own patterns and conventions.
This is far superior to contorting your code with method overrides that are
necessary only because of the structure handed to you by someone else.

Yes, using ``paged_object_list_context`` is very slightly longer than just
adding a ``paginate_by`` attribute to a ``ListView``. But the benefits are huge
— you stay in full control of your view function and it remains readable and
extremely easy to debug or further customise. You also have a utility that is
separately testable, with a well-defined interface that means its very unlikely
to interact badly with the different contexts you might use it in.

The `ListView alternative
<https://docs.djangoproject.com/en/stable/topics/pagination/#paginating-a-listview>`_
for this code is tempting, but it is a short-sighted laziness. Any real world
view will quickly develop enough logic that you lose even in terms of code
length, and much more so in terms of code complexity.

As well as ``paged_object_list_context``, we should also mention ``Paginator``,
which is a great example of the kind of re-usable functionality that you should
be looking for in your own projects. It has a single responsibility — it handles
pagination. It has a clearly defined interface that can be documented and
understood, and separately tested, and used outside of a web context.

I have various similar utility functions and classes in my own Django projects:
things like ``ExcelFormatter`` and ``OdsFormatter`` (simple abstractions over
creating spreadsheets, that share an interface so that the user can choose
between XLS or ODS files); small HTTP-level utilities that do redirections or
closing of popups; small glue utilities that encapsulate some small convention
or decision that needs to be applied in several places.

In my experience, these are the kinds of things that are **less likely** to come
out if you use mixins for re-using functionality. Mixins encourage big classes
with many methods that hide the layers of your code. I encourage you again to
watch `Brandon Rhode's analysis <https://youtu.be/S0No2zSJmks?t=3116>`_ of the
Python stdlib ``socketserver`` library, or his section on mixins in his article
on `The Composition Over Inheritance Principle
<https://python-patterns.guide/gang-of-four/composition-over-inheritance/#dodge-mixins>`_.

