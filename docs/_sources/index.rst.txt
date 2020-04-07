.. How to write Django views documentation master file, created by
   sphinx-quickstart on Mon Apr  6 19:12:19 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django Views - The Right Way
============================

Welcome to my opinionated guide on how to write views in Django.

This guide was inspired by the fact that many (wrong) people on the internet are
(wrongly) encouraging the use of "Class Based Views" (CBVs from now on) as both
a superior way of writing views, and also the way to teach those who are
starting out with Django.

This is wrong advice! (Did I mention that?) It's got so bad that some people are
even scared to write "function based views" (FBVs from now on), despite the fact
that these are so much easier and simpler. So here I am to save the day, and
show you The Right Way.

The essential part of this guide is very short, because FBVs are very easy and
simple, but I've added extra bits for common patterns in FBVs. If you read all
of it:

* You'll learn how to make your views shorter and much, much simpler than if you
  use CBVs.
* You'll be freed from a whole bunch of terrifying APIs that were only making
  your life harder.
* You'll learn general Python techniques for good program structure, in contrast
  to Django specific APIs that are actually teaching you bad patterns.

Each page is composed of two parts:

1. The business - a short, definitive guide to The Right Way. As a junior
   developer, this part is all you need.

2. Discussion - a longer, in-depth explanation of why everyone else who tells
   you differently is wrong. It's targeted at slightly more experience
   developers, or junior developers who want to sit at my feet and catch my
   pearls of wisdom.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

Caveats and disclaimers etc.
============================

1. Yes, this guide will be slightly exaggerated in style, and definitely
   arrogant. Because it's more fun to write that way. #SorryNotSorry

2. My comments mainly apply to the CBVs that come with Django. Specifically,
   many of my criticisms don't apply to Django Rest Framework (see later
   discussion), and possibly other implementations.

3. Although I'm a Django core dev, I'm not speaking for all the Django
   developers, and I'm not actually implying they are all stupid (although they
   may be wrong). I was actually around when CBVs were first being added to
   Django, and even involved in the design of them a bit, and at the time didn't
   realise the things I'm expressing now.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
