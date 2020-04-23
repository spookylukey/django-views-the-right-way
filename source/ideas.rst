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
miracle for me - except it wasn't. Instead of sticking things on ``self``, I was
using local variables, and so my linter was pointing out my mistakes every step
of the way - e.g. undefined and unused locals - until everything was in shape,
at which point the code worked. (I'm using flake8 in emacs, but most IDEs will
have just as capable linters that will catch the same errors).

The opposite refactoring would not have worked like this.
