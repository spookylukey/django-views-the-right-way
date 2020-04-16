Django Views — The Right Way
============================

Welcome to my opinionated guide on how to write views in Django!

This guide was inspired by the fact that many people on the internet seem to be
starting with "Class Based Views" (CBVs) as the default way to write views, to
the point that some are even scared to write "function based views" (FBVs from
now on), despite the fact that these are so much easier and simpler. So here I
am to save the day, and show you The Right Way.

The essential part of this guide is very short, because FBVs are very easy and
simple, but I've added extra bits for common patterns in FBVs. If you read all
of it:

* You'll learn how to make your views usually shorter and definitely much
  simpler than if you used CBVs.
* You'll be freed from learning a whole stack of terrifying APIs that were only
  making your life harder.
* You'll learn general Python techniques for good program structure, in contrast
  to Django specific APIs that are actually teaching you bad patterns (in my
  opinion).

Each page is composed of two parts:

1. The business - a short, definitive guide to The Right Way. As a junior
   developer, this part is all you need.

2. Discussion - a longer, in-depth explanation of why everyone else who tells
   you differently is wrong :-). It's targeted at slightly more experienced
   developers.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

Caveats and disclaimers etc.
============================

1. Yes, there may in fact be more than one Right Way. But not in this guide!

2. My comments mainly apply to the CBVs that come with Django. Specifically,
   many of my criticisms don't apply to Django Rest Framework, the Django admin
   (which uses a form of CBV), and possibly other implementations. See later
   discussion on this.

3. Although I'm a Django core dev, I'm not speaking for all the Django
   developers. I was actually around when CBVs were first being added to Django,
   and even involved in the design of them a bit, and at the time didn't see the
   things I'm expressing now.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
