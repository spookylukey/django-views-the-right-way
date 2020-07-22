Common context data
===================

Suppose we have a bunch of views that end up all needing the same bits of
context data. How should we handle that?

There are a few different answers:

1. Is the data going to be needed by pretty much every page in your site? The
   answer is `context processors
   <https://docs.djangoproject.com/en/stable/ref/templates/api/#django.template.RequestContext>`_.

2. Is the data going to be needed in a large fraction of your site, but not
   everywhere and is expensive to evaluate? I'd recommend using `lazy evaluation
   in your context processor <https://stackoverflow.com/a/28146359/182604>`_.

3. Is the data needed for a ”component” that exists really at the template level, perhaps
   in a base template or is included in several templates?

   For example, it might be data needed for common navigation elements that
   appear in a header on lots of pages.

   In general this can be done most easily by using a `custom inclusion template
   tag
   <https://docs.djangoproject.com/en/stable/howto/custom-template-tags/#inclusion-tags/>`_
   which can load its own data — that way you don't have to worry about changing
   view functions every time you include this component.

But suppose none of these apply — we just have some common data that is used for
a group of a pages. Perhaps we have an e-commerce site, and all the checkout
pages have a common set of data that they need, without necessarily displaying
it in the same way.

For this, we can use the simple technique below of pulling out the code that
returns the common data into a function:

.. code-block:: python

   def checkout_start(request):
       context = {}
       context.update(checkout_pages_context_data(request.user))
       return TemplateResponse(request, "shop/checkout/start.html", context)


   def checkout_pages_context_data(user):
       context = {}
       if not user.is_anonymous:
           context["user_addresses"] = list(user.addresses.order_by("primary", "first_line"))
       return context

Just add ``context.update(checkout_pages_context_data(request.user))`` into
every view that needs it.

This is a perfectly adequate technique that is very easy to use, easy to
understand and flexible. You can add parameters to the function if necessary,
such as the ``user`` object as above, and combine common sets of these helpers
into bigger helpers, as per your requirements. And you can write tests for these
helpers if they have any significant logic in them.

Next up: :doc:`url-parameters`

(You may be interested in a more fancy technique, based on TemplateResponse and
decorators - TODO - but it really isn't necessary).

.. _helpers-vs-mixins:

Discussion: Helpers vs mixins
-----------------------------

The solution above is simple and direct. But some might protest it is a bit
ugly, and has involved a bit of boilerplate. A CBV solution using a mixin is
surely more elegant:

.. code-block:: python

   class CheckoutPageMixin:

       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           user = self.request.user
           if not user.is_anonymous:
               context["user_addresses"] = list(user.addresses.order_by("primary", "first_line"))
           return context

You simply have to include ``CheckoutPageMixin`` in your base classes, which is
less typing than ``context.update(checkout_pages_context_data(request.user))``.
This kind of base class or mixin might also provide some other functionality,
like doing some pre-condition checks and redirects as necessary.

My response would be, first, a reminder that a small reduction in typing is a
poor trade-off if it obfuscates your code even a small amount, due to the time
we spend reading versus writing code.

Second, the mixin has several significant disadvantages:

* It hides the source of the context data. Any of your base classes could
  potentially be overriding ``get_context_data``, you have to look at all of
  them to get the whole picture, which in general is harder than just following
  function definitions.

* Your mixin is not separately testable. This is a major problem with mixins in
  general.

* Lack of testability is just an indication of a deeper problem — the mixin does
  not have a well defined interface, and this always hinders comprehension. If
  you think of ``get_context_data`` not as a method, but as a function whose
  first parameter is ``self``, you'll quickly see how complicated its interface
  is.

* Over time, mixins defined like this quickly becomes tangled, due to that
  problematic ``self`` parameter, which can have all kinds of things attached to
  it. Very quickly you can end up with a mixin that works in one context, but
  not in another, due to different expectations about what is attached to
  ``self``.

  In contrast, all the parameters to functions are usually well defined, and you
  can usually have a very high level of confidence that they will work in all
  contexts. There is no ``self`` parameter which you can you use to sneak things
  in. (See :ref:`shortcuts vs mixins <shortcuts-vs-mixins>` for a more in-depth
  treatment of this)

* Mixins often tie you into inheritance trees for organising things. In reality,
  instead of trees you often want a mix-and-match approach to including data or
  functionality. Mixins are supposed to support that, but it you quickly find
  :ref:`they don't really and you end up in a tangle <multiple-mixins>`.

The simple solution is the best!

This example is part of a larger principle for the best way to write views, and
any similar functions:

.. pull-quote::

   Building up behaviour by explicitly **composing** smaller, testable units of
   functionality (whether functions or classes) is far better than building up
   behaviour via **inheritance**.

For more on this, see Brandon Rhodes' treatment of `The Composition Over
Inheritance Principle
<https://python-patterns.guide/gang-of-four/composition-over-inheritance/>`_,
which also mentions mixins.
