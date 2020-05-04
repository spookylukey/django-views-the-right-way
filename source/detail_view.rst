Displaying a single database object
===================================

To continue :doc:`our example <url_parameters>`, we want to display individual
product pages, looking them up from a product slug that will be part of the URL.

This requires knowing how to use ``QuerySet``, and in particular the
`QuerySet.get
<https://docs.djangoproject.com/en/3.0/ref/models/querysets/#django.db.models.query.QuerySet.get>`_
method. Assuming we have a ``Product`` model with a `SlugField
<https://docs.djangoproject.com/en/3.0/ref/models/fields/#slugfield>`_ named
``slug``, the code looks like:

.. code-block:: python

   product = Product.objects.get(slug=product_slug)

However, this could throw a ``Product.DoesNotExist`` exception, which we need to
catch. Instead of crashing, we should instead show a 404 page to the user. We
can do this easily using Django's `Http404
<https://docs.djangoproject.com/en/3.0/topics/http/views/#django.http.Http404>`_
exception.

The combined code would look like this:

.. code-block:: python

   try:
       product = Product.objects.get(slug=product_slug)
   except Product.DoesNotExist:
       raise Http404('Product not found, please check the link')

This is perfectly adequate code that you should not feel in any way embarrassed
about. However, this pattern comes up so often in Django apps that there is a
shortcut for it — `get_object_or_404
<https://docs.djangoproject.com/en/3.0/topics/http/shortcuts/#get-object-or-404>`_.
This combines the above logic for, so that you can just write:


.. code-block:: python

   # imports
   from django.shortcuts import get_object_or_404

   # in the view somewhere
   product = get_object_or_404(Product.objects.all(), slug=product_slug)

If the only thing we are going to do with the product object is render it in a
template, the final, concise version of our view will look like this:

.. code-block:: python

   def product_details(request, product_slug):
       return TemplateResponse(request, 'products/product_detail.html', {
           'product': get_object_or_404(Product.objects.all(), slug=product_slug),
       })


That's it! Next up: :doc:`list_view.rst`

Discussion: Comparison to DetailView
------------------------------------

If we used `DetailView
<https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-display/#detailview>`_
instead, what would we have?

.. code-block:: python

   class ProductDetailView(DetailView):
       template_name = 'products/product_detail.html'
       queryset = Product.objects.all()
       context_object_name = 'product'

We'd also either have to change the name of the named group in our URLconf like
this:

.. code-block:: python

   urlpatterns = [
       path('products/<slug:slug>/', views.product_detail, name='product_detail'),
   ]

...or, add ``slug_url_kwarg = 'product_slug'`` to our class.

This CBV is shorter, at least in terms of token count, than my version, although
not by much. It suffers from the common disadvantages that CBVs have, such as by
default not having an easy way to add extra data into the context, which makes a
big difference. The essential logic ``DetailView`` adds is equivalent to the
single line ``'product': get_object_or_404(Product.objects.all(),
slug=product_slug),`` in my FBV, so there is a question about how much value for
money you are getting.

You could make it more concise, but not in good ways. Each alternative way to
write this brings up some issues that I'll discuss in turn, and finally I'll
look at one of the biggest issues with CBVs — the layering violations they
encourage.


Discussion: ``template_name`` — convention vs configuration
-----------------------------------------------------------

The first way we could shorten the CBV version is by omitting ``template_name``.
The generic CBVs have some logic built in to derive a template name from the
model name and the type of view, which in this case would result in
``products/product_detail.html``, on the assumption that the 'app' the model
lived in was called ``products``.

This kind of behaviour is called “convention over configuration”. It's popular
in Ruby on Rails, much less so in Python and Django, partly due to the fact that
it is pretty much directly against the “Zen of Python” maxim “Explicit is better
than implicit”. This is a good thing, because convention over configuration is
one of the those things that seems great when you are writing code, and is often
a nightmare when it comes to maintenance.

Consider the maintenance programmer who comes along and needs to make
modifications to a template. We do not assume a maintenance programmer is an
expert in your framework, or in this particular codebase. They may be a junior
developer, or they may be a more senior one who just has less experience in this
particular framework. (If you are not expecting your project is going to be
taken on by people like this, you really should).

They discover they need to change ``products/product_detail.html``, and set
about looking for the corresponding view code. Where can they find it?

