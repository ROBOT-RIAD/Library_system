from django.urls import path
from .views import BookDetail,BorrowBookView,UserBookListView,ReturnBookView

urlpatterns = [
    path('detail/<int:id>',BookDetail.as_view(),name='detaile'),
    path('Borrow/<int:id>',BorrowBookView.as_view(),name='Borrow'),
    path('User_book/',UserBookListView.as_view(),name='profile'),
    path('return/<int:id>',ReturnBookView.as_view(),name='return'),
]