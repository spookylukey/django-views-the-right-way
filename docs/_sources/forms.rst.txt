Forms
=====

The fundamental pattern for a view that handles a form is covered fully in the
`Django form docs
<https://docs.djangoproject.com/en/stable/topics/forms/#the-view>`_, so I don't
have much to add, except a few notes:

* You don't need to use ``FormView``, and I recommend you don't.

* You don't actually need ``Form`` either. It's an API that provides a very
  helpful set of behaviours (validation etc.), but it's entirely possible to
  build forms in Django without it. You need to know how forms work at the `HTML
  level <https://developer.mozilla.org/en-US/docs/Learn/Forms>`_, and you need
  to process `request.GET
  <https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpRequest.GET>`_
  or `request.POST
  <https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpRequest.POST>`_
  yourself to get the submitted data and do something with it.

  Normally, this would be very tedious compared to using ``Form``, but in some
  cases it will be better. For example, if you have a page with dynamically
  generated controls (e.g. lots of buttons or input boxes) it can be easiest to
  build them up and process them without using ``Form``.

* If you need multiple buttons on the same form, that do different things, you
  need to understand how this works at the HTML level. The button that is
  pressed becomes a “successful” control, which means the ``request.POST`` (or
  ``request.GET``) dictionary will get an entry with that control's ``name``
  attribute.

  So it looks like this:

  Template:

  .. code-block:: html+django

     <form action="" method="POST">
         {% csrf_token %}
         {{ form }}
         <input type="submit" name="save" value="Save">
         <input type="submit" name="preview" value="Preview">
     </form>

  View:

  .. code-block:: python

     def my_view(request):
         if request.method == 'POST':
             if 'preview' in request.POST:
                 # Do preview thing...

  You may have to do something similar for multiple forms on one page.

That's it! Next up: :doc:`preconditions`.

Discussion: Complex form cases
------------------------------

Why not ``FormView``? Of all the CBVs, it is perhaps the most tempting, due to
the control flow boilerplate that it eliminates. But overall, I still feel it is
not worth it.

First, it requires you to know and use a second API (``get_form_class``,
``form_valid``, ``get_initial`` etc.). All of these are more awkward to use than
just using ``Form`` directly.

It also makes some relatively common things much harder to do, and provides a
very bad starting point for most customisations.

For example, if you find you have a page that has two forms on it (perhaps
alternative flows that the user can choose between), ``FormView`` will cause you
lots of pain.

Or if you have form handling as well as something else (such as a list of
items), you will be in confusion if you are trying to use ``FormView``, even
more so if you've forgotten how to use the ``Form`` API directly.

Another example is when you need multiple different submit buttons, which do
something different. This is an easy thing in HTML/HTTP, and easy if you are
using ``Form`` directly and in charge of the control flow yourself, as outlined
above, but horrible if you are trying to fit it into ``FormView``.
