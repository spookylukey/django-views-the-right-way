Django Views — The Right Way
============================

Welcome to my opinionated guide on how to write views in Django!

**WORK IN PROGRESS** - this is an early draft, you should probably come back
 later...

This guide was inspired by the fact that many people on the internet seem to be
starting with "Class Based Views" (CBVs from now on) as the default way to write
views, to the point that some are even scared to write "function based views"
(FBVs), despite the fact that these are so much easier and simpler. So here I am
to save the day, and show you The Right Way.

The essential part of this guide is very short, because FBVs are very easy and
simple. In fact, the `Django tutorial for views
<https://docs.djangoproject.com/en/3.0/intro/tutorial03/>`_ already has all you
need to know. Just read that, and skip the bits about CBVs, and you'll be fine.

But if you want a different take on the same things, this guide might be for
you. I've also added extra bits for common tasks and patterns in FBVs for which
CBVs are often suggested as the solution. If you read all of it:

* You'll learn how to make your views usually shorter and definitely much
  simpler than if you used CBVs.
* You'll be freed from learning a whole stack of terrifying APIs that were only
  making your life harder (and teaching you bad patterns).
* Instead of learning a bunch of Django specific APIs, you will gain much more
  re-usable knowledge:

  * Some HTTP principles
  * General OOP/multi-paradigm programming principles
  * General Python techniques

Each page is composed of two parts:

1. The business — the **what and how** — a short, definitive guide to The Right Way. As a less
   experienced developer, either in general or in terms of knowledge of Django,
   this part is all you need.

2. Discussion — the **why** — a longer, in-depth explanation of why everyone
   else who tells you differently is wrong :-). It's targeted at slightly more
   experienced developers, and especially those who are responsible for teaching
   or making decisions about the patterns used in a code base. In each one I'll
   tackle one or two different aspects of the comparisons between CBVs and FBVs.

So let's go!

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   thepattern
   anything
   context_data

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
