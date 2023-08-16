# 
from collections import UserDict
from collections.abc import Iterator
import re
import pickle
from datetime import datetime
from datetime import timedelta


class PhoneException(Exception):
   """Phone wrong number exception"""

class BirthdayException(Exception):
   """Birthday wrong format exception"""

class EmailException(Exception):
   """Email wrong format exception"""


class Field():
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self) -> str:
        if self.__value:
            return self.value
        return ""

    def __repr__(self) -> str:
        return str(self.value)
    
# клас Ім'я
class Name(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value


# клас Телефон
class Phone(Field): 
    @property
    def value(self):
        return self.__value 
    
    @value.setter
    def value(self, value):
        if value == None: 
            self.__value = value
            raise PhoneException("Incorrect phone format: None")
        else:
            correct_phone = ""
            for i in value: 
                if i in "+0123456789": correct_phone += i

            if len(correct_phone) == 13: self.__value = correct_phone # "+380123456789"
            elif len(correct_phone) == 12: self.__value = "+" + correct_phone # "380123456789"
            elif len(correct_phone) == 10: self.__value = "+38" + correct_phone # "0123456789"
            elif len(correct_phone) == 9: self.__value = "+380" + correct_phone # "123456789"
            else: raise PhoneException("Incorrect phone format")

    
# клас День народження        
class Birthday(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        if value == None: 
            self.__value = None
        else:
            pattern = r"^\d{2}(\.|\-|\/)\d{2}\1\d{4}$"  # дозволені дати формату DD.MM.YYYY 
            if re.match(pattern, value):         # альтернатива для крапки: "-" "/"
                self.__value = re.sub("[-/]", ".", value)  # комбінувати символи ЗАБОРОНЕНО DD.MM-YYYY 
            else: 
                self.__value = None
                # устанавливаем None - для валидации 
                #raise BirthdayException("Unauthorized birthday format")

    # возвращает количество дней перед днём рождения
    def days_to_birthday(self) -> int:
        if self.value:
            # возвращает количество дней до следующего дня рождения.
            # если положительное то др еще не наступил, если отрицательное то уже прошел
            current_date = datetime.now().date()

            birthday = datetime.strptime(self.value, "%d.%m.%Y")
            birthday = birthday.replace(year=current_date.year).date()
            quantity_days = (birthday - current_date).days
            return quantity_days
        else: return -1


class Address(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        self.__value = value
  

class Email(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        if value == None: 
            self.__value = None
        else:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, value):
                raise EmailException("Invalid email address!")
            else:
                self.__value = value
      

#========================================================
# Класс Record, который отвечает за логику 
#  - добавления/удаления/редактирования
# необязательных полей и хранения обязательного поля Name
#=========================================================
class Record():
    def __init__(self, name:Name, phones: list, email: Email=None, birthday: Birthday=None, address: Address=None) -> None:
        self.name = name
        self.email = email
        self.birthday = birthday
        self.address = address
        self.phones = []            
        self.phones.extend(phones)


    def edit_birthday(self, birthday: Birthday):
        if birthday.value:
            self.birthday = birthday
            return f"bithday changed to: {birthday.value}"
        # если None то интерпретируем как удаление всего поля
        self.birthday = None
        return "birthday successfully deleted"

    def edit_email(self, email: Email):
        if email.value:
            self.email = email
            return f"email changed to: {email.value}"
        # если None то интерпретируем как удаление всего поля
        self.email = None
        return "email successfully deleted"

    def edit_address(self, address: Address):
        if address.value:
            self.address = address
            return f"address changed to: {address.value}"
        # если None то интерпретируем как удаление всего поля
        self.address = None
        return "address successfully deleted"

    def __str__(self) -> str:
        result = f"{', '.join(map(lambda phone: phone.value, self.phones))}"
        if self.birthday != None:
            result = f"{self.birthday.value}|" + result
        if self.email != None and self.email.value != None:
            result = f"{self.email.value}|" + result
        if self.address != None and self.address.value != None:
            result = f"{self.address.value}|" + result

        return f"{self.name.value}|" + result
      

    # Done - розширюємо існуючий список телефонів особи - Done
    # НОВИМ телефоном або декількома телефонами для особи - Done
    def add_phone(self, list_phones) -> str:
        self.phones.extend(list_phones)
        return f"The phones was/were added - [bold green]success[/bold green]"
    
    # Done - видаляємо телефони із списку телефонів особи - Done!
    def del_phone(self, del_phone: Phone) -> str:
        error = True
        for phone in self.phones:
                if phone.value == del_phone.value: 
                    self.phones.remove(phone) 
                    self.phones.append(Phone("None")) if self.phones == [] else self.phones 
                    error = False  #видалення пройшло з успіхом
                    break
        if error: return f"The error has occurred. You entered an incorrect phone number."
        else: return f"The phone {phone.value} was deleted - [bold green]success[/bold green]"
    
    # Done = редагування запису(телефону) у книзі особи - Done
    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> str:
        index = next((i for i, obj in enumerate(self.phones) if obj.value == old_phone.value), -1)
        self.phones[index]= new_phone
        return f"User set new phone-number - [bold green]success[/bold green]"
    
    
    # перевіряє наявність 1(одного)телефону у списку
    def check_dublicate_phone(self, search_phone: str) ->bool:  
        result = list(map(lambda phone: any(phone.value == search_phone), self.data[self.name.value].phones))
        return True if result else False
    
class AddressBook(UserDict):

    def search(self, text):
        result = []
        for rec in self.values():
            if (rec.name.value.lower().find(text.lower()) >= 0):
                result.append(rec)
                continue
            for phone in rec.phones:
                if phone.value.find(text.lower()) >= 0:
                    result.append(rec)
                    break

        return result

    def get_list_birthday(self, count_day: int):
        lst = []
        if count_day < 0: return lst
        for name, person in self.items():
            if person.birthday != None:
                days = person.birthday.days_to_birthday()

                if (0 <= days) and (days <= count_day):
                    lst.append(f"{name}|{person.birthday.value}")
        return "\n".join(lst)
       
    def add_record(self, record):
        self.data[record.name.value] = record
        return "1 record was successfully added - [bold green]success[/bold green]"

    def rename_record(self, old_name: str, new_name: str):
        rec = self.data.pop(old_name)
        rec.name.value = new_name
        self.data[new_name] = rec
        return f"successfully renamed from:{old_name} to:{new_name}"
    
    # завантаження записів книги із файлу
    def load_database(self, path):
        if path.exists():
            with open(path, "rb") as fr_bin:
                self.data = pickle.load(fr_bin)  # копирование Словника   load_data = pickle.load(fr_bin)
                                                                    # self.data = {**load_data}
            return f"The database has been loaded = {len(self.data)} records"
        return ""
    
    #-----------------------------------------
    # збереження записів книги у файл
    #-------------------------------------------
    def save_database(self, path):
        with open(path, "wb") as f_out:
            pickle.dump(self.data, f_out)
        return f"The database is saved = {len(self.data)} records"    
            
    # генератор посторінкового друку
    def _record_generator(self, N=10):
        records = list(self.data.values())
        total_records = len(records)
        current_index = 0
        
        while current_index < total_records:
            batch = records[current_index: current_index + N]
            current_index += N
            yield batch

