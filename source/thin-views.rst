Thin views
==========

This section, the last in my guide, is about what **not** to put in a view.

My basic philosophy is that views should:

* deal with incoming HTTP requests
* create outgoing HTTP requests
* refer to enough logic from elsewhere to glue these together.

And try not to do much else. The result will be that your views tend to be
pretty simple and not have much logic in them. This is often called “fat models,
skinny views/controllers”, although here I'm focusing on just the view.

Another way to look at it is to imagine that your code, as well as powering a
website, is also going to be used in another way. This could include being part
of a desktop GUI, command line app, or scheduled tasks that run without any
interactive user. Then, divide up the logic that would be common to both the web
site and the other types of application. Logic that is **common** should **not**
be part of your view function or view layer utilities.

We'll have a look at a few examples to illustrate this.


Example: push actions to the model layer
----------------------------------------

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
need to be saved, or some other things that need to be done. We want this logic
to be in one place, so that it will always be used correctly if some other part
of our code needs to do the same thing, and to avoid complicating the view with
details it doesn't really care about.

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

Note that we did **not** move the ``messages.info()`` call into the model layer.
It is concerned with putting a message into a web page, and so stays in the view
layer where it belongs.

Example: push filtering to the model layer
------------------------------------------

Continuing the example above, when we display a list of bookings to the user, we
might want to do different types of filtering. For example, we might want to
display “in the basket” bookings, “on the shelf” bookings (as above), or
“confirmed for this year“ bookings. Confirmed bookings are controlled with
another boolean flag, at least for the moment.

We could do this filtering in our view functions something like as follows:

.. code-block:: python

   # In the basket
   Booking.objects.filter(shelved=False, confirmed=False)

   # On the shelf
   Booking.objects.filter(shelved=True, confirmed=False)

   # Confirmed for this year
   Booking.objects.filter(confirmed=True, start_date__year=date.today().year)


But, as before, this it putting too much information about the schema directly
in the view. This has some bad effects:

* we'll have to duplicate that logic if we want it in more than one place.

* if we change the schema we'll have to change all these places.

* our code is less readable — we are going to have to work out what those
  filtering conditions actually refer to. We could add a comment against each
  one, as in the code above. But I always try to interpret comments like that as
  “code smells”. They are hints telling me that my code isn't clear by itself.

I agree with Jamie Matthews that `using filter directly in view code is a
usually an anti-pattern
<https://www.dabapps.com/blog/higher-level-query-api-django-orm/>`_. So, let's
listen to those hints, and change our code so we no longer need the comments:

.. code-block:: python

   Booking.objects.in_basket()

   Booking.objects.on_shelf()

   Booking.objects.confirmed().for_year(date.today().year)


We also want to be able to use the same functionality from a user object, for
example:

.. code-block:: python

   user = request.user
   context = {
       'basket_bookings': user.bookings.in_basket()
   }
   # etc.

If there is a user involved, I usually prefer code that looks like this. By
getting into the habit of starting all user-related queries with ``user``,
whether I'm displaying a list or a retrieving a single item, it’s harder to
forget to add access controls, so I will be less prone to `insecure direct
object reference <https://portswigger.net/web-security/access-control/idor>`_
security issues.

The question now is, how do we create an interface like that?


Chainable custom QuerySet methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The answer is we define ``in_basket()``, ``on_shelf()``, ``confirmed()``,
``for_year()`` etc. as custom ``QuerySet`` methods. By making them ``QuerySet``
methods, rather than just ``Manager`` methods, we can make them chainable as
above, so that we can use ``for_year()`` after ``confirmed()``, for example, or
after other methods.

The `Django docs for QuerySets and Managers
<https://docs.djangoproject.com/en/stable/topics/db/managers/>`_ will show you
how to do it, but due to the ``Manager``/``QuerySet`` split, it can get a bit
overwhelming. So here is the basic pattern:

.. code-block:: python

   class BookingQuerySet(models.QuerySet):
       # Custom, chainable methods added here, which will
       # do lower level 'filter', 'order_by' etc.
       def in_basket(self):
           return self.filter(shelved=False, confirmed=False)

       def for_year(self, year):
           return self.filter(start_date__year=year)

       # etc.


   class Booking(models.Model):
       # fields etc

       objects = BookingQuerySet.as_manager()


