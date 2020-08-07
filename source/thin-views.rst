Thin views
==========

WORK IN PROGRESS!


This section, the last in my guide, is about what **not** to put in a view.

My basic philosophy is that views should:

* deal with incoming HTTP requests
* create outgoing HTTP requests
* refer to enough logic from elsewhere to glue these together.

And try not to do anything else. The result is that your views tend to be pretty
simple and not have much logic in them. This is often called “fat models, skinny
views/controllers”, although here I'm focusing on just the view.

Another way to look at it is to imagine that your code, as well as powering a
website, is also going to be used in another way. This could include being part
of a desktop GUI, command line app, a or scheduled tasks that run without any
interactive user.

Then, divide up the logic that would be common to both the web site and the
other types of application. Logic that is **common** should **not** be part of
your view function (or live inside ``views.py``).

We'll have a look at a few examples to illustrate this.


Example - push actions to the model layer
-----------------------------------------

This example comes from code I wrote (always a fruitful place to look for
examples of how not to do it...), for a booking system. After adding place
details to your basket, you can choose to “Book now”, or “Put on shelf”.

The view code looks something like this (simplified):

.. code-block::

   def view_booking(request, pk):
       booking = request.user.bookings.get(id=pk)

       if request.method == 'POST':
           if 'shelve' in request.POST:  # pressed the 'Put on shelf' button
               booking.shelved = True
               booking.save()
               messages.info(request, 'Booking moved to shelf')

      # the rest...


The issue with this code is that the view has too much knowledge about what
“putting on the shelf” means. It may be in the future that we don't use a
boolean ``shelved`` property, but perhaps some multi-value flag, or something
else entirely. With a different schema, there might be some other objects that
need to be saved. We want this logic to be in one place, so that it will always
be used correctly if some other part of our code needs to do the same thing, and
to avoid complicating the view with details it doesn't really care about.

So, instead of having:


.. code-block:: python

               booking.shelved = True
               booking.save()

we should write:

.. code-block:: python

               booking.put_on_shelf()

It then becomes the responsibility of the ``Booking.put_on_shelf()`` method to
handle the ``shelved`` attribute or whatever else needs to be done.

This is a very simple example, and it might not look much different. But if you
get into the habit of moving this kind of logic out of the view layer, it will
help a lot.

Example - push filtering to the model layer
-------------------------------------------

Continuing the example above, when we display a list of bookings to the user, we
might want to do different types of filtering. For example, we might want to
display “in the basket” bookings, “on the shelf” bookings (as above), or
“confirmed for this year“ bookings. Confirmed bookings are controlled (at the
moment) with another boolean flag.

We could do this filtering in our view functions something like as follows::

.. code-block:: python

   # In the basket
   Booking.objects.filter(shelved=False, confirmed=False)

   # On the shelf
   Booking.objects.filter(shelved=True, confirmed=False)

   # Confirmed for this year
   Booking.objects.filter(confirmed=True, start_date__year=date.today().year)


But, as before, this it putting too much information about the schema directly
in the view. This has some bad effects:

* our code is less readable - we are going to have to work out what those
  filtering conditions actually refer to. We could add a comment against each
  one, as in the code above. But I always try to interpret comments like that as
  a hint that is telling me that my code isn't clear by itself.

* we'll have to duplicate that logic if we want it in more than one place.

* if we change the schema we'll have to change all these places.

Instead, let's listen to the hints of the comments we are tempted to write, and
change our code like this:

.. code-block:: python

   Booking.objects.in_basket()

   Booking.objects.on_shelf()

   Booking.objects.confirmed().for_year(today().year)

The question now is how do we do that?


Chainable custom QuerySet methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~






Where to put this code
----------------------

Model layer code:

* doesn't have to live inside a ``models.Model`` method
* doesn't have to live inside a ``models.py`` file.
* doesn't have to refer to "database models". We are really talking about
  "domain models" here, which can often be backed directly by a Django database
  model, but it could be other classes or functions.

Often it makes sense to pull out related code into functions and modules with a
different structure. Remember that you can also `split up
<https://stackoverflow.com/a/6338719/182604>`_ ``models.py`` into as many
modules as you want (using multiple apps if you want, or not).



Discussion: service layer?
--------------------------

Service layer? Probably not
https://www.b-list.org/weblog/2020/mar/16/no-service/


Discussion: pragmatism / purity
-------------------------------

I tend to take a pragmatic view with this kind of thing. It's often very
difficult to fully shield the view layer from details of the model layer.

For example, for performance, appropriate use of ``select_related`` and
``prefetch_related`` is very important. To know exactly what to include in them
requires knowing what the view and template code is going to do, so it has to be
a view layer decision. At the same time, it requires knowing details about the
kind of FKs you have at the schema level. Performance fixes often require this
kind of whole-system thinking which necessarily breaks some of the abstractions


Can't hide your schema altogether.



Links
-----


https://www.dabapps.com/blog/higher-level-query-api-django-orm/

https://simpleisbetterthancomplex.com/tips/2016/08/16/django-tip-11-custom-manager-with-chainable-querysets.html
