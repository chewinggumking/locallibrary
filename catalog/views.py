from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre
from django.views import generic
import datetime

# Create your views here.




def index(request):
        num_books = Book.objects.all().count()
        num_instances = BookInstance.objects.all().count()
        num_instances_available = BookInstance.objects.filter(status__exact='a').count()
        num_authors = Author.objects.count()
        page_title = "Index of Local Library"
        context = {
            'num_books':num_books, 'num_instances':num_instances,
            'num_instances_available':num_instances_available, 'num_authors':num_authors,
            'page_title':page_title,
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






# def helloWorld(request):
#     message_to_u = """<h1>HELLO WORLD</h1>
#     <p>This is the catalog app landing page</p>
#     """
#     return HttpResponse(message_to_u)
