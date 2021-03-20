Custom logic in the middle — dependency injection
=================================================

What happens if we have code that is largely common, but want to do something
different “in the middle”?

We are getting into more advanced territory now, so this page is heavier than
the ones that have come before, but the techniques here are also very powerful
and widely applicable.

Continuing our :doc:`example of two different views both featuring lists of
products <delegation>`, let's add a new requirement, imitating the kind of
complexity you will likely encounter in real projects.

Instead of using Django's ``QuerySets`` as the basis for our list of products,
we have to use a different API. Maybe it is a third party HTTP-based service, or
our own service, but our entry point is a function that doesn't take a
``QuerySet`` as an input. Perhaps like this:

.. code-block:: python

   def product_search(filters, page=1):
       ...
       return product_list

``filters`` is a dictionary that contains product filtering info, with allowable
keys defined elsewhere. Our ``display_product_list`` now needs to convert query
string parameters from ``request.GET`` to something that can be passed as
``filters``.

(For the sake of simplicity, we're doing a much more basic kind of paging in
this example, in contrast to what ``Paginator`` gives you with page counts
etc.)

For special offers, however, we have been provided with a **different** function
to use:

.. code-block:: python

   def special_product_search(filters, special_offer, page=1):
       ...
       return product_list

In addition, we have a further requirement: for our special offer page, after
retrieving the list of products that will be displayed, we need to do some
database logging to record the user, the special offer and the products that
were displayed.

The point of all this is to set up a common requirement — something that applies
to many programming situations, not just view functions:

    **How can we execute some custom logic in the middle of some common logic?**

We can think of this is as just another example of `parameterisation
<https://www.toptal.com/python/python-parameterized-design-patterns>`_. We need
a parameter that will capture “what we need to do in the middle”.

Let's start with the easier case — just the ``product_list`` view, factored out
:doc:`as before <delegation>` into the main view and the
``display_product_list`` function it delegates to. The latter now needs
changing:

1. It no longer takes a ``queryset`` parameter, but a ``searcher`` parameter.
2. It has to be adapted to use this ``searcher`` parameter instead of
   manipulating a passed in ``QuerySet``.

Something like this:

.. code-block:: python

   from somewhere import product_search

   def product_list(request):
       return display_product_list(
           request,
           searcher=product_search,
           template_name='shop/product_list.html',
       )

   def display_product_list(request, *, context=None, searcher, template_name):
       if context is None:
           context = {}
       filters = collect_filtering_parameters(request)
       try:
           page = int(request.GET['page'])
       except (KeyError, ValueError):
           page = 1
       context['products'] = searcher(filters, page=page)
       return TemplateResponse(request, template_name, context)


To explain a little: here we passed the ``product_search`` function into
``display_product_list`` as the parameter ``searcher``. This feature is called
“first class functions” — just like you can pass around any other data as a
parameter, you can pass around functions too. That is the heart of the technique
here, allowing us to insert our custom logic into the middle of the common
logic.

But what about the ``special_offer_detail`` view? If we pass
``searcher=special_product_search``, inside ``display_product_list``
we'll have a problem. Our passed in function gets called like this::

  searcher(filters, page=page)

But that doesn't match the signature of ``special_product_search``, which has an
extra parameter. How can we get that parameter passed?

You might be tempted to make ``display_product_list`` accept the additional
parameters needed, but this is clunky — we'll have to pass these parameters that
it doesn't care about, just so that it can pass them on to somewhere else. Plus
it is unnecessary.

Instead, what we do is make ``special_offer_detail`` provide a wrapper function
that matches the signature that ``display_product_list`` expects for
``searcher``. Inside the wrapper function, we'll call the
``special_product_search`` function the way it needs to be called. While we're
at it, we can do our additional requirements too.

It looks like this, assuming we've written ``log_special_offer_product_view``
function for the extra logging:


.. code-block:: python

   from somewhere import special_product_search

   def special_offer_detail(request, slug):
       special_offer = get_object_or_404(SpecialOffer.objects.all(), slug=slug)

       def special_product_search_wrapper(filters, page=1):
           products = special_product_search(filters, special_offer, page=page)
           log_special_offer_product_view(request.user, special_offer, products)
           return products

       return display_product_list(
           request,
           context={
               'special_offer': special_offer,
           },
           searcher=special_product_search_wrapper,
           template_name='products/special_offer_detail.html',
       })

