import csv
import os.path

DEFAULT_FILENAME = 'default.csv'


def get_input(prompt: str, error_message: str) -> int:
    """
    Запрос ввода параметра
    :param prompt: Подсказка запроса
    :param error_message: Текст ошибочного ввода
    :return: Введёный параметр
    """
    variants = ['1', '2', '3', '4']
    while True:
        parameter = input(prompt)
        if parameter in variants:
            return int(parameter)
        print(error_message)


class PhoneBook:
    """
    Класс для работы с телефонным справочником.
    """
    FIELDNAMES: list[str] = ['Фамилия Имя Отчество', 'Компания', 'Рабочий телефон', 'Личный телефон']

    def __init__(self, filename):
        """
        :param filename: Имя файла справочника
        """
        self.filename: str = filename
        self.data: list[list[str]] = self.read()

    def read(self):
        """
        Чтение справочника из файла в формате csv
        :return: Загруженный справочник
        """
        with open(self.filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            data: list[list[str]] = []
            for row in reader:
                data.append(row)
        return data

    def save(self):
        """
        Сохранение справочника в файл в формате csv
        """
        with open(self.filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(self.data)

    def list_phonebook(self):
        """
        Вывод справочника постранично
        """
        page_size: int = 20
        i: int = 1
        print('{:<5} {:<40}  {:<40}  {:<20} {:<20}'.format('№', *self.FIELDNAMES))
        for row in self.data:
            print('{:<5} {:<40}  {:<40}  {:<20} {:<20}'.format(i, *row))

            if i % page_size == 0:
                command = input('Для вывода следующих записей нажмите Enter, для выхода - x: \n')
                if command == 'x':
                    break
            i += 1

    def add_new_record(self):
        """
        Добавление записи в конец справочника и сохранение в файл
        """
        name: str = input('Введите ФИО: ')
        company: str = input('Введите название компании: ')
        work_phone: str = input('Введите рабочий телефон: ')
        personal_phone: str = input('Введите личный телефон: ')
        self.data.append([name, company, work_phone, personal_phone])
        self.save()
        print('Запись добавлена')

    def search(self):
        """
        Поиск по справочнику
        """
        search_prompt: str = '''Введите поле для поиска: 
                1 - для поиска по ФИО
                2 - для поиска по названию компании
                3 - для поиска рабочего телефона
                4 - для поиска личного телефона
                '''
        search_error_message: str = 'Неверный параметр поиска!'
        search_field: int = get_input(search_prompt, search_error_message)
        query: str = input('Введите значение для поиска: ').strip().lower()

        search_field -= 1
        records = []
        for i in range(len(self.data)):
            if query in self.data[i][search_field].lower():
                records.append([i + 1, *self.data[i]])
        print(f'Найдено записей: {len(records)}')
        if len(records):
            print('{:<5} {:<40}  {:<40}  {:<20} {:<20}'.format('№', *self.FIELDNAMES))
            for record in records:
                print('{:<5} {:<40}  {:<40}  {:<20} {:<20}'.format(*record))

    def edit_record(self):
        """
        Редактирования справочника
        """
        edit_prompt: str = '''Выберите поле для редактирования: 
                        1 - ФИО
                        2 - Название компании
                        3 - Рабочий телефон
                        4 - Личный телефон
                        '''
        edit_error_message: str = 'Неверный выбор поля для редактирования!'
        while True:
            query: str = input('Введите номер записи для редактирования: ')
            if not query.isdecimal():
                print('Неверный ввод!')
                continue
            row_number: int = int(query) - 1
            if row_number > len(self.data):
                print('Такой записи не существует')
                continue
            break
        print('{:<5} {:<40}  {:<40}  {:<20} {:<20}'.format('№', *self.FIELDNAMES))
        print('{:<5} {:<40}  {:<40}  {:<20} {:<20}'.format(row_number + 1, *self.data[row_number]))
        edit_field = get_input(edit_prompt, edit_error_message)
        edit_field -= 1
        query = input('Введите новое значение: ').strip().lower()

        self.data[row_number][edit_field] = query
        self.save()
        print('Запись обновлена')


def main():
    print('Интерфейс для работы с телефонным справочником')
    filename: str = input(
        'Введите имя файла справочника (Enter для файла по умолчанию - default.csv)') or DEFAULT_FILENAME
    if not os.path.isfile(filename):
        print('Неверное имя файла')
        return
    phone_book: PhoneBook = PhoneBook(filename)
    while True:
        command: str = input('''Введите команду для работы:
                    \u0332list - для постраничного выводы на экран
                    \u0332edit - для редактирования записи
                    \u0332add  - для добавления новой записи
                    \u0332search - для поиска по записям
                    e\033[4mx\033[0mit - для выхода
                    ''')

        match command:
            case 'list' | 'l':
                phone_book.list_phonebook()
            case 'add' | 'a':
                phone_book.add_new_record()
            case 'edit' | 'e':
                phone_book.edit_record()
            case 'search' | 's':
                phone_book.search()
            case 'exit' | 'x':
                break


if __name__ == '__main__':
    main()
