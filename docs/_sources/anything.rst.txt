How to do anything with in a view
=================================

So, you have a template for writing a view function. There are a whole bunch of
changes or actions you might want to do. How do you go about doing them?

The answer to the question of how to do something with function based views is:

   Just do it

That probably isn't very clear yet, so let's have some common examples. Next
up - :doc:`context_data`.


Discussion - directness
-----------------------

The point of this page is to highlight that fact that class based views often
make things far harder than needed. There is ``ListView`` for displaying a list
of items, or ``DetailView`` for displaying a single item, there are dozens of
methods to override, and docs to look up, for doing the simplest things.

These things are unnecessary, and make things much harder than they need to be.
We'll see more examples later.

Developers should understand **what** they are doing when they write a view, and
then the vast majority of things they need to do will be obvious, and won't
require docs or StackExchange answers. They already know how to program, the
things they are doing are often not hard, they just need a context that doesn't
actively prevent them from doing stuff.
