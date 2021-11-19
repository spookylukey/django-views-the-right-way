Applying policies
=================

Sometimes you may need a certain policy, such as a security policy, to be
applied to a group of views. The policy might correspond to decorator like
``login_required``, for example, and it might be an entire module or app that
needs the policy applying.

What’s the best way to handle that using FBVs to ensure that we don’t forget? We
could also call this problem “comprehensive preconditions” — our earlier
:doc:`preconditions` patterns are great, but what if we just forget to apply
them to a view?

To make it a bit harder, we may have some variations on this theme, or
alternative ways of expressing it:

- we might want “every view in a module — apart from one or two”
- or “every view by default, unless we’ve specifically excluded it”
- or “every view should have one of N allowed policies applied”
- or “anonymous access should be opt-in” (instead of the default like it is in Django)


Solution 1: django-decorator-include
------------------------------------

`django-decorator-include <https://github.com/twidi/django-decorator-include>`_
is a neat little package that solves exactly this problem. It does what you’d
expect — it works just like `include
<https://docs.djangoproject.com/en/stable/ref/urls/#include>`_, but applies
decorators to all the URLs included.

This pattern is particularly good when you are including a 3rd party app —
without touching the code, you can apply a single blanket policy to it. It has
some disadvantages, though, especially when it’s your own code:

- it works at the URL level, which might be slightly different than what you
  want.

- it leaves your own view functions “not obviously right”. Views that you expect
  to be decorated with a ``login_required`` are now bare, and you have to
  remember that security is applied at a different point.

  What’s worse is that you might have some parts of your code base where you
  don’t (or can’t) use this pattern, and some where you do. So you have to
  switch between multiple mindsets. If you come across a view without a
  decorator, is that a security issue or not? You could end up training your
  subconscious to ignore the real issues, which is quite bad.

- it doesn’t have an obvious, easy mechanism for making exceptions.


Solution 2: decorator include with checking
-------------------------------------------

So, a modified version of the above technique is to still use
``decorator_include`` as above, but instead of adding security preconditions in
the decorator, we make the decorator simply check that a different, required
decorator has already been applied (at import time), and do nothing at run time.

The checking decorator might look something like this:

.. code-block:: python

   _SECURITY_POLICY_APPLIED = "_SECURITY_POLICY_APPLIED"

   def check_security_policy_applied(view_func):
       if not getattr(view_func, _SECURITY_POLICY_APPLIED, False):
           raise AssertionError(f"{view_func.__module__}.{view_func.__name__} needs to have a security policy applied")
       return view_func


(See the full code example — `decorators
<https://github.com/spookylukey/django-views-the-right-way/tree/master/code/the_right_way/policies/decorators.py>`_
and `URLs
<https://github.com/spookylukey/django-views-the-right-way/blob/master/code/the_right_way/policies/urls.py#L18>`_)

Our decorator simply checks for the existence of an attribute on the view
function that indicates that the security policy has been applied. I’ve defined
it using a constant with a leading underscore here to indicate that you are not
supposed to import this constant, but instead use it via one of several
decorators that apply the policy. Using our “premium required” example from
before, one of those decorators might look like this:


.. code-block:: python

   import functools
   from django.contrib import messages
   from django.http import HttpResponseRedirect


   def premium_required(view_func):
       @functools.wraps(view_func)
       def wrapper(request, *args, **kwargs):
           if not (request.user.is_authenticated and request.user.is_premium):
               messages.info(request, "You need to be logged in to a premium account to access that page.")
               return HttpResponseRedirect('/')
           return view_func(request, *args, **kwargs)

       setattr(wrapper, _SECURITY_POLICY_APPLIED, True)
       return wrapper


We can now use ``decorator_include`` with ``check_security_policy_applied`` as
the decorator. If all our views are decorated in ``@premium_required``,
everything will be fine. Otherwise we will get an exception — at import time,
not at run time, so we won’t be able to ignore it or find out too late.

