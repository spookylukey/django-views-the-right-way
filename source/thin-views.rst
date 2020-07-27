Thin views
==========

WORK IN PROGRESS!


This section, the last in my guide, is about what **not** to put in a view.

My basic philosophy is that views should:

* deal with incoming HTTP requests
* create outgoing HTTP requests
* refer to enough logic from elsewhere to glue these together

And try not to do anything else. The result is that your views tend to be pretty
simple and not have much logic in them. This is often called “fat models, skinny
views/controllers”, although here I'm focusing on just the view.

Another way to look at it is to imagine that your code, as well as powering a
website, is also going to be used in another way. This could include being part
of a desktop GUI, command line app, a or scheduled tasks that run without any
interactive user.

For that situation, divide up the logic that would be common to both the web
site and the other types of application. Logic that is **common** should **not**
be part of your view function (or live inside ``views.py``).

I tend to take a pragmatic view with this kind of thing. It's often very
difficult to fully shield the view layer from details of the model layer. For
example, for performance, appropriate use of ``select_related`` and
``prefetch_related`` is very important. To know exactly what to include in them
requires knowing what the view and template code is going to do, so it has to be
a view layer decision. At the same time, it leaks details about the kind of FKs
you have at the schema level. My answer is to just live with this, TODO



Example - push actions to model layer
-------------------------------------

This example comes from code I wrote (always a fruitful place to look for
examples of how not to do it...), for a booking system. After adding place
details to your basket, you can choose to “Book now”, or “Put on shelf”.

The code looks something like this (simplified):

.. code-block::

   def view_booking(request, pk):
       booking = request.user.bookings.get(id=pk)

       if request.method == 'POST':
           if 'shelve' in request.POST:
               booking.shelved = True
               booking.save()
               messages.info(request, 'Booking moved to shelf')

      # the rest...

TODO


Example - push schema details to model layer
--------------------------------------------

Use custom QuerySet methods to keep schema details out of the view.

Can't hide your schema altogether.


This doesn't mean that:

Model layer code:

* doesn't have to live inside a ``models.Model`` method
* doesn't have to live inside a ``models.py`` file.

Often it makes sense to pull out related code into functions and modules with a
different structure. Remember that you can also `split up
<https://stackoverflow.com/a/6338719/182604>`_ ``models.py`` into as many
modules as you want (using multiple apps if you want, or not).



TODO!

Thin views / fat models pattern.

Custom QuerySet methods instead of ``.filter()`` in view code.

https://www.dabapps.com/blog/higher-level-query-api-django-orm/

https://simpleisbetterthancomplex.com/tips/2016/08/16/django-tip-11-custom-manager-with-chainable-querysets.html


Discussion: service layer?
--------------------------

Service layer? Probably not
https://www.b-list.org/weblog/2020/mar/16/no-service/
