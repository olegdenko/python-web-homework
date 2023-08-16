from collections import UserDict
from datetime import datetime
import pickle
from contact_book import Field

class Tag(Field):

    def __init__(self, value):        
        super().__init__(value)
        self.value = value

        # список ключей тех ноутов, к которым тэг будет привязан
        self.notes = set()
        
    def __str__(self):
        result = str(self.value)
        if len(self.notes): result += "\nnote-keys: " + ", ".join([key for key in self.notes])
        return result
    
    def __repr__(self):
        return str(self.value)

    def sz(self):
        return len(self.notes)

    # добавляем ключ-ссылку на ноут в список ключей, тем самым делаем привязку к ноуту
    def link(self, note_key: str):
        self.notes.add(note_key)

    # удаляем ключ-ссылку на ноут, тем самым удаляем связь к ноуту (отвязываем)
    def unlink(self, note_key: str):
        self.notes.remove(note_key)

class Note(Field):

    def __init__(self, key: str, value: str):
        super().__init__(value)
        self.value = value
        self.key = key

        # список тэгов, к которым будет привязан 
        self.tags = set()

    def __str__(self):
        result = f"{str(self.value)}\nkey: {str(self.key)}"
        if len(self.tags): result += "\n" + " ".join(["#" + tag for tag in self.tags])
        return result

    # добавляем ключ-ссылку на тэг в список ключей, тем самым делаем привязку к тэгу
    def link(self, tag_key: str):
        self.tags.add(tag_key)
    
    # удаляем ключ-ссылку на тэг, тем самым удаляем связь к тэгу (отвязываем)
    def unlink(self, tag_key: str):
        self.tags.remove(tag_key)


class NoteBook(UserDict):

    def __init__(self):
        super().__init__()
        self.tags = dict() # dict(tag=str, Tag)
        self.max = 0

    def change_note(self, note_key: str, value: str):
        if note_key in self.data.keys():
            note = self.data[note_key]
            note.value = value
            return f"change_note: successfully note.key={note_key}"
        else: return f"change_note: wrong note.key={note_key}"


    def add_tags(self, note_key:str, tags_list:list):
        # проверяем по ключу есть ли такой ноут
        if note_key in self.data.keys():
            note = self.data[note_key]

            for tag_key in tags_list:
                # проверяем есть ли такой ключ в списке уже существующих
                if tag_key not in self.tags.keys():
                    # добавляем новый тэг по строке-ключу
                    self.tags[tag_key] = Tag(tag_key)
                tag = self.tags[tag_key]
                # привязываем к ноуту тэг
                note.link(tag_key)
                # привязываем к тэгу ноут
                tag.link(note_key)

            return f"add_tags: successfully attached tags:{len(tags_list)}"
        else: return f"add_tags: wrong note.key={note_key}"

    # удаляем у ноута заданный список тэгов
    def del_tags(self, note_key: str, tags_list: list):
        # проверяем по ключу есть ли такой ноут
        if note_key in self.data.keys():
            note = self.data[note_key]

            # если список тэгов пуст - удалим все тэги ноута
            if tags_list == None: tags_list = list(note.tags)

            for tag_key in tags_list:
                # отвязываем от ноута тэг по ключу тэга
                note.unlink(tag_key)
                tag = self.tags[tag_key]
                # отвязываем от тэга ноут
                tag.unlink(note_key)
                # если тэг после отвязки не привязан не к одному ноуту - удаляем тэг
                if tag.sz() == 0:
                    tag = self.tags.pop(tag_key)

            return f"del_tags: successfully detached tags:{len(tags_list)}"
        else: return f"del_tags: wrong note.key={note_key}"


    def create_note(self, value: str):
        # генерируем уникальный ключ=счётчик
        self.max += 1
        key = str(self.max)
        note = Note(key, value)
        self.data[key] = note
        return f"Added new note, key={key}"
    
    def del_note(self, note_key: str):
        if note_key in self.data.keys():
            note = self.data.pop(note_key)
            # обрабатываем каждый тэг удаленного ноута
            for tag_key in note.tags:
                tag = self.tags[tag_key]
                # отвязываем тэг от удаленного ноута по ключу ноута
                tag.unlink(note_key)
                # если тэг после отвязки не привязан не к одному ноуту - удаляем тэг
                if tag.sz() == 0:
                    self.tags.pop(tag_key)
            return f"Deleted Note.key: {note.key}\nNote: {note.value}\nTags: {len(note.tags)}"
        return f"Wrong key={note_key} to delete Note"

    # получаем у тэга список ноутов в развёрнутом текстовом формате
    def get_tag_notes(self, tag_key: str) -> list:
        if tag_key in self.tags.keys():
            tag = self.tags[tag_key]
            notes_list = []
            for note_key in tag.notes:
                note = self.data[note_key]
                notes_list.append(f"Note[{note.key}]:{note.value}")
            return notes_list
        return []

    # ищем текст в тэгах, и возвращаем список ноутов по найденным тэгам
    def search_notes_by_text_tags(self, text: str):
        tag_list = []

        # находим все тэги, содержащие в себе искомый текст
        if len(text) > 0:
            for tag in self.tags.values():
                if tag.value.find(text) >= 0:
                    tag_list.append(tag.value)
        # сортируем найденные тэги по их тексту
        tag_list = sorted(tag_list)
        note_list = []

        # формируем по найденным тэгам список ключей, привязанных к этим ноутам
        # исспользуем множество set(int), чтобы исключить дубли ключей, 
        # потому как к разным найденным тэгам может быть привязан один и тот-же ноут
        note_ids = set()

        # проходим по списку в том порядке, в котором они были отсортированы
        for tag_str in tag_list:
            # получаем тэг по ключу
            tag = self.tags[tag_str]
            for id in tag.notes:
                if id not in note_ids:
                    # заполняем финальный список ноутов
                    note_list.append(self.data[id])
            # заполняем ноутами чтобы устранять дубликаты
            note_ids.update(tag.notes)

        print(f"search_notes_by_text:\"{text}\" in tags={len(tag_list)}, for notes={len(note_list)}")
        return note_list
        
    def iterator(self, group_size=15):
        notes = list(self.data.values())
        self.current_index = 0

        while self.current_index < len(notes):
            group_items = notes[self.current_index:self.current_index + group_size]
            group = [rec for rec in group_items]
            self.current_index += group_size
            yield group

    def find_notes(self, fragment:str):
        result = []
        for note in self.values():
            if note.value.lower().find(fragment.lower()) >= 0:
                result.append(note.key)
        return result

    def save_to_file(self, path):
        with open(path, 'wb') as f_out:
            pickle.dump([self.data, self.tags, self.max], f_out)
            #print(f"Saved notes:{len(self.data)} tags:{len(self.tags)}")
        return ""

    def load_file(self, path):
        if path.exists():
            with open(path, 'rb') as f_in:
                obj = pickle.load(f_in)
                if len(obj) != 3: raise ValueError("Wrong object loaded")
                self.data = obj[0]
                self.tags = obj[1]
                self.max  = obj[2]
            #print(f"Load notes:{len(self.data)} tags:{len(self.tags)}, max={str(self.max)}")
        return ""
