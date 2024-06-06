from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import DetailView,ListView
from . import models, forms
from accounts.models import UserAccount
from django.contrib import messages
from django.views import View
from  django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

def send_transaction_email(user,amount,subject,template):
    message = render_to_string(template,{'user': user,'amount':amount })
    send_email =EmailMultiAlternatives(subject,"",to =[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()

class BookDetail(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'Books/detaile.html'

    def post(self, request, *args, **kwargs):
        review_form = forms.ReviewForm(data=self.request.POST)
        book = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = models.Review.objects.filter(book=book)
        review_form = forms.ReviewForm()

        context['book'] = book
        context['reviews'] = reviews
        context['review_form'] = review_form
        return context
    

class BorrowBookView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = get_object_or_404(models.Book, pk=book_id)
        user_account = get_object_or_404(UserAccount, user=request.user)
        
        if user_account.balance < book.price:
            messages.warning(request,"There is no money in the account")
            return redirect('home')
        
        book.account = user_account
        user_account.balance -= book.price
        book.buye = True
        messages.success(self.request, 'Borrow book Successfully check your email')
        send_transaction_email(user_account.user,book.price,'Book Borrow','Books/borrow_email.html')
        user_account.save()
        book.save()   
        return redirect('profile')
class ReturnBookView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = get_object_or_404(models.Book, pk=book_id)
        user_account = get_object_or_404(UserAccount, user=request.user)
        book.account = None
        user_account.balance += book.price
        book.buye = False
        messages.success(self.request, 'Return book Successfully check your email')
        send_transaction_email(user_account.user,book.price,'Return Book','Books/return_email.html')
        user_account.save()
        book.save()  
        return redirect('profile')
    

class UserBookListView(LoginRequiredMixin,ListView):
    model = models.Book
    template_name = 'Books/profile.html'
    context_object_name = 'books'

    def get_queryset(self):
        return super().get_queryset().filter(account__user=self.request.user)
