Custom logic at the start — delegation
======================================

The next few pages address the problem of needing to re-use some logic from one
view in another view. We've thought about how we can use utility functions and
classes, but sometimes these don't cut it — sometimes the majority of the body
of the view needs to be re-used. How can we do that with FBVs?

Continuing our :doc:`example <list-view>` of a list of products, let's add a
variation. As well as the main product list page, we've also got a “special
offers” page — or rather, a set of them, because we have a ``SpecialOffer``
model that allows us to have many different ones. Each of these pages needs to
display some details about the special offer, and then the list of products
associated with that offer. Our feature requirements say this product list
should have **all** the features of the normal product list (filtering, sorting
etc.), so we want to re-use the logic as much as possible.

So our view will need to do two things: it will show a single object, and also
shows a list. The answer of how to do two things with FBVs is: **do two
things**. No special tricks needed for that. Let's start with a simple version
of our view:

.. code-block:: python

   # urls.py

   from . import views

   urlpatterns = [
       path('special-offers/<slug:slug>/', views.special_offer_detail, name='special_offer_detail'),
   ]

.. code-block:: python

   # views.py

   def special_offer_detail(request, slug):
       special_offer = get_object_or_404(SpecialOffer.objects.all(), slug=slug)
       return TemplateResponse(request, 'shop/special_offer_detail.html', {
           'special_offer': special_offer,
           'products': special_offer.get_products(),
       })

I've assumed the ``SpecialOffer.get_products()`` method exists and returns a
``QuerySet``. If you have an appropriate ``ManyToMany`` relationships the
implementation might be as simple as ``return self.products.all()``, but it
might be different.

But now we want to change this view to re-use the logic in our normal
``product_list`` view, whether it is filtering/sorting/paging or anything else
it has built up by now (which I'll represent using the function
``apply_product_filtering()`` below). How should we do that?

One way would be to do what we did in :doc:`common-context-data` — wrap the body
of the existing ``product_list`` view into a function that takes some parameters
and returns the data to be added to the context. However, in some cases that
interface won't work. For instance, if the view decides that in some cases it
will return a completely different kind of response — perhaps a redirection, for
example — then it won't fit into that mould.

Instead we'll use what I'm going to call **delegation** — our entry-point view
will delegate the rest of the work to another function.

To create this function, look at our old ``product_list`` view and apply
`parameterisation
<https://www.toptal.com/python/python-parameterized-design-patterns>`_. The
extra parameters we need to pass are: the product list ``QuerySet``; the name of
the template to use; and something to pass in some extra context. With those in
place we can easily pull out a ``display_product_list`` function, and call it
from our two entry-point view functions.


.. code-block:: python

   def product_list(request):
       return display_product_list(
           request,
           queryset=Product.objects.all(),
           template_name='shop/product_list.html',
       )


   def special_offer_detail(request, slug):
       special_offer = get_object_or_404(SpecialOffer.objects.all(), slug=slug)
       return display_product_list(
           request,
           context={
               'special_offer': special_offer,
           },
           queryset=special_offer.get_products(),
           template_name='shop/special_offer_detail.html',
       )


   def display_product_list(request, *, context=None, queryset, template_name):
       if context is None:
           context = {}
       queryset = apply_product_filtering(request, queryset)
       context.update(paged_object_list_context(request, queryset, paginate_by=5))
       return TemplateResponse(request, template_name, context)


.. note::

   For those unfamiliar with the signature on ``display_product_list``:

   * the arguments after ``*`` are “`keyword only arguments
     <https://lukeplant.me.uk/blog/posts/keyword-only-arguments-in-python/>`_”.
   * ``queryset`` and ``template_name`` lack defaults (because we don't have any
     good defaults) which forces calling code to supply the arguments.
   * for ``context`` we do have a sensible default, but also need to avoid the
     `mutable default arguments gotcha
     <https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments>`_,
     so we use ``None`` in the signature and change to ``{}`` later.

At the template level, we'll probably do a similar refactoring, using `include
<https://docs.djangoproject.com/en/stable/ref/templates/builtins/#include>`_ to
factor out duplication.

That's it! See below for some more discussion about how this delegation pattern
might evolve. Otherwise, onto :doc:`dependency-injection`.

.. _function-based-generic-views:

Discussion: Function based generic views
----------------------------------------

What happens if you keep going with this parameterisation pattern? Let's say you
have not one model, but lots of models where you want to display a list, with
the same kind of filtering/sorting/paging logic applied?

You might end up with an ``object_list`` function and a bunch of parameters,
instead of ``product_list``. In other words, you'll end up with your own
function based generic views, `just like the ones that used to exist in Django
<https://django.readthedocs.io/en/1.3.X/topics/generic-views.html#generic-views-of-objects>`_.

Isn't that a step backwards? I'd argue no. With the benefit of hindsight, I'd
argue that the move from these function based generic views to class based
generic views was actually the backwards step.

But that is in the past. Looking forward, the generic views you might develop
will be better than both Django's old generic FBVs and the newer generic CBVs in
several ways:

* They will have all the functionality you need built-in.
* Importantly, they will have none of the functionality you don't need.
* You will be able to change them **whenever you want**, **however you want**.

In other words, they will be both specific (to your project) and generic (across
your project) in all the right ways. They won't suffer from Django's limitations
in trying to be all things to all men.

As FBVs they will probably be better for you than your own custom CBVs:

* They will have a well defined interface, which is visible right there in the
  function signature, which is great for usability.

* The generic code will be properly separated from the specific. For example,
  inside your ``object_list`` function, local variable names will be very
  generic, but these won't bleed out into functions that might call
  ``object_list``, because you don't inherit local variable names (in contrast
  to classes where you do inherit instance variable names).

