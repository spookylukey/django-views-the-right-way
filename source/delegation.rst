Custom logic at the start - delegation
======================================

The next few pages address the problem of needing to re-use some logic from one
view in another view. We've thought about how we can use utility functions and
classes, but sometimes these don't cut it — sometimes the majority of the body
of the view needs to be re-used. How can we do that with FBVs?

Continuing our :ref:`example <list_view>` of a list of products, let's add a
variation. As well as the main product list page, we've also got a “special
offers” page — or rather, a set of them, because we can have a ``SpecialOffers``
model that allows us to have many different ones. Each of these pages needs to
display some details about the special offer, and then the list of products
associated with that offer. This product list should have **all** the features
of the normal product list (filtering, sorting etc.) so we want to re-use the
logic.

Let's start with a simple version of our view:

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
       products = special_offer.get_products()
       return TemplateResponse(request, "products/special_offer_detail.html", {
           'special_offer': special_offer,
           'products': products,
       })

I've assumed the ``SpecialOffer.get_products()`` method exists and returns a
``QuerySet``. If you have an appropriate ``ManyToMany`` relationships the
implementation might be as simple as ``return self.products.all()``.

Notice first of all — our view does two things: it shows a single object, and
also shows a list. The answer of how to do two things with FBVs is: **do two
things**. There is no special magic or combination of CBVs needed. The names
I've chosen reflect the "model instance detail" conventions, but that was just a
choice.

But now we want to change this view to re-use the logic in our normal
``product_list`` view, whether it is filtering/sorting/paging or anything else
it has built up by now. How should we do that?


The easiest way to answer to this is to look at our old ``product_list`` view
and apply `parameterisation
<https://www.toptal.com/python/python-parameterized-design-patterns>`_.



(Template level - use includes)



Discussion

Contrast the simplicity with trying to wrangle CBVs into doing this.
https://docs.djangoproject.com/en/dev/topics/class-based-views/mixins/#using-singleobjectmixin-with-listview

Docs wisely say "avoid anything more complex". But:

1) It's virtually impossible to know ahead of time which combinations are likely
   to turn out bad

2) Simple things often turn into complicated things. If you have started with
   CBVs, you will most likely want to continue, and find yourself rather snarled
   up. You will then have to retrace, and completely restructured your code,
   working out how to implement for yourself the things the CBVs were doing for
   you. The CBV is a bad starting point.
