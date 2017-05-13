from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import datetime

# Create your views here.




def index(request):
        num_books = Book.objects.all().count()
        num_instances = BookInstance.objects.all().count()
        num_instances_available = BookInstance.objects.filter(status__exact='a').count()
        num_authors = Author.objects.count()
        page_title = "Index of Local Library"
        num_visits = request.session.get('num_visits', 0)
        request.session['num_visits'] = num_visits + 1
        context = {
            'num_books':num_books, 'num_instances':num_instances,
            'num_instances_available':num_instances_available, 'num_authors':num_authors,
            'page_title':page_title, 'num_visits':num_visits,
            }
        return render(request, 'index.html', context)


class BookListView(generic.ListView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['page_title'] = 'Book List'
        return context

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['page_title'] = 'Author List'
        return context

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_as_returned'
    template_name = 'catalog/loaned_book_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')



# def helloWorld(request):
#     message_to_u = """<h1>HELLO WORLD</h1>
#     <p>This is the catalog app landing page</p>
#     """
#     return HttpResponse(message_to_u)
