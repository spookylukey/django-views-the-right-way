
- The Pattern

- How to do X with a function based view: do X
  - It's easy!


- Context data

  - Discussion: embarrassingly simple

- Conditional context data

  - Discussion: control flow

  - Discussion: 
- Common context data


- URL parameters
  - Discussion: checkable URLconf


- Display an object.
  
  - Discussion: 
    
- Redirect
  - HTTP level

  - Discussion: codeless views?

Discussion -

  - RedirectView - rewrite example in docs - https://docs.djangoproject.com/en/3.0/ref/class-based-views/base/#django.views.generic.base.RedirectView

Original::
    from django.shortcuts import get_object_or_404
    from django.views.generic.base import RedirectView

    from articles.models import Article

    class ArticleCounterRedirectView(RedirectView):

        permanent = False
        query_string = True
        pattern_name = 'article-detail'

        def get_redirect_url(self, *args, **kwargs):
            article = get_object_or_404(Article, pk=kwargs['pk'])
            article.update_counter()
            return super().get_redirect_url(*args, **kwargs)

Function::

    from django.http import HttpResponseRedirect
    from django.urls import reverse
    from django.shortcuts import get_object_or_404

    from articles.models import Article

    def article_counter_redirect_view(request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.update_counter()
        query_string = request.META.get('QUERY_STRING', '')
        return HttpResponseRedirect(reverse('article-detail', kwargs={'pk': pk})
                                    + ('?' + query_string) if query_string else '')

Function wrapper of CBV::

    from django.shortcuts import get_object_or_404
    from django.views.generic.base import RedirectView

    from articles.models import Article

    def article_counter_redirect_view(request, pk):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        article.update_counter()
        return RedirectView.as_view(
            pattern_name='article-detail'
            query_string=True,
            permanent=False,
        )(request, pk=pk)


        



Discussion - DetailView vs get_object_or_404

https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-display/#detailview


Original::

    from django.utils import timezone
    from django.views.generic.detail import DetailView

    from articles.models import Article

    class ArticleDetailView(DetailView):

        model = Article

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['now'] = timezone.now()
            return context

Rewritten::

    from django.template.response import TemplateResponse
    from django.shortcuts import get_object_or_404
    from django.utils import timezone

    def article_view(request, slug):
       return TemplateResponse(request, "my_app/article_detail.html", {
           'article': get_object_or_404(Article.objects.all(), slug=slug),
           'now': timezone.now(),
       })


Comparisons:
- Compare template ``object``
- Suppose we need to change CBV to be filtered QuerySet, not all objects.

  ``model`` -> ``queryset``

- Suppose we need it to be filtered according to something in request
  ``queryset`` attribute -> ``get_queryset`` method.


  Discussion - convention vs configuration (template name)

  Discussion - shortcuts vs mixins

   - Brandon Rhodes



- Simple customisation
  - keyword args in the URLconf

- Custom logic

  - Write some code. Do it yourself, it's not hard.
  - Discussion: codeless views?
    History of CBVs. 

https://twitter.com/rasulkireev/status/1230974745644060678

https://twitter.com/rasulkireev/status/1231267109717626880

https://iheanyi.com/journal/2020/04/04/dynamic-page-titles-in-django/


Discussion - Boilerplate

Discussion - Starting point
 - guy who created template tags just to add something to the context
   


   


---

Customising in the middle - Callbacks

 - Discussion - Callbacks vs template method

   - Use CCIW example of PopupEmailAction

---
Customising in the middle - Advanced callbacks 

---

Customising the start - pre-conditions

- Decorators

Customising the start - delegating

- Discussion: re-usable functionality

  Classes vs functions for re-usability

---

Customising the end



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
request to this page (even though I don't use the POST data). But
``@csrf_exempt`` is a red flag for security, so this needs auditing to ensure
that I'm not, in fact, doing anything with the POST data that makes assumptions
about its connection to the current session or logged in user.

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
TemplateView as a base class, rather than my own, and the first version of my
view, which looked almost identical to the above, wouldn't work at all - a fact
I discovered after deploying to production. Can you guess why? Are you sure you
know what your base classes are doing?


Alternatively, you could audit this FBV, which is the new version and does
everything I need::

    @csrf_exempt
    def pay_done(request):
        return TemplateResponse(request, 'cciw/bookings/pay_done.html', {
            'title': 'Booking - payment complete',
            'stage': BookingStage.PAY,
        })

Which would you rather? And this is a very simple example, real CBVs often gain
far more base classes and complexity.



URL checking

https://gist.github.com/spookylukey/ebc68928d831da1f89bce15d9e18809d

Especially useful if you have registered a view in more than one way


e.g.

/foo/<int:year>/

/foo/<int:from_year>-<int:to_year>/


def show_foo(request, year=None, from_year=None, to_year=None)


Type checker will ensure that you don't accidentally have something like:

def show_foo(request, year, from_year=None, to_year=None)


-----
Redirects
 - HTTP
   

URL conf

RedirectView vs make_redirect

Discussion - views in the URLconf

-----


View factory / mass produced views

- Redirect views for a whole family of views, each needing same kwargs passed on.

  - Will do the same custom logic each time.
  
-----

Discussion - convention or configuration




--------------------

MRO problem:

Before::


    class AjaxMroFixer(type):

        def mro(cls):
            classes = type.mro(cls)
            # Move AjaxyFormMixin to one before last that has a 'post' defined.
            new_list = [c for c in classes if c is not AjaxyFormMixin]
            have_post = [c for c in new_list if 'post' in c.__dict__]
            last = have_post[-1]
            new_list.insert(new_list.index(last), AjaxyFormMixin)
            return new_list


    class BookingAccountDetails(DefaultMetaData, AjaxyFormMixin, TemplateResponseMixin, BaseUpdateView, metaclass=AjaxMroFixer):
        metadata_title = "Booking - account details"
        form_class = AccountDetailsForm
        template_name = 'cciw/bookings/account_details.html'
        success_url = reverse_lazy('cciw.bookings.views.add_place')
        extra_context = {'stage': 'account'}

        def get_object(self):
            return self.request.booking_account

        def form_valid(self, form):
            messages.info(self.request, 'Account details updated, thank you.')
            return super(BookingAccountDetails, self).form_valid(form)


After::
  
    @booking_account_required
    @ajax_form_validate(AccountDetailsForm)
    def account_details(request):
        form_class = AccountDetailsForm

        if request.method == "POST":
            form = form_class(request.POST, instance=request.booking_account)
            if form.is_valid():
                form.save()
                messages.info(request, 'Account details updated, thank you.')
                return next_step(request.booking_account)
        else:
            form = form_class(instance=request.booking_account)
        return TemplateResponse(request, 'cciw/bookings/account_details.html', {
            'title': 'Booking - account details',
            'stage': BookingStage.ACCOUNT,
            'form': form,
        })


``account_details`` is only slightly longer than ``BookingAccountDetails`` (129
tokens vs 102), despite the fact that it includes all the form flow control
logic and all other logic, rather than delegating to base classes. However, it
is many times easier to understand, and no crazy metaclass fixes are necessary.



------

ListView

https://docs.djangoproject.com/en/3.0/topics/pagination/#using-paginator-in-a-view-function

def listing(request):
    contact_list = Contact.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list.html', {'page_obj': page_obj})


# Rewritten:

def listing(request):
    context = {}
    context.update(paged_object_list_context(request, Contact.objects.all(), paginate_by=25))
    return TemplateResponse(request, 'list.html', context)



Writing ``paged_object_list_context`` is left as an exercise for you! I'm not
being lazy, actually — adding these kind of utilities to your code is what every
developer should learn to do, and in a project you would expect to have a small
library of this kind of thing that is specific to your project and encapsulates
your own patterns and conventions. This is far superior to contorting your code
with method overrides that are necessary only because of the structure handed to
you by someone else.

Yes, using ``paged_object_list_context`` is very slightly longer than just
adding a ``paginate_by`` attribute to a ``ListView``. But the benefits are huge
— you stay in full control of your view function and it remains readable and
extremely easy to debug or further customise. You also have a utility that is
separately testable.


def paged_object_list_context(request, queryset, paginate_by=25):
    paginator = Paginator(queryset, paginate_by)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'page_obj': page_obj}
