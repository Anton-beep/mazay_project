from Contact import Contact
from Validation import phone_validation, email_validation
from Data import Data


if __name__ == '__main__':
    commands_list = """
    Напишите номер команды
    \t0. Выйти из программы
    \t1. Поиск контакта по  номеру телефону
    \t2. Поиск контакта по почте
    \t3. Поиск контакта по ФИО
    \t4. Поиск контактов с отсутсвующими параметрами (почты/номер телефона)
    \t5. Узнать все контакты
    \t6. Изменить контакт по его id\n
    """

    data = Data(input("Введите название файла базы данных\n"))

    finder_functions = [
        data.number_finder,
        data.email_finder,
        data.name_finder,
        data.find_contacts_with_blank_phone,
        data.find_contacts_with_blank_email,
        data.find_contacts_with_blank_lines
    ]

    while True:
        number_command = int(input(commands_list))
        if number_command == 0:
            break
        elif number_command in [1, 2]:
            if number_command == 1:
                print('Введите номер телефона:\n')
            else:
                print('Введите пользовательскую почту:\n')

            contacts_output = finder_functions[number_command - 1](input())
        elif number_command == 3:
            surname = input('Введите фамилию (оставить пустую строку, если не ищем по этому параметру)\n')
            name = input('Введите имя (оставить пустую строку, если не ищем по этому параметру)\n')
            second_name = input('Введите отчество (оставить пустую строку, если не ищем по этому параметру)\n')

            surname = None if surname == '' else surname
            name = None if name == '' else name
            second_name = None if second_name == '' else second_name

            contacts_output = finder_functions[2](surname, name, second_name)
        elif number_command == 4:
            action = int(input("Выберите цифру из списка:\n"
                               "\t1. Поиск пользователей без номера телефона\n"
                               "\t2. Поиск пользователей без почтового адреса\n"
                               "\t3. Поиск пользователей без телефона или без почты\n"))

            contacts_output = finder_functions[action + 2]()
        elif number_command == 5:
            print("Все пользователи:\n")
            contacts_output = data.get_all_database()
        elif number_command == 6:
            contact_id = int(input("Введите id контакта:\n"))

            if data.get_contact_by_id(contact_id) is None:
                print(f'Контакт с id({contact_id}) не найден: \n')
                continue

            print(f'Контакт сейчас -> {str(data.get_contact_by_id(contact_id))}')

            surname = ''
            while surname == '':
                surname = input('Введите фамилию (не может быть пустой)\n')

            name = input('Введите имя (пустая строка, если нет)\n')
            second_name = input('Введите отчество (пустая строка, если нет)\n')
            email = input('Введите почту (пустая строка, если нет)\n')
            phone_number = input('Введите номер телефона (пустая строка, если нет)\n')

            name = name if name != '' else None
            second_name = second_name if second_name != '' else None
            phone_number = phone_number if phone_number != '' else None
            email = email if email != '' else None

            if phone_number is not None and not phone_validation(phone_number):
                print('Некорректный формат номера телефона')
                continue
            if email is not None and not email_validation(email):
                print('Некорректный формат электронной почты')
                continue

            data.edit_contact_by_id(contact_id, Contact(contact_id, surname,
                                                        name, second_name, email, phone_number))
            continue
        else:
            print('Некорректный номер')
            continue

        try:
            print(*list(map(str, contacts_output)), sep="\n")
        except TypeError:
            print("\nПользователи не найдены")

    input()