If we have used “convention over configuration”, they have to:

1. Know all the conventions that could end up referencing this template.

2. Look for any ``DetailView``, find the model it is using, and check to see if
   it matches ``product.Product``. And also any further subclasses of
   ``DetailView`` etc.

3. In addition, they will have to do a grep for code that references
   ``products/product_detail.html``, because as well as ``DetailView`` there
   could of course be other code just using the template directly.

Step 1 is especially problematic. Attempting to document all the conventions in
your code base probably won't do any good. If someone doesn't know the
conventions, they won't think to read docs, because unknown conventions are
unknown unknowns — they are like the surprising things in a foreign culture,
things that you don't know that you don't know until you trip up over them.

Step 2 is a bit annoying, and harder to do than a simple grep.

Finally, you still need to step 3 — which is the only step needed if you didn't
have “convention over configuration” to deal with.

So these typing-savers hurt maintenance, and therefore hurt your project because
most software development is maintenance. If you do use CBVs, do yourself a
favour and always add ``template_name``, even if you are sticking to the naming
convention as I have done here.

The same “convention over configuration” logic is also present in the way
``DetailView`` looks up its object: it looks for a named URL parameter called
``pk``, and then one called ``slug`` if ``pk`` doesn't exist, and finds your
object using those parameters. Neat shortcuts, but leave a maintenance developer
completely stumped as to how or why this code works, or where you should start
if you want different behaviour. You have to read the docs in detail.

Proponents of Ruby-on-Rail-style “convention over configuration” will point to
some super-verbose Java framework as an example of all the boilerplate you can
save. But this is a false dichotomy. With dynamic languages, we can very often
avoid as much configuration as we want to. We should make sure we restrain
ourselves if we are going to make code harder maintain for the sake of saving a
tiny bit of typing.

Discussion: static vs dynamic?
------------------------------

We could shorten the CBV by changing ``queryset = Product.models.all()`` to
``model = Product``, which, in this case will do the same thing.

But it will hurt the maintenance programmer. Suppose the requirement comes along
to only allow “visible” products to be seen in this view, which has been
encapsulated in a custom QuerySet method ``visible()``, so they can write
``Product.objects.visible()``. The maintenance programmer has to know they can
switch ``model = <model>`` to ``queryset = <queryset>`` — they have to know the
API of ``DetailView`` very well, instead of just being able to modify the code
in front of them.

(For the same reason, in my FBV above I wrote
``get_object_or_404(Product.objects.all(), …)`` instead of
``get_object_or_404(Product, …)`` which is also supported by the shortcut
function).

If, however, the queryset needed depends on the ``request`` object, the
programmer will have to instead define ``get_queryset()`` to get access to the
request data and dynamically respond to it, rather than have a static definition
on the class.

This means you now have 3 different ways of doing the same thing, and you have
to be comfortable switching between them.

There is also a subtlety with querysets: suppose your
``ProductQuerySet.visible()`` method goes from being a simple filter on a field
to gaining some additional time based logic e.g.:

.. code-block:: python

   def visible(self):
       return self.filter(visible=True).exclude(visible_until__lt=date.today())

If you have ``queryset = Products.objects.visible()`` attribute, rather than a
``get_queryset()`` method, due to the fact that this is a class attribute which
gets executed at module import time, the ``date.today()`` call happens when your
app starts up, not when your view is called. So it seems to work, but you a get
a surprise on the second day in production!

None of these are massive issues — they are small bits of friction, but these
things do add up, and it happens that all of them are avoided by the way in
which FBVs are constructed.

On the other hand, there are some benefits with the statically defined class
attributes, in addition to being more concise and declarative. For example, the
Django admin classes has attributes like ``fieldsets`` for the static case, with
``get_fieldsets()`` for the dynamic case. If you use the attribute, the Django
checks framework is able to check it for you before you even access the admin.

Some of the trade-offs here also depend on how often the static attribute is
enough, compared to how often you need the dynamic version.


Discussion: generic code and variable names
-------------------------------------------

A third way to shorten the CBV is to omit ``context_object_name``. In that case,
instead of having our ``Product`` object having the name ``product`` in the
template, it would have the name ``object``.  Don't do that! ``object`` is
a very choice of name for something unless you really have no idea what type it
is, and is going to hurt maintenance in various ways.

