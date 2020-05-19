How to do anything in a view
============================

So, you have a template for writing a view function. There is something
different you want to do. How should you go about it?

The answer is:

   Just do it.

That probably isn't very clear yet, so I'll cover some common examples. What I
want you to remember is:

* You are in charge. It's your view function. You make it do whatever you want
  it to do, without trying to fit into someone else's pattern. Just do it.

* It's probably not hard and you can probably do it already.

* Sometimes you might have to write a little bit of code to make it do what you
  want, rather than being able to find something already written. But you are a
  software developer, you write code. Take responsibility and just do it.

* It doesn't have to be perfect yet. In time you'll find ways to make your code
  more concise if you find yourself writing the same things over and over. Don't
  be afraid to make some mistakes along the way.

Next up - :doc:`context-data`.


.. _starting-point:

Discussion: Starting points
---------------------------

One of the reasons for the pattern I'm recommending is that it makes a great
starting point for doing anything. The body of the view — the function that
takes a request and returns a response — is right there in front of you, just
ready for you to write some logic. If a developer understands **what a view
is**, and they have some idea of what they want this view to do, then they will
likely have a good idea of what code they need to write. The code structure in
front of them will not be an obstacle.

The same is not true of using CBVs are a starting point. As soon as you need any
logic, you have to start adding configuration or defining methods, which brings
you pain:

* You've got to know which methods to define, which involves knowing this
  massive API.
* You could easily get it wrong in a way which introduces serious bugs. (TODO
  link)
* You've got to add the method, which is extra boilerplate.
* You may need to switch the base class, and understand what that will do.

We'll see more examples of this as we go through.

Some people will say we should use a CBV for the really simple cases, and then
switch to an FBV later as needed. But in reality that doesn't happen. Most
developers are much more likely to stick with the existing structure of the
code, because that is a safe option, and usually involves less work. Plus, once
you have started down the CBV route, you quickly gain various mixins etc. that
make using plain functions less attractive.
