https://twitter.com/rasulkireev/status/1230974745644060678

https://twitter.com/rasulkireev/status/1231267109717626880

https://iheanyi.com/journal/2020/04/04/dynamic-page-titles-in-django/


Boilerplate

Starting point




DetailView vs get_object_or_404
shortcuts


Security




---

CCIW - Transformed PopupEmailAction to CBVs

- Use of ``self.foo`` to pass data around is eliminated - just have ``foo``
  - explicitly passed

  - closures

- no hidden inputs
- everything checked by flake8, even better by mypy
  - positively and negatively - unused local variables highlighted, typos



Explicit contract - defined by the signature of the functions.
 - this is wonderful for code comprehension
 - it also works great for static type checkers


    
Length - not the most important measure

Code got significantly more succinct:

Before:
631 tokens
83 non-blank lines
103 total lines

After:
542 tokens
86 non-blank lines
96 total lines

(tokens are the most objective measure of size by my book)

This is despite the fact that before, I was using only minimal CBV base classes
that I had explicitly designed for my own purposes. It would have been more
extreme if I had been trying to use Django's CBVs.


Accuracy - the refactor was bugless on my first attempt, which is pretty much a
miracle for me - except it wasn't a miracle, there were good reasons why it
happened. Instead of common setup code that was storing data on ``self`` for use
by other methods, I was just using local variables, and so my linter was pointing out
my mistakes every step of the way - e.g. undefined and unused locals - until
everything was in shape, at which point the code worked. (I'm using flake8 in
emacs, but most IDEs will have just as capable linters that will catch the same
errors).

The opposite refactoring would not have worked like this.


Automated static analysis that linters can do is just a sign of a deeper
reality - the FBV is simpler and easier to understand. The fact that it reaches
a stage where an automated process can understand it and catch most errors,
despite Python's dynamism, is great, but what is even better is the benefit for
humans trying to understand this kind of code.


My code is more boring now, in the best sense. There are few tricks or clever
techniques. These are still allowed, but reserved for when you really need them
and get benefit from them.


Security:

e.g. this view that shows the return page when people come back from PayPal. It
needs ``csrf_exempt`` because PayPal insists on making browsers do a POST
request to this page (even though I don't use the POST data). But @csrf_exempt
is a red flag for security, so this needs auditing to ensure that I'm not, in
fact, doing anything with the POST data that makes assumptions about its
connection to the current session or logged in user.

Here is the CBV I had.

CBV::

    class BookingPayDone(BookingPayBase):
        metadata_title = "Booking - payment complete"
        template_name = "cciw/bookings/pay_done.html"

    pay_done = csrf_exempt(BookingPayDone.as_view())


BookingPayDone inherits from BookingPayBase which inherits from CciwBaseView
which inherits from TemplateView which inherits from View (all my own base
classes in this case). You're going to need to investigate all those bases
classes to be sure about what they do.

Well, presumably TemplateView at least would be safe, so do I really need to
check that? Before you answer, consider this: previously I was using Django's
TemplateView as a base class, and the first version of my view, which looked
almost identical to the above, wouldn't work at all - a fact I discovered after
deploying to production. Can you guess why? Are you sure you know what your base
classes are doing?


Alternatively, you could audit this FBV, which is the new version and does
everything I need::

    @csrf_exempt
    def pay_done(request):
        return TemplateResponse(request, 'cciw/bookings/pay_done.html', {
            'title': 'Booking - payment complete',
            'stage': BookingStage.PAY,
        })

Which would you rather? And this is a very simple example, real CBVs often gain
far more base classes.
