
from view import AbstractView
from contact_book import AddressBook, Record, Name, Phone, Email, Birthday, Address, PhoneException, BirthdayException, EmailException
from note_book import NoteBook

from rich import print
from rich import box
from rich.table import Table
from rich.console import Console


class Console_View(AbstractView):

   # вывод в консоль ноут-буки
   def show_note_book(self, note_book: NoteBook):
      for note in note_book.data.values():
         print(f"[{(len(note.tags))}] {note.key}: " + note.value)
      for tag in note_book.tags.values():
         print("[" + str(tag.sz()) + "]#" + tag.value)

   # вывод в консоль контакт-буки
   def show_contact_book(self, contact_book: AddressBook):
      if len(contact_book.data) == 0: 
         print("The database is empty")
      else: 
         table = Table(box=box.DOUBLE)
         table.add_column("Name", justify="center", style="cyan", no_wrap=True)
         table.add_column("Birthday", justify="center", style="yellow", no_wrap=True)
         table.add_column("Phone number", justify="center", style="green", no_wrap=True)
         table.add_column("Email", justify="center", style="red", no_wrap=True)
         table.add_column("Address", justify="center", style="red", no_wrap=True)
         
         console = Console()
         result = [table.add_row(
               str(record.name.value), 
               str(record.birthday.value if record.birthday else "---"), 
               str(', '.join(map(lambda phone: phone.value, record.phones))), 
               str(record.email.value    if record.email    else "---"), 
               str(record.address.value  if record.address  else "---")
                  ) for record in contact_book.data.values()]        
         console.print(table)

   # вывод в консоль хэлпа
   def show_help(self):
         print("""[bold red]cls[/bold red] - очищення екрану від інформації
[bold red]hello[/bold red] - вітання
[bold red]good bye, close, exit[/bold red] - завершення програми
[bold red]load[/bold red] - завантаження інформації про користувачів із файлу
[bold red]save[/bold red] - збереження інформації про користувачів у файл
[bold red]show all[/bold red] - друкування всієї наявної інформації про користувачів
[bold red]show book /N[/bold red]  - друкування інформації посторінково, де [bold red]N[/bold red] - кількість записів на 1 сторінку
[bold red]add[/bold red] - додавання користувача до бази даних. 
      example >> [bold blue]add Mike 02.10.1990 +380504995876[/bold blue]
            >> [bold blue]add Mike None +380504995876[/bold blue]
            >> [bold blue]add Mike None None[/bold blue]
[bold red]phone[/bold red] - повертає перелік телефонів для особи
      example >> [bold blue]phone Mike[/bold blue]
[bold red]add phone[/bold red] - додавання телефону для користувача
      example >> [bold blue]add phone Mike +380504995876[/bold blue]
[bold red]change phone[/bold red] - зміна номеру телефону для користувача
      Формат запису телефону: [bold green]+38ХХХ ХХХ ХХ ХХ[/bold green]
      example >> [bold blue]change phone Mike +380504995876 +380665554433[/bold blue]
[bold red]del phone[/bold red] - видаляє телефон для особи. Дозволяється видаляти одразу декілька телефонів.
      example >> [bold blue]del phone Mike +380509998877, +380732225566[/bold blue]
[bold red]birthday[/bold red] - повертає кількість днів до Дня народження
      example >> [bold blue]birthday Mike[/bold blue]
[bold red]change birthday[/bold red] - змінює/додає Дату народження для особи
      example >> [bold blue]change birthday Mike 02.03.1990[/bold blue]
[bold red]search[/bold red] - виконує пошук інформації по довідковій книзі
      example >> [bold blue]search Mike[/bold blue]
[bold red]note add[/bold red] - додає нотатку з тегом у записник нотаток
      example >> [bold blue]note add My first note Note[/bold blue]
[bold red]note del[/bold red] - видаляє нотатку за ключем із записника нотаток
      example >> [bold blue]note del 1691245959.0[/bold blue]
[bold red]note change[/bold red] - змінює нотатку з тегом за ключем у записнику нотаток
      example >> [bold blue]note change 1691245959.0 My first note Note[/bold blue]
[bold red]note find[/bold red] - здійснює пошук за фрагментом у записнику нотаток
      example >> [bold blue]note find name[/bold blue]
[bold red]note show[/bold red] - здійснює посторінковий вивід всіх нотаток
      example >> [bold blue]note show /10[/bold blue]
[bold red]note sort[/bold red] - здійснює сортування записів нотаток за тегами
      example >> [bold blue]note sort /10[/bold blue]      
[bold red]sort[/bold red] - виконує сортування файлів в указаній папці
      example >> [bold blue]sort folder_name[/bold blue]
""")

