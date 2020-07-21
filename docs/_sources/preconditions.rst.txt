Preconditions
=============

When writing views, a common situation is that you have some checks that need to
be done at the beginning of a view before the main logic, and several views
might share the same checks. If the check fails you might want to redirect the
user to a different page, but other options are possible, such as displaying a
message (perhaps using the `messages framework
<https://docs.djangoproject.com/en/stable/ref/contrib/messages/>`_).

Python “decorators” are a perfect match for these kind of things.

If you haven't used decorators at all before, I'd recommend this `Primer on
Python Decorators <https://realpython.com/primer-on-python-decorators/>`_. If
you just want to apply an existing decorator to a view, that's very easy, but a
good understanding of what is going on is really necessary if you want to be
able to implement them. Plus, you'll get a huge amount of benefit in other ways
from this very general Python technique.

First let's look at our starting point. We have a page that should only be
accessible to 'premium' users. If, somehow, a non-premium user gets the link to
the page, they should be redirected to their account page, and also shown a
message.

It might look like this:

.. code-block:: python

   def my_premium_page(request):
       if not request.user.is_premium:
           messages.info(request, "You need a premium account to access that page.")
           return HttpResponseRedirect(reverse('account'))
       return TemplateResponse(request, 'premium_page.html', {})


Now, we want to re-use those first 3 lines of logic. The neatest way is to put
them in a decorator, which we will use like this:

.. code-block:: python

   @premium_required
   def my_premium_page(request):
       return TemplateResponse(request, 'premium_page.html', {})


To understand how to implement a decorator, it's often useful to remember what
decorator syntax is doing. The long-hand way of defining ``my_premium_page``,
equivalent to the above, is like this:

.. code-block:: python

   def my_premium_page(request):
       return TemplateResponse(request, 'premium_page.html', {})

   my_premium_page = premium_required(my_premium_page)

In other words, ``premium_required`` is a function that takes a view function as
input, and returns a new, replacement view function as output. The view function
it returns will **wrap** the original view function. In our case, it will also
add some additional checks and logic, and in some cases (where the user is not a
premium user), it will decide to bypass the original view function and return
its own response.

So the implementation of ``premium_required`` will look like this:


.. code-block:: python

   import functools

   def premium_required(view_func):

       @functools.wraps(view_func)
       def wrapper(request, *args, **kwargs):
           if not request.user.is_premium:
               messages.info(request, "You need a premium account to access that page.")
               return HttpResponseRedirect(reverse('account'))
           return view_func(request, *args, **kwargs)

       return wrapper


The ``@functools.wraps(view_func)`` line is not strictly necessary. But it makes
our wrapper function view behave more nicely — for example, it copies the name
and docstring of the original view over, along with other attributes. These make
debugging nicer, and sometimes it can be important for functionality too (for
instance, if you are wrapping something that has been wrapped in
``csrf_exempt``) — so you should always add it.

So far, the views we're using it on only take a single ``request``, so making
our wrapper take ``*args`` and ``**kwargs`` might not seem necessary. But we
want this decorator to be generic and future proof, so we put those in there
from the start.


Managing multiple decorators
----------------------------

Our decorator as above has an issue — if an anonymous user accesses it,
``request.user`` will be an ``AnonymousUser`` instance, and won't have an
``is_premium`` attribute, which will result in a 500 error.

A nice way to tackle this is to use the Django-provided ``login_required``
decorator, which will redirect to the login page for anonymous users.
We simply need to apply both decorators. The correct order is as
follows:

.. code-block:: python

   from django.contrib.auth.decorators import login_required

   @login_required
   @premium_required
   def my_premium_page(request):
       return TemplateResponse(request, 'premium_page.html', {})


The checks that ``login_required`` does ensure that by the time we get into the
``premium_required`` view wrapper, we are guaranteed to have a logged in user.


Ordering multiple decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When dealing with multiple decorators, as above, ordering can be very important,
and it's easy to get confused about what order everything is happening.

The best analogy I know of is to think of it as an **onion**. In the centre, you
have the actual view function, and each decorator adds a layer. Let's write it
out the long hand way as a visualisation:

.. code-block:: python

   def my_premium_page(request):
       return TemplateResponse(request, 'premium_page.html', {})

   my_premium_page = \
       login_required(
           premium_required(
               my_premium_page
           )
       )

So, ``premium_required`` is the **innermost** decorator. It is the first to be
**applied** to ``my_premium_page``, while ``login_required`` is the
**outermost** decorator, and it is the last to be applied.

**BUT!** The decorators themselves (the functions ``premium_required`` and
``login_required``) are distinct from the wrappers they return!

So, the preconditions that the ``login_required`` wrapper adds are run **first**
(because it is the outermost), and the preconditions that the
``premium_required`` wrapper adds are run **last** (because it is the
innermost).

