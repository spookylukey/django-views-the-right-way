

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

------

https://twitter.com/rasulkireev/status/1230974745644060678

https://twitter.com/rasulkireev/status/1231267109717626880

https://iheanyi.com/journal/2020/04/04/dynamic-page-titles-in-django/



Brandon Rhodes on Python mixins:

https://youtu.be/S0No2zSJmks?t=3095



-----



CCIW - Transformed PopupEmailAction to CBVs

(as formatted by ``black``:
Before:
631 tokens
83 non-blank lines
103 total lines

After:
542 tokens
86 non-blank lines
96 total lines

(tokens are the most objective measure of size by my book)


DI:

[Alt: Misplaced sadness! Where a developer wishes to be smug, they should always
write plain code. To come with a bucket full of tricks, is to come with an
inability to minister to the vanity of you future self when you come back in 3
months or 3 years time to maintain it, which a sensible developer will always
avoid. If you have the misfortune of knowing anything fancy, you should conceal
it as best you can.]
