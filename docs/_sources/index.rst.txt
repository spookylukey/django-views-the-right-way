Django Views — The Right Way
============================

Welcome to my opinionated guide on how to write views in Django! 

It is the result of mistakes made and lessons learned in a range of
Django and Python projects over 15+ years.

It has also been prompted by the fact that “Class Based Views” (CBVs from now
on) seem to have become the default way to teach and learn Django views in some
circles, to the point that some are even scared to write “Function Based Views”
(FBVs).

Perhaps worst of all, some official Django documentation has `well-intentioned
advise that will help to continue the torture of mixins
<https://docs.djangoproject.com/en/stable/topics/class-based-views/mixins/>`_, but
without actually killing you and putting you out of your misery. (After a bit of
“git blaming” it turns out that I'm `credited
<https://github.com/django/django/commit/c4c7fbcc0d9264beb931b45969fc0d8d655c4f83>`_
in the commit log for that page. I hate it when that happens…)

So, in view of all this, here I am to save the day, and show you The Right Way
:-)


The essential part of this guide is very short, because FBVs are very easy and
simple. In fact, the `Django tutorial for views
<https://docs.djangoproject.com/en/stable/intro/tutorial03/>`_ already has all you
need to know. Just read that, and skip the bits about CBVs, and you'll be fine.

But if you want a different take on the same things, this guide might be for
you. I've also added extra bits for common tasks and patterns in FBVs for which
CBVs are often suggested as the solution. I have a few aims:

* I want to show how simple and easy views can be.

* I want you to be freed from learning a whole stack of additional APIs that
  were only making your life harder (and teaching you bad patterns).

* Instead of learning a bunch of Django specific APIs, I want to cover much more
  transferable knowledge:

  * HTTP principles
  * General OOP/multi-paradigm programming principles
  * General Python techniques

And there are some other goodies along the way, like how to type-check all the
URL parameters to your view functions.

Each page is composed of **two parts**, which have **two different audiences**.

First, the business — the **what and how**: a short, definitive guide to The
Right Way. As a less experienced developer, either in general or in terms of
knowledge of Django, this part is all you need. Since this guide is not intended
to be reference documentation, I'll include various links to the official Django
reference docs. All example code can be found in full in the `GitHub repo
<https://github.com/spookylukey/django-views-the-right-way/tree/master/code>`_.

Second, discussion — the **why**: a longer, in-depth explanation of why everyone
else who tells you differently is wrong :-). It's targeted at slightly more
experienced developers, and especially those who are responsible for teaching
other people, or making decisions about the patterns used in a code base. These
discussion sections are really about general programming principles, and how
they apply in Python and Django.

So let's go!

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   the-pattern
   anything
   context-data
   common-context-data
   url-parameters
   detail-view
   list-view
   delegation
   dependency-injection
   redirects
   forms
   preconditions
   thin-views


Something missing? This guide is a **work in progress**, and no matter how much
I add it probably always will be! If you have requests for things to include,
you could file an issue on `GitHub
<https://github.com/spookylukey/django-views-the-right-way>`_.

Caveats and disclaimers etc.
============================

1. Yes, there may in fact be more than one Right Way. But not in this guide!

2. I'm assuming you are writing a ‘classic’ web app or web site — in which
   most of your pages are server-side rendered HTML, with perhaps some Javascript
   loaded onto those pages, as opposed to a site where your server mostly sends
   data (e.g. JSON) to a client-side Javascript web app that puts the pages together.

3. My comments mainly apply to the CBVs that come with Django. Specifically,
   many of my criticisms don't apply to Django Rest Framework, the Django admin
   (which uses a form of CBV), and possibly other implementations. See later
   discussion on this.

4. Although I'm a Django core dev, I'm not speaking for all the Django
   developers. I was actually around when CBVs were first being added to Django,
   and even involved in the design of them a bit, and at the time didn't see the
   things I'm expressing now.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
