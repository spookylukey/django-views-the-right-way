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
   :emphasize-lines: 5

   from datetime import date

   def home(request):
       return TemplateResponse(request, "home.html", {
           'today': date.today(),   # This is the line you add
       })


.. note::

   **Formatting:** I'm formatting my code examples in line with PEP8, and after
   that for clarity, especially to highlight things that have changed. So this
   example adds one line to our pattern, and I've formatted it accordingly.
   There is no need to follow the formatting, and you (or your tools) might
   have other ideas!

   **Imports:** For brevity I'll omit any imports I've already mentioned. If you
   want full source code, have a look at the `code folder
   <https://github.com/spookylukey/django-views-the-right-way/tree/master/code>`_.

The template will decide how to format the date (most likely using the `date
filter <https://docs.djangoproject.com/en/stable/ref/templates/builtins/#date>`_),
so we used a ``date`` object rather than a string. Our pattern already had an
empty context dictionary sitting there, waiting to be filled up, so we just put
the value right in. Done!

There is a variation on this, which is that sometimes it helps to pull out the context
data into a variable first, especially if we are conditionally adding data to
it:

.. code-block:: python

   def home(request):
       today = date.today()
       context = {
           'today': today,
       }
       if today.weekday() == 0:
           context['special_message'] = 'Happy Monday!'
       return TemplateResponse(request, "home.html", context)

That's it! Next up: :doc:`common-context-data`.


Discussion: Embarrassingly simple?
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

With a CBV, however, what you have to add is this:

.. code-block:: python

       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           context['today'] = date.today()
           return context

If I'm lucky then most of this method has already been written for me (in which
case we then have a :ref:`boilerplate <boilerplate>` issue), but it might not
have been. I have to know this API, and there is plenty that can go wrong — a
wrong signature, or failing to call ``super()`` (which may not have immediate
problems, but could cause problems down the road) — enough that `people need to
write blog posts about it <https://vsupalov.com/pass-context-to-django-cbv/>`_.

Is this a real problem? Am I making a mountain out of a molehill?

Here is another `blog post about putting data on your home page
<https://rasulkireev.com/django-get-context-data>`_. The author's `first attempt
<https://twitter.com/rasulkireev/status/1230974745644060678>`_ involved using
template tags to solve this problem — something he was very embarrassed about.
But he shouldn't be embarrassed — for a newbie, you would have to be a pretty
capable developer to actually successfully pull off all the parts needed for a
`custom template tag
<https://docs.djangoproject.com/en/stable/howto/custom-template-tags/>`_.

Rather, he struggled for so long because of a bad :ref:`starting point
<starting-point>` that was making a simple thing hard. If we as the Django
community have made this hard, we are the ones who should be embarrassed.


.. _boilerplate:

Discussion: Boilerplate
-----------------------

With the above in mind, do we have more boilerplate with CBVs or FBVs?

Before we answer that, the first thing to note about boilerplate (by which I
mean repeated code that just Needs To Be There For Some Reason) is that a small
amount of it is not a big problem in software development. **We don't spend most
of our time typing, we spend most of our time reading code. This means that
clarity is much more important than shaving a few keystrokes**. Arguments about
small amounts of boilerplate should not be the major factor.

The real issue with boilerplate, in fact, is not how much typing it involves,
but that verbose code hinders comprehension due to the low signal-to-noise
ratio. **Boilerplate reduction should be almost entirely about code
comprehension, not typing reduction.**

For example, if we wanted, we could reduce the “repetition” of having
``request`` as an parameter to each view function using threadlocals and an
import. We could go further, and remove the import using some magic like web2py
does. But `we recognise both of these as bad ideas
<https://youtu.be/S0No2zSJmks?t=1716>`_, because they reduce clarity. Those
functions have ``request`` as a parameter because it is an input to the
function. Making it an implicit one, instead of an explicit one, would hurt you
in lots of ways.

With that said, let's do a comparison. Once you have added the need for context
data, as above, the CBV equivalent to the view I wrote above is as follows:

.. code-block:: python

   from django.views.generic import TemplateView


   class HomeView(TemplateView):
       template_name = "home.html"

       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           context['today'] = date.today()
           return context


.. code-block:: python

   urlpatterns = [
       path('', views.HomeView.as_view(), name='home'),
   ]


This is now significantly longer than the FBV, by any measure. I think this is a
fairer comparison in terms of boilerplate, because you almost always need to add
extra context data. In fact, so many people have found this, that they have
created boilerplate generators/snippets for starting new CBVs — such as `this
for emacs
<https://github.com/pashinin/emacsd/blob/c8e50e6bb573641f3ffd454236215ea59e4eca13/snippets/python-mode/class>`_
and `this for vim
<https://github.com/honza/vim-snippets/blob/087d3e7c72912baeb6b1d7ba626e61d50092c848/UltiSnips/django.snippets#L357>`_,
and `this for Sublime Text
<https://github.com/mvdwaeter/dotfiles/blob/60673ae395bf493fd5fa6addeceac662218e1703/osx/Sublime%20Text/get_context_data.sublime-snippet>`_.

The result of this is that if you `search GitHub
<https://github.com/search?q=get_context_data&type=Code>`_ for
``get_context_data``, you'll find hundreds and hundreds of examples that look
like this, which otherwise wouldn't make much sense.

.. code-block:: python

   class HomeView(TemplateView):
       # ...

       def get_context_data(self):
           context = super(HomeView, self).get_context_data()
           return context

In other words:

* The boilerplate you need for a basic CBV is bigger than for an FBV.
* It's so big and tedious that people feel the need of snippets libraries.

Maybe the boilerplate issue will be better when it comes to ``DetailView`` etc?
:ref:`We'll see about that <DetailView comparison>`.

OK, we have more boilerplate, but have we improved code comprehension? Well, the
CBV is very explicit about use of templates, but so is the FBV. Now that we've
added ``get_context_data``, the CBV is clear about context data, but so was the
FBV. However, CBV has made the key elements of the view :ref:`invisible
<visibility>`, as we noted before, and obscured all the control flow, so I think
it is difficult to argue this is a win for comprehension.