(By the way, when implementing things like this, you should double check that it
really does fail in the way you expect it to fail…)

This mechanism is quite flexible, and can be used to allow exceptions to the
general policy. For example, we could add an ``anonymous_allowed`` decorator:


.. code-block:: python

   def anonymous_allowed(view_func):
       @functools.wraps(view_func)
       def wrapper(request, *args, **kwargs):
           return view_func(request, *args, **kwargs)

       setattr(wrapper, _SECURITY_POLICY_APPLIED, True)
       return wrapper


The wrapper added by this decorator actually does nothing but forward to the
original view function. It only exists to allow us to set the
``_SECURITY_POLICY_APPLIED`` attribute. But with this in place, we can
successfully move from Django’s “open to everyone by default” policy for view
functions to “private by default”, or whatever else we want.

We can make this solution more friendly by going back to
``check_security_policy_applied`` and making the error message list the possible
or preferred fixes.

Solution 3: introspection
-------------------------

The remaining issue with the previous solution is that it is tied to the
URL-space — our checks run only when we use ``decorator_include`` to add some
URLs into an application. That might not always be what we want.

Instead of that, we might want to apply policies to “all view functions
everywhere”, or something else more custom. In this case, one solution is to do
introspection of the URLconf after having loaded it. The details will depend on
what exactly you want to do, but there is `an example in the code folder
<https://github.com/spookylukey/django-views-the-right-way/blob/master/code/the_right_way/policies/introspection.py>`_.
The `Django system checks framework
<https://docs.djangoproject.com/en/stable/topics/checks/>`_ is a good option for
reporting this kind of error, or you could use ``raise AssertionError`` as
before to be more aggressive.

When implementing this, if you wish to apply this policy to something like “all
views within an app”, the hardest part is working out what you mean by “within
an app”. A view function could be defined outside the conventional ``views.py``
module, or imported from an entirely different app. Be sure that your
introspection accounts for these cases and does what you need!

Next up: :doc:`thin-views`.


Discussion: secure by default
-----------------------------

In the patterns suggested, I’m thinking about a simplified version of `Rusty's
API Design Manifesto
<http://sweng.the-davies.net/Home/rustys-api-design-manifesto>`_:

* Good: the wrong thing looks long
* Better: the wrong thing is harder than the right thing
* Best: the wrong thing is impossible

’Best’ is not always possible or easy to achieve, but we should be aiming for
it.

If you are using CBVs, then applying security checks (or other common policies)
in a CBV base class can be a nice pattern, because it is likely that new code
added to a module will follow the existing code, use the same base classes etc.
It will be harder to not do this, and code will probably look wrong if it
doesn’t. These are all great things.

Personally I think that using FBVs and having the decorator at the top of each
view function is even clearer, rather than having the check buried in a base
class. Also, as noted :ref:`before <mixins-do-not-compose>`, you can easily get
security problems with CBVs due to how inheritance works.

Another important property for reasoning about code correctness is “locality”.
That’s why I don’t like solution 1 above — when reading ``views.py``, I’m having
to remember whether ``urls.py`` is adding some additional behaviour, and the
right thing actually looks wrong.

After making the right thing easy and the wrong thing look wrong, being able to
use some form of introspection for additional guarantees that we are doing it
right is great, and an area where Python really shines.

Sometimes, we might have an explicit list of exceptions to a policy. Here are
some tips for managing that effectively:

- if you gather exceptions to a rule into a list in one place, each exception
  should have a comment justifying its presence. This establishes a strong
  precedence that makes it hard to just add more exceptions — without a
  justification, they look wrong.

- you can go further, and make things like your “anonymous allowed” decorator
  have a mandatory ``rationale`` argument in which the developer must provide a
  non-empty string reason for its existence. Of course, they could always write
  ``"Just because"``, but they will at least be conscious that they are doing
  something bad.