There are some important things to note about this:

* We defined our wrapper function ``special_product_search_wrapper`` inside the
  body of the main view. This is important for the functionality that follows.
  (There are other ways to do it but this is the simplest.)

* We made its signature match the one expected by ``display_product_list``.

* Our wrapper function has access to the ``special_offer`` object from the
  enclosing scope, and also ``request``. These objects “stay with it” when the
  wrapper function gets passed to ``display_product_list``, so they are able to
  use them despite not having been passed them as a normal arguments.

  Functions that behave in this way are called “closures” — they capture
  variables from their enclosing scope.


This powerful technique has lots of great advantages. For one,
``display_product_list`` never needs to be concerned with all of this. We don't
have to modify its signature, nor the signature of the ``searcher`` parameter it
expects. Also, this works really well with static analysis, like the linters
that are built-in to many IDEs which can point out undefined names and so on.

Closures are a concept that some find intimidating, but they are extremely
useful in a wide variety of programming situations. If you found the above
confusing, have a look at this `Python closures primer
<https://www.programiz.com/python-programming/closure>`_ and then come back to
the more complex example here.

In our theme of re-using logic, I want to cover :doc:`preconditions`, but before
that we're going to go back to some basics, the first of which is
:doc:`redirects` and then :doc:`forms`.


Note: terminology
-----------------

In OO languages, the standard solution to this problem is the “strategy
pattern”. That involves creating an object which can encapsulate the action you
need to take.

In Python, functions are “first class objects“ i.e. objects that you can pass
around just like every other type of value. So we can just use “functions” where
we need “the strategy pattern”, particularly if our strategy has only one part to
it. If you have more than one entry point that you need to bundle together, a
class can be helpful.

A slightly more general concept is “dependency injection”. If you have some code
that needs to do something, i.e. it has a dependency on some other code, instead
of depending directly, the dependency gets injected from the outside. If our
dependency is a just a single function call, we can simply accept a function as
a parameter. If our dependency is a set of related function calls, we might want
an object with methods as the parameter.

Often you will hear the term “dependency injection” being used for things that
go one step further, and inject dependencies **automatically** in some way. I
call these “dependency injection frameworks/containers”. Outside of `pytest's
fixtures <https://docs.pytest.org/en/latest/fixture.html>`_ I have not yet found
a need or desire for these in Python.

So, we can call this pattern “first class functions”, or “callbacks”, “strategy
pattern” or “dependency injection”. But dependency injection is clearly the
coolest sounding, so I used that in the title.


Discussion: DI vs inheritance
-----------------------------

In contrast to the pattern I'm suggesting here (dependency injection / strategy
/ first class functions), Django's CBVs opt for inheritance as the basic method
of customisation, resulting in the need for class attributes and method
overrides.

Inheritance brings with it the problems we've discussed under :ref:`helpers vs
mixins <helpers-vs-mixins>`.

To make it more concrete, suppose we had solved the above
custom-logic-in-the-middle problem by using inheritance and the template method
pattern, in which we have a base class that calls an abstract
``do_product_search`` method, and two subclasses which each implement that
method. The base class might look something like this:

.. code-block:: python

   class ProductSearchBase(TemplateView):
       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           filters = collect_filtering_parameters(self.request)
           try:
               page = int(self.request.GET['page'])
           except (KeyError, ValueError):
               page = 1
           context['products'] = self.product_search(filters, page=page)
           return context

       def product_search(self, filters, page=1):
           raise NotImplementedError()


Now, how do we implement ``product_search`` for our “special offer“ subclass? To
call ``special_product_search``, we need access to the ``special_offer`` object
that we already looked up in a different method. Note that we've got the same
problem as before — in both cases we need some way to adapt our common code to
call functions with two different signatures.

We could solve this by saving the object onto ``self``, something like this:

.. code-block:: python

   class SpecialOfferDetail(ProductSearchBase):
       template_name = 'shop/special_offer_detail.html'

       def get(self, request, *args, **kwargs):
           special_offer = get_object_or_404(SpecialOffer.objects.all(), slug=kwargs['slug'])
           self.special_offer = special_offer
           return super().get(request, **kwargs)

       def product_search(self, filters, page=1):
           products = special_product_search(filters, self.special_offer, page=page)
           log_special_offer_product_view(self.request.user, self.special_offer, products)
           return products

       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           context['special_offer'] = self.special_offer
           return context


In this solution, we have separate methods that are forced to communicate with
each other by setting data on ``self``. This is hacky and difficult to follow or
reason about. Your ``product_search`` method now has some hidden inputs that
could easily be missing. To be sure of correctness, you need to know the order
in which your different methods are going to get called. When you are forced to
use ``self`` like this, it's worth reflecting on the `objects are a poor man's
closures koan <https://wiki.c2.com/?ClosuresAndObjectsAreEquivalent>`_.