* At some point you might find you have too many parameters to a function. But
  this is a good thing. For your class-based equivalent, the number of extension
  points would be the same, but hidden from you in the form of lots of mixins
  each with their own attributes and methods. With the function, your problem is
  more visible, and can prompt you to factor things out. For example, if you
  have several parameters related to filtering a list, perhaps you actually need
  to invent a ``Filterer`` class?


TODO - going further - higher level - DRF/Django admin


Discussion: Copy-Paste Bad, Re-use Good?
----------------------------------------

Where do Django's generic CBVs come from? Why didn't we stop with function based
generic views? The problem was that there was an endless list of requests to
extend generic views to do one more thing, and we wanted to provide something
more customisable.

Our answer to this problem ought to have been this: if these generic views don't
do what you want, write your own. You can easily copy-paste the functionality
you need and start from there. So why didn't we just say that? I think we
somehow had the idea that copy-paste is the ultimate disaster in software
development. If there is some functionality written, we should always make it
re-usable rather than re-implement, and we've somehow failed as software
developers if we can't.

You can see this in the design of the CBVs. A lot of the complexity in the
hierarchy looks like it was introduced in order to avoid a single duplicate
line. `But that shouldn't be our primary aim
<https://verraes.net/2014/08/dry-is-about-knowledge/>`_.

There are plenty of things worse than copy-paste programming, and `the wrong
abstraction <https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction>`_ is
one of them.

I recently wrote several implementations of Mozilla's `Fluent
<https://projectfluent.org/>`_ localisation language, all of them in Python. One
of them was a Fluent-to-Python compiler, another was a Fluent-to-Elm compiler.
These two projects are clearly very similar in nature. So when I started the
second, I did so with `one big copy-paste job of 2500 lines of code
<https://github.com/elm-fluent/elm-fluent/commit/a100de2021dcc4fa413769342b1cba0240ba63ee>`_.
I knew that although there were many, many similarities between the two
projects, there would also be many, many differences. I was right — the two code
bases still share a huge amount in terms of structure. In a few places they even
still have significant chunks of identical code. But the code bases have also
diverged at many, many points, both in small details and in more fundamental
ways.

The decision to copy-paste was overwhelming the right decision. Attempting to
avoid duplicating anything while I was developing the second would have been an
absolute killer in terms of complexity, and may have failed completely. Once or
twice I copied fixes or changes directly from one to the other, but most times
when I had “equivalent” changes to do, they looked significantly different in
the two projects. Having to do them twice from scratch cost far, far less than
attempting to write the two projects with a common abstraction layer.

Before you can abstract commonality, you actually need at least two examples,
preferably three, and abstracting before then is premature. The commonalities
may be very different from what you thought, and when you have enough
information to make that decision you might decide that it's not worth it. So
avoiding all duplication at any cost is not the aim we should have.

.. _multiple-mixins:

Discussion: Multiple mixins?
----------------------------

When doing both a single object lookup and a list of objects, contrast the
simplicity of the above FBV code with `trying to wrangle CBVs into doing this
<https://docs.djangoproject.com/en/stable/topics/class-based-views/mixins/#using-singleobjectmixin-with-listview>`_.

These Django docs do come up with a solution for this case, but it is a house of
cards that requires lots of extremely careful thinking and knowing the
implementation as well as the interface of all the mixins involved.

But, after scratching your head and debugging for an hour, at least you have
less typing with the CBV, right? Unfortunately, the opposite is true:

Here is our view implemented with Django CBVs — as it happens, it is exactly the
same as the example in the docs linked above with model names and template names
changed:

.. code-block:: python

   from django.views.generic import ListView
   from django.views.generic.detail import SingleObjectMixin

   from shop.models import SpecialOffer


   class SpecialOfferDetail(SingleObjectMixin, ListView):
       paginate_by = 2
       template_name = "shop/special_offer_detail.html"

       def get(self, request, *args, **kwargs):
           self.object = self.get_object(queryset=SpecialOffer.objects.all())
           return super().get(request, *args, **kwargs)

       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           context['special_offer'] = self.object
           return context

       def get_queryset(self):
           return self.object.products.all()

And here is The Right Way (including calling ``Paginator`` manually ourselves
without any helpers):

.. code-block:: python

   from django.core.paginator import Paginator
   from django.shortcuts import get_object_or_404
   from django.template.response import TemplateResponse

   from shop.models import SpecialOffer


   def special_offer_detail(request, slug):
       special_offer = get_object_or_404(SpecialOffer.objects.all(), slug=slug)
       paginator = Paginator(special_offer.products.all(), 2)
       page_number = request.GET.get('page')
       page_obj = paginator.get_page(page_number)
       return TemplateResponse(request, 'shop/special_offer_detail.html', {
           'special_offer': special_offer,
           'page_obj': page_obj,
       })

This is a clear win for FBVs by any code size metric.

Thankfully the Django docs do add a “don't try this at home kids” warning and
mention that many mixins don't actually work together. But we need to add to
those warnings:

* It's virtually impossible to know ahead of time which combinations are likely
  to turn out bad. It's pretty much the point of mixins that you should be able
  to “mix and match” behaviour. But you can't.

* Simple things often turn into complicated things. If you have started with
  CBVs, you will most likely want to continue, and you'll quickly find yourself
  rather snarled up. You will then have to retrace, and completely restructure
  your code, working out how to implement for yourself the things the CBVs were
  doing for you. Again we find the CBV is a bad :ref:`starting point
  <starting-point>`.