If you additionally want a custom ``Manager`` class with other methods that are not
part of the ``QuerySet`` interface you can use `Manager.from_queryset
<https://docs.djangoproject.com/en/stable/topics/db/managers/#from-queryset>`_.

To make the most of this pattern, you should be aware of `all the cool things
that QuerySet can do
<https://docs.djangoproject.com/en/stable/ref/models/querysets>`_. For example,
this code will construct a ``QuerySet`` that has everything that is either on
the shelf or in the basket:

.. code-block:: python

   on_shelf_or_in_basket = Booking.objects.in_basket() | Booking.objects.on_shelf()

The new ``QuerySet`` is constructed without executing a query. When you evaluate
``on_shelf_or_in_basket``, you'll execute a single DB query that will return
both types of bookings. So we get efficient code that is also readable and
doesn't leak our schema inappropriately.


Where to put this code
~~~~~~~~~~~~~~~~~~~~~~

If not in the view, where does this code actually live? If you are going for the
“fat model” arrangement, as above, often this gets put into a ``models.py`` file.

But you should note:

* You can split a ``models.py`` file into any number of modules. No need to
  create massive files!
* Model layer code doesn't have to refer to "database models". We are really talking about
  "domain models" here, which can often be backed directly by a Django database
  model, but it could be other classes or functions.
* You don't have to put all logic relating to a Django ``Model`` into methods of
  that class. You should “listen to the code”, and also listen to the business
  level requirements, and discover the concepts and divisions that make sense
  for your project.


The end
~~~~~~~

That's the end of the guide! (Apart from discussion sections below, as always). I
hope it has been helpful. If there are some common things I haven't covered,
feel free to `open an issue on GitHub
<https://github.com/spookylukey/django-views-the-right-way>`_.

.. _service-layers:

Discussion: service layer?
--------------------------

A service layer goes further than the above, and creates an interface for
accessing the data in the database that doesn't expose ORM methods at all. In
such an arrangement you would also normally separate your “domain model” classes
from your Django ``Model``.

James Bennett has an excellent post `Against service layers in Django
<https://www.b-list.org/weblog/2020/mar/16/no-service/>`_ that summarises
everything that I would want to say on the topic, so I'm not going to repeat
that. The long and short is — using custom ``Model`` methods and custom
``QuerySet`` methods as your “service layer”, as above, is an approach that will
work really well for a lot of projects.

If you believe that a service layer is essential — for example, using a
repository pattern that doesn't use ``QuerySets`` — then you will probably not
agree with some of the patterns I've suggested. For example, the
:ref:`get_object_or_404 shortcut <shortcuts-vs-mixins>` might strike you as a
weird or terrible idea. However, if you are sold on using the ``QuerySet`` API
(with custom methods) as your interface, then this is just a useful shortcut
that adapts the ``QuerySet`` API for a common case in HTTP applications.


Discussion: pragmatism and purity
---------------------------------

When trying to hide schema details from your view layer, there are some obstacles.

For example, for performance, appropriate use of `select_related
<https://docs.djangoproject.com/en/stable/ref/models/querysets/#django.db.models.query.QuerySet.select_related>`_
and `prefetch_related
<https://docs.djangoproject.com/en/stable/ref/models/querysets/#django.db.models.query.QuerySet.prefetch_related>`_
is very important. To know exactly what to include in them requires knowing what
the view and template code is going to do, so it has to be a view layer
decision. At the same time, it requires knowing details about the kind of
foreign keys you have at the schema level. So it’s difficult to see how we can
properly isolate the layers from each other.

This is actually quite common problem in software — performance fixes often
require whole-system thinking which necessarily breaks some of the abstractions
and layers we put in place.

My answer is to take a pragmatic approach, and usually just put the
``select_related`` calls into the view. Sometimes I might make a ``QuerySet``
method like ``with_foo``, meaning “fetch Foo objects efficiently along with the
main thing”, adding whatever ``select_related`` or ``prefetch_related`` logic is
needed there, but sometimes I feel it isn't worth it.

It is not the end of the world if you fail to 100% insulate your schema from the
rest of the app. You can get benefits from doing it partially, and if you have
some integration tests that exercise the queries constructed by your view code,
you will have a mechanism for finding those places where your schema has leaked
out.