The result is actually very intuitive — the preconditions added by each
decorator are run in the order that the decorators appear in your source code.

However, you might also want to do post-processing in your view wrappers. If you
do that, remember the onion metaphor — post-processing from the innermost
wrapper will run before post-processing from the outermost wrapper.

Exercise
~~~~~~~~

If the above left you horribly confused, I think the best way to understand this
is to get your hands dirty with some examples, so here is an exercise.

Suppose we have the following decorators (which do nothing other than print some
things):


.. code-block:: python

   def decorator_1(view_func):
       print("In decorator_1")

       def wrapper(request, *args, **kwargs):
           print("In decorator_1 wrapper, pre-processing")
           response = view_func(request, *args, **kwargs)
           print("In decorator_1 wrapper, post-processing")
           return response

       return wrapper


   def decorator_2(view_func):
       print("In decorator_2")

       def wrapper(request, *args, **kwargs):
           print("In decorator_2 wrapper, pre-processing")
           response = view_func(request, *args, **kwargs)
           print("In decorator_2 wrapper, post-processing")
           return response

       return wrapper

Then, what will the following code blocks print?


.. code-block:: python

   >>> @decorator_1
   ... @decorator_2
   ... def my_view(request):
   ...     print("In my_view")
   ...     return "I am a response"

.. code-block:: python

   >>> response = my_view(None)

First make your guesses, then try the code from a Python prompt. If you get it
wrong, have another look until you understand exactly what is going on.

Hints:

* Replace the ``@`` syntax with the long-hand version
* Simplify using no decorators, then one decorator, then two decorators


Combining multiple decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have multiple decorators that need to be applied in a certain order, or
where you often have them together, you should probably be thinking about
building a single decorator that combines them — for which I can do no better
than point you to Adam Johnson's post `How to Combine Two Python Decorators
<https://adamj.eu/tech/2020/04/01/how-to-combine-two-python-decorators/>`_!

You could also see this Stackoverflow post with `general code for composing any
number of decorators
<https://stackoverflow.com/questions/5409450/can-i-combine-two-decorators-into-a-single-one-in-python>`_


Built-in decorators
-------------------

Also, don't miss out on the decorators and "decorator factories" than come with
Django and cover many of the common cases, such as ``login_required`` (already
used), `user_passes_test
<https://docs.djangoproject.com/en/stable/topics/auth/default/#django.contrib.auth.decorators.user_passes_test>`_
and `permission_required
<https://docs.djangoproject.com/en/stable/topics/auth/default/#the-permission-required-decorator>`_

Next up: :doc:`thin-views`.


Discussion: Mixins do not compose
---------------------------------

Django also provides mixins for applying preconditions, like `LoginRequired
<https://docs.djangoproject.com/en/stable/topics/auth/default/#the-loginrequired-mixin>`_
etc., which work by overriding the ``dispatch()`` method.

Now, suppose we were to go the CBV route, and have a ``PremiumRequired`` mixin
instead of ``@premium_required``. Let's also add another similar check —
``GoodReputationRequired`` which does some kind of reputation check (perhaps
this is a social site with moderation in place). To require a user to have both,
is it enough to just add both mixins? Similarly, could I produce a new mixin
like this?

.. code-block:: python

   class PremiumAndGoodReputationRequired(PremiumRequired, GoodReputationRequired):
       pass


The answer is: **it depends**.

Let's suppose we used the `UserPassesTestMixin
<https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin>`_
that Django provides, which will make our mixins quite short and simple. In this
case, our mixins will **not** compose as required, but will **silently fail** —
only one of the checks will run. If this was a feature critical for security,
that could be rather bad!

But if we implemented our base mixins some other way (like only overriding
``dispatch()``, and using ``super()`` correctly), they **should** compose.

(See the `preconditions discussion_views.py
<https://github.com/spookylukey/django-views-the-right-way/blob/master/code/the_right_way/preconditions/discussion_views.py>`_
file for a full example of both)

This issue is noted in the docs for ``UserPassesTestMixin`` — you cannot stack
multiple uses of it.

However, docs or not, this is a great example of how, in general, **mixins do
not compose**. I've said it :ref:`before <multiple-mixins>` but it is worth
repeating. You can have two mixins that work perfectly apart, but fail together.
To be sure that they do compose, you have to **know the implementation**.
Further, it's entirely possible that when you first put them together there is
no issue, but a later change means they fail start failing in the worst possible
way — **silently**.

This is a horrible way to write software! As much as possible, we should choose
techniques where you can simply depend on the interface of some code to know
that you are using it correctly, rather than its implementation.

Decorators aren't prone to this problem. Mixins are like injecting things right
into the middle of someone else's code, hoping that the context will fit, while
decorators wrap existing functionality depending only its interface.
