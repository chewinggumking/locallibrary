from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid

# Create your models here.
class Genre(models.Model):
    """
    Genre for the books like Science fiction, Horror etc.
    """
    name = models.CharField(max_length = 200, help_text = "Enter a Book Genre eg. Science Fiction, Poetry etc.")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    #ForeignKey used because book can only have on author but authors can have many books
    summary = models.TextField(max_length=1000, help_text="Enter a brief summary for the book here.")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """
    Model representing a sepcific copy of a book (i.e. that can be borrowed from the library)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular copy of the book")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text="Book Availability")

    @property
    def is_overdue(self):
        if date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_as_returned", "Set book as returned"),)

    def __str__(self):
        return '%s (%s)' % (self.id, self.book.title)


class Author(models.Model):
    "Model representing an Author"
    first_name = models.CharField(max_length=100, help_text="Author's First Name")
    last_name = models.CharField(max_length=100, help_text="Author's Last Name")
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):

        return reverse ('author-detail', args=[str(self.id)])

    def get_books(self):
        book_list = Book.objects.filter(author__id=self.id)
        return (book_list)

    def __str__(self):

        return '%s, %s' %(self.last_name, self.first_name)
