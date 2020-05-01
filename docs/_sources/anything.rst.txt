How to do anything in a view
============================

So, you have a template for writing a view function. There are a whole bunch of
changes or actions you might want to do. How do you go about doing them?

The answer to the question of how to do something with function based views is:

   Just do it

That probably isn't very clear yet, so I'll cover some common examples. What I
want you to remember is:

* You are in charge. It's your view function. You make it do whatever you want
  it to do, without trying to fit into someone else's pattern. Just do it.

* It's probably not hard and you can probably do it already.

* Sometimes you might have to write a little bit of code to make it do what you
  want, rather than being able to find something already written. But you are a
  software developer, you write code. Take responsibility and just do it. In
  time you'll find ways to make your code more concise if you find yourself
  writing the same things over and over.

Next up - :doc:`context_data`.


Discussion — directness
-----------------------

The point of this page is to highlight that fact that class based views often
make things far harder than needed. There is ``ListView`` for displaying a list
of items, or ``DetailView`` for displaying a single item, there are dozens of
methods to override, and docs to look up, all for doing the simplest things.

These things are unnecessary, and make things much harder than they need to be.
We'll see more examples later.

Developers should understand **what** they are doing when they write a view, and
then the vast majority of things they need to do will be obvious, and won't
require docs or StackExchange answers. They already know how to program, the
things they are doing are often not hard, they just need a context that doesn't
actively prevent them from doing stuff.

Many of the problems with CBVs also stem, ultimately, from people trying to
avoid writing any code at all. TODO see "codeless views".
