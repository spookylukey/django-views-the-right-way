Common context data
===================

Suppose we have a bunch of views that end up all needing the same bits of
context data. A common example is some data that will be used by the navigation
parts of your templates.

If the data is going to be needed by pretty much every page in your site, the
answer is `context processors
<https://docs.djangoproject.com/en/3.0/ref/templates/api/#django.template.RequestContext>`_.
If you have context processors that are expensive to evaluate, and are used in
lots of places but not everywhere, one technique is to use `lazy evaluation in
your context processor <https://stackoverflow.com/a/28146359/182604>`_.

But let's say you have some data that is just used for a sub-set of a pages —
perhaps it's navigation data for the help sub-section of your site. We can use
the simple technique below of pulling out the code that returns the common data
into a function:

.. code-block:: python

   def help_index(request):
       context = {}
       context.update(help_section_context_data())
       return TemplateResponse(request, "help/index.html", context)


   def help_section_context_data():
       # This might be loaded from a database or something...
       return {
           'help_pages': [
               ('/help/',                 'Help index'),
               ('/help/getting-started/', 'Getting started'),
               ('/help/contact-us',       'Contact us'),
               # etc.
           ],
       }

Just add ``context.update(help_section_context_data())`` into every view that
needs it.

This is a perfectly adequate technique that is very easy to use, easy to
understand and flexible. You can add parameters to the function if necessary
(e.g. ``request`` or some data from it), combine common sets of these helpers
into bigger helpers, as per your requirements. And you can write tests for these
helpers if they have any significant logic in them.

Next up: :doc:`url-parameters`

(You may be interested in a fancy technique, based on TemplateResponse and
decorators - TODO - but it really isn't necessary).

.. _helpers-vs-mixins:

Discussion: Helpers vs Mixins
-----------------------------

The solution above is simple and direct. But some might protest it is a bit
ugly, and has involved a bit of boilerplate. A CBV solution using a mixin is
surely more elegant:

.. code-block:: python

   class HelpPageMixin:

       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           context['help_pages'] = [
               # etc.
           ]
           return context

You simply have to include ``HelpPageMixin`` in your base classes, which is less
typing than ``context.update(help_section_context_data())``. This kind of base
class or mixin might also provide some other functionality, like doing some
permission checks for this sub-set of pages etc.

My response would be, first, a reminder that a small reduction in typing is a
poor trade-off if it obfuscates your code even a small amount, due to the amount
of time we spend reading versus writing code.

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
  functionality. Mixins do support that, at least in this case, but if you
  imagine that you'll have a neat hierarchy involving a ``HelpPageMixin`` that
  provides both context data and some other functionality, you'll quickly be
  disappointed when things don't turn out that simple, and you find yourself in
  a tangle.

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
