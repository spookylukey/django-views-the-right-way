Adding data to a template
=========================

Suppose we have some data that we want to use in a template. We therefore need
to pass that data into the template's “context”. It could be anything — a simple
value or a list of objects retrieved using the ORM. Using :ref:`the-pattern` I
described earlier, how do we do that?

For the sake of argument, we are going to put today's date into the context,
with the name ``today``, and I'm going to assume you are writing the home page
view for your site.

As we said, the answer to how do anything in a view is “Just do it”:

.. code-block:: python

   from datetime import date

   def home(request):
       return TemplateResponse(request, "home.html", {
           'today': date.today(),   # This is the line you add
       })

(Ignoring imports we already added)

We're going to let the template decide how to format the date (most likely using
the `date filter
<https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#date>`_), so we
just use the ``date`` object rather than a string. Our pattern already had an
empty context dictionary sitting there, waiting to be filled up, so we just put
the value right in. Done!

There is a variation on this, which is also very simple and to some people may
be completely obvious, which is that sometimes it helps to pull out the context
data into a variable first, especially if we are conditionally adding data to
it:

.. code-block:: python

   def home(request):
       context = {}
       if date.today().weekday() == 0:
           context['special_message'] = 'Happy Monday!'
       return TemplateResponse(request, "home.html", context)

Next up: :doc:`common_context_data`


Discussion: embarrassingly simple?
----------------------------------

This code is so simple it might not seem worth mentioning. Yet, with Class Based
Views, the equivalent is anything but simple. Suppose we start with a
``TemplateView``, or a subclass:

.. code-block:: python

   class HomeView(TemplateView):
       template_name = "home.html"


The context dictionary passed to the template is nowhere visible in this code.
The fact that there is such as thing as a context dictionary is not obvious —
all this has been hidden from the developer.

The minimum I can possibly write as a developer is to calculate the data
— ``date.today()`` — and pick a name for it — ``'today'``. With the FBV, the code
I actually end up adding is::

      'today': date.today(),

So it's extremely hard to see how this can be improved.

With a CBV, however, what you have to write is this:

.. code-block:: python

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = data.today()
        return context

If I'm lucky then most of this method has already been written for me (in which
case I then have the boilerplate issue mentioned in :ref:`boilerplate`), but it
might not have been. I have to know this API, and there is plenty that can go
wrong — a wrong signature, or failing to call ``super()`` (which may not have
immediate problems, but could cause problems down the road).

Is this a real problem? Am I making a mountain out of a molehill? Look at this
`blog post about putting data on your home page
<https://rasulkireev.com/django-get-context-data>`_. The problem solved by that
post is exactly the same as what I showed above, with different data.

The author's `first attempt
<https://twitter.com/rasulkireev/status/1230974745644060678>`_ involved using
template tags to solve this problem — something he was very embarrassed about.
But he shouldn't be embarrassed — for a newbie, you would have to be a pretty
capable developer to actually successfully pull off all the parts needed for a
`custom template tag
<https://docs.djangoproject.com/en/3.0/howto/custom-template-tags/>`_.

Rather, he struggled for so long because of a bad context that was making a
simple thing hard, and those of us responsible for that bad context should be
the ones who are embarrassed.