This kind of code is not uncommon with CBVs. For example, a lot of code that
uses ``DetailView`` will need to use the fact that ``get_object`` method stores
its result in ``self.object``.

I recently refactored some CBV views that demonstrated exactly this issue into
the FBV pattern I recommend above. The initial CBV views had a significant
advantage over most CBVs you'll find — I was using `my own custom CBV base class
<https://lukeplant.me.uk/blog/posts/my-approach-to-class-based-views/>`_, that I
had specifically designed to avoid what I consider to be the worst features of
Django's offering.

Despite this advantage, rewriting as FBVs yielded immediate improvements. There
was a noticeable reduction in length (542 tokens vs 631). But far more important
and impressive was the fact that I completed the task without any errors — the
new code had no bugs and passed all the tests first time.

Was this because I'm some kind of super-programmer? No, it was simply that my
linter was pointing out every single mistake I made while I was moving code
around. Once I had fixed all the “undefined name” and “unused variable” errors,
I was done. The reason for this is that **static analysis has a much easier time
with code written using functions and closures**.

The same static analysis is almost impossible with the CBV version. Half of the
local variables become instance variables, and not set up in ``__init__``
either. This means the analyser has to trace all the methods to see if any of
them create the instance variables. Really, it then needs to check the order in
which methods are called, to check whether they get set up before they are used.
Most static analysis tools will not get very far with this, if they even attempt
it, and it will be almost impossible to get past `this line
<https://github.com/django/django/blob/8dabdd2cc559a66b519e2a88b64575d304b96ebe/django/views/generic/base.py#L98>`_.

However, the static analysis tools we use are simply automating what you can do
as a human. The fact that they fail with the CBV and succeed with the FBV is
just pointing out to you the much greater complexity of the former, which has
implications for any human maintainer of the code, as well as for tools.

I'm not using anything fancy in terms of linters, by the way — just ``flake8``
integrated into my editor. If you want to go further and add type hints and use
mypy, you will find it very easy to do with the approach I've outlined above,
and make it possible to automatically verify even more things. On the other
hand, if your CBV ``self`` object is a rag-bag of stuff as above it will be very
hard for even the most advanced tools to help you.

`pylint <https://pylint.pycqa.org/en/latest/>`_ gets further than flake8 in
trying to detect typos in instance variables, and does a pretty good job.
However it cannot detect the ordering issue mentioned, and it also complains
about us setting instance variables outside of ``__init__`` (W0201
``attribute-defined-outside-init``) — a complaint which has some solid reasons,
and is essentially recommending that you don't structure your code like this. If
you follow its recommendations you'll (eventually) get yourself to the FBV.

When I had finished this refactoring, which in the end completely removed my
custom CBV base class, I confess I had a little twinge of sadness — my final
code seemed just a little bit… *plain*. I now had just a bunch of simple
functions and a few closures, and fewer OOP hierarchies and clever tricks to
feel smug about. But this is misplaced sadness. If you are into smugness-driven
development, nothing can beat the feeling you get when you come back to some
code 3 months or 3 years later and find it's so straightforward to work with
that, after doing ``git praise``, you feel the need to give yourself a little
hug.