It's good that ``context_object_name`` exists, but unfortunate that it is
optional. For the instance variable on the view, however, things are worse — it
is always ``self.object``. This is probably a good thing when you are writing
CBVs, but a bad thing when doing maintenance.

The issue here is again the problem of generic code. For the view code, it's
unusually tricky problem — you are inheriting from generic code that doesn't
know a better name than ``object``. However, **your** code is not generic, and
could have chosen a much better name, but your code wasn't in charge.

This is a problem that is specific to class based generic code. If you write
generic **function** based generic code (see TODO), the problem doesn't exist,
because you don't inherit local variable names.

Discussion: layering violations — shortcuts vs mixins
-----------------------------------------------------

``get_object_or_404`` is an example of a “shortcut” function. `Django's docs for
shortcut functions
<https://docs.djangoproject.com/en/3.0/topics/http/shortcuts/>`_ defines them
like this:

    The package django.shortcuts collects helper functions and classes that
    “span” multiple levels of MVC. In other words, these functions/classes
    introduce controlled coupling for convenience’s sake.

And the `tutorial
<https://docs.djangoproject.com/en/3.0/intro/tutorial03/#a-shortcut-get-object-or-404>`_
has a helpful comment about them:

    **Philosophy**

    Why do we use a helper function ``get_object_or_404()`` instead of
    automatically catching the ``ObjectDoesNotExist`` exceptions at a higher level,
    or having the model API raise ``Http404`` instead of ``ObjectDoesNotExist?``

    Because that would couple the model layer to the view layer. One of the
    foremost design goals of Django is to maintain loose coupling. Some
    controlled coupling is introduced in the ``django.shortcuts`` module.


An important property of well designed shortcut functions is that they only have
local effects on your code. For example, when we introduced
``get_object_or_404``, we replaced 4 lines in the original function and saved
some typing, but there were no effects on the external behaviour of that view
function, or on the interface of any function or method. If you want
“controlled” coupling that doesn't hurt your code base, this is vital.

I find looking at views — whether CBVs or FBVs — through the lens of “layering”
is slightly tricky.

We could look at the list of methods on ``DetailView``, which includes the
following:

* ``dispatch``
* ``get``
* ``options``
* ``get_context_data``
* ``get_context_object_name``
* ``get_object``
* ``get_queryset``
* ``get_slug_field``
* ``get_template_names``
* ``http_method_not_allowed``
* ``render_to_response``
* ``setup``

These methods certainly span a more than one layer. We've got methods that deal
very much with the HTTP layer (dispatching on different verbs, extracting data
out of a URL), and others that deal with retrieving database objects and others
with templates.

On the other hand, you could say the same about any view function. By their very
nature, views have to work in terms of HTTP requests and responses, but they
also have to arrange to get data from the database (or somewhere), and this CBV
is just a class-based equivalent to the view function.

Perhaps a better way is to think about it is the “the single responsibility
principle” for class design. Through that lens, this class doesn't look very
good at all. It has far too many different directions you might want to take it.

But the most convincing to me is too look what happens when you carry on this
pattern.

I recently came across a family of views that had the following methods:

* TODO

These views generate Excel spreadsheets. You'll see it has a whole bunch of
methods that relate only to XLS generation, with others that relate to HTTP
handling, and other to retrieving data the from the database. As you can guess,
the implementation was significantly complicated by its hybrid nature.

What is needed is a separate set of classes that handle just XLS generation,
which should then be used by our view functions (or classes). Such properly
decoupled code will make your life much easier — so that, for instance, when you
realise that you need to generate these XLS reports offline, completely outside
the context of a web request, it will be a very easy task. Or so that you can
test some aspect of the XLS generation without having to set up a web request.

So where did the design go wrong? Look back at the views provided by Django, and
you'll see this design is simply carrying on the same pattern.

This is a fundamental difference between a shortcut and a mixin. The shortcut is
a convenient way to reduce some boilerplate with only local effects on your
code, while mixins set up a pattern for your code which determines its structure
— and not in a good way. The coupling becomes totally out of control.

Brandon Rhodes has `an excellent discussion on mixins in his talk on Python
anti-patterns <https://youtu.be/S0No2zSJmks?t=3095>`_. He also specifically
calls out Django CBV mixins (though manages to avoid saying ‘Django’), and in my
opinion his analysis is spot on.
