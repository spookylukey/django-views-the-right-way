Applying policies
=================

You may find yourself in the situation where you need a certain policy, often a
security policy, needs to be applied to a group of views. The policy might
correspond to decorator like ``login_required``, for example, and it might be an
entire module or app that needs the policy applying.

What’s the best way to handle that using FBVs to ensure that we don’t forget? We
could also call this problem “comprehensive preconditions” — our earlier
:doc:`preconditions` patterns are great, but what if we just forget to apply
them to a view?

To make it a bit harder, we may have some variations on this theme, or
alternative ways of expressing it:

- we might want “every view in a module apart from one or two”
- or “every view by default, unless we’ve specifically excluded it”
- or “every view should have one of N allowed policies applied”
- or “anonymous access should be opt-in” (instead of the default like it is in Django)


Solution 1 - django-decorator-include
-------------------------------------

`django-decorator-include <https://github.com/twidi/django-decorator-include>`_
is a neat little package that solves exactly this problem, at least in some
forms. It does what you’d expect - it works just like `include
<https://docs.djangoproject.com/en/stable/ref/urls/#include>`_, but applies
decorators to all the URLs included.

This pattern is particularly good when you are including a 3rd party app -
without touching the 3rd party code, you can apply a single blanket policy. It
has some disadvantages, though, especially when it’s not a 3rd party app but
your own code:

- it works at the URL level, which might be slightly different than what you want
- it leaves your own view functions “not obviously right”. Pages that you expect
  to be decorated with a ``login_required`` are now bare, and you have to
  remember that security is applied at a different point.

  Worse is that you might have some parts of your code base where you don’t (or
  can’t) use this pattern, so you have to switch between multiple mindsets. If
  you come across a view without a decorator, is that a security issue or not?
  You could end up training your subconscious to ignore the real issues, which
  is quite bad.
- it doesn’t have an easy mechanism for making exceptions.



Solution 2 - decorator include with checking
--------------------------------------------

So, a modified version of the above technique is to still use
``decorator_include`` as above, but instead of adding security preconditions in
the decorator, we make the decorator simply check that a required decorator has
been applied (at import time), and do nothing at runtime.

So, the checking decorator might look something like this:

.. code-block:: python

   _SECURITY_POLICY_APPLIED = "SECURITY_POLICY_APPLIED"

   def check_security_policy_applied(view_func):
       if not getattr(view_func, _SECURITY_POLICY_APPLIED, False):
           raise AssertionError(f"{view_func.__module__}.{view_func.__name__} needs to have a security policy applied")
       return view_func


(See the `full code example here
<https://github.com/spookylukey/django-views-the-right-way/tree/master/code/the_right_way/policies>`_)

Our checker simply checks for the existence of an attribute on the view function
that indicates that the security policy has been applied. I’ve defined it using
a constant with a leading underscore here to indicate that you are not supposed
to import this constant, but instead use it via one of several decorators that
apply the policy. Using our “premium required” example from before, one of those
decorators might look like this:


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


Now, we can use ``decorator_include``, with ``check_security_policy_applied`` as
the decorator. If all my views are decorated in ``@premium_required``,
everything will be fine. Otherwise I will get an exception - at import time, not
at runtime, so I won’t be able to ignore it or find out too late.

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
``_SECURITY_POLICY_APPLIED`` attribute. This means we have successfully moved
from Django’s “open to everyone by default” to “private by default”.




Solution 3 - introspection
--------------------------

TODO  - as a test that runs against your URLconf






Helpful patterns: make it hard for people to add exceptions thoughtlessly.

- each exception in a list has a comment justifying its presence. This establishes
  a strong precedence that makes it hard to just add exceptions - they look wrong.

- your “public allowed” decorator contains a mandatory ``rationale`` argument
  in which the developer must provide a string reason for its existence.





Discussion - secure by default
------------------------------


Discussion: security and failing



Good: the wrong thing looks long
Better: the wrong thing is harder than the right thing
Best: the wrong thing is impossible


Applying security checks in a CBV base class can be a nice pattern, because it
is likely that new code added to a module will follow the existing code, use the
same base classes etc. It will be harder to not do this, and code will look
wrong if it doesn’t.




CBVs, use a base class for security policy - wrong thing looks wrong or is
harder
