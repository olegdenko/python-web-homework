
from abc import ABC, abstractmethod
from contact_book import AddressBook
from note_book import NoteBook

class AbstractView(ABC):

   @abstractmethod
   def show_contact_book(self, contact_book: AddressBook):
      pass

   @abstractmethod
   def show_note_book(self, note_book: NoteBook):
      pass

   @abstractmethod
   def show_help(self):
      pass

