class Student:
    def __init__(self, name, surname, gender):
        "Создаём нашего студента"
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.average_rating = [] # Добавлено для упрощения сравнения объектов между собой

    def rate_lecture(self, lecturer, course, score):
        "Студен имеет возможность выставлять оценки лекторам"
        if (score >=0 or score <=10) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course].append(score)
            else:
                lecturer.grades.setdefault(course, [score])
        else:
            return "Ошибка! Отказано в действии"

    def __str__(self):
        "Переопределяю метод __str__ как попросили"
        return (
                f" Студент\n"
                f" Имя: {self.name}\n"
                f" Фамилия: {self.surname}\n"
                f" Средняя оценка за домашние задания: {self.average_rating}\n"
                f" Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n"
                f" Завершенные курсы: {"Отсутствуют" if len(self.finished_courses) == 0 else ", ".join(self.finished_courses)}"
                )

    def __eq__(self, other):
        return "Средние оценки этих студентов равны" if self.average_rating == other.average_rating else "Средние оценки этих студентов не равны"

    def __ne__(self, other):
        return "Верно! Средние оценки этих студентов не равны" if self.average_rating != other.average_rating else "Неправда! Средние оценки этих студентов равны"

    def __lt__(self, other):
        return f"Средняя оценка {self.name} составляет {self.average_rating} это меньше чем у {other.name}" if self.average_rating < other.average_rating else f"Средняя оценка {other.name} составляет {other.average_rating} это меньше чем у {self.name}"

    def __gt__(self, other):
        return f"Средняя оценка {self.name} составляет {self.average_rating} это больше чем у {other.name}" if self.average_rating > other.average_rating else f"Средняя оценка {other.name} составляет {other.average_rating} это больше чем у {self.name}"

class Mentor:
    "Родоначальник для последующих классов"
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        "Позволяет выставлять хорошие оценки)"
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

class Lecturer(Mentor):
    def __init__(self, name, surname):
        "Создание нашего лектора"
        super().__init__(name, surname)
        self.grades = {}
        self.average_rating = []

    def rate_hw(self):
        "Метод переопределен, чтобы ограничить лекторам доступ к выставлению оценок"
        return "Отказано в доступе"

    def __str__(self):
        "Опять переопределяю спец.метод __str__ как попросили"
        return (
                f" Лектор\n"
                f" Имя: {self.name}\n"
                f" Фамилия: {self.surname}\n"
                f" Средняя оценка за лекции: {self.average_rating}"
                )

    def __eq__(self, other):
        return "Средние оценки этих лекторов равны" if self.average_rating == other.average_rating else "Средние оценки этих лекторов не равны"

    def __ne__(self, other):
        return "Правильно! Средние оценки этих лекторов не равны" if self.average_rating != other.average_rating else "Неправда! Средние оценки этих лекторов равны"

    def __lt__(self, other):
        return f"У {self.name} оценка составляет {self.average_rating} это меньше чем у {other.name}" if self.average_rating < other.average_rating else f"У {other.name} оценка составляет {other.average_rating} это меньше чем у {self.name}"

    def __gt__(self, other):
        return f"У {self.name} оценка составляет {self.average_rating} это больше чем у {other.name}" if self.average_rating > other.average_rating else f"У {other.name} оценка составляет {other.average_rating} это больше чем у {self.name}"


class Reviewer(Mentor):
    "Для выставления оценок достаточно вызвать метод rate_hw с нужными аргументами в остальном это не документация класса"
    def __init__(self, name, surname):
        super().__init__(name, surname)
    def __str__(self):
        return (
                f" Проверяющий\n"
                f" Имя: {self.name}\n"
                f" Фамилия: {self.surname}"
                )

# Функция для подсчета средней оценки
def whole_score(ranked, course):
    """ Для удобного подсчёта средней оценки по курсу
    В самом классе мне не удалось её реализовать нормально
    Важно что подсчет средней оценки возможен только после её проставления """
    if course in ranked.grades:
        ranked.average_rating = round(sum(ranked.grades[course]) / len(ranked.grades[course]), 1)

# Функция для подсчета средней оценки у студентов по определенному курсу
def course_total_grade_std(list_students, course):
    "Подсчет средней оценки за курс у студентов"
    result = []
    for pupil in list_students:
        if course in pupil.courses_in_progress:
            result.extend(pupil.grades[course])
        continue
    return sum(result) / len(result)

# Функция для подсчета средней оценки у лекторов по определенному курсу
def course_total_grade_lct(list_lectors, course):
    """ Подсчет средней оценки за курс у лекторов
    Важно! Нужный курс должен быть в списке лекторов """
    result = []
    for comrade in list_lectors:
        if course in comrade.courses_attached:
            result.extend(comrade.grades[course])
    return sum(result) / len(result)

# Первая тройка объявляется
lecturer_1 = Lecturer('Тимур', 'Анвартдинов')
reviewer_1 = Reviewer('Говард', 'Флац')
student_1 = Student('Марья', 'Богородова', 'Ж')

# Вторая тройка объявляется
lecturer_2 = Lecturer("Василий", "Теркин",)
reviewer_2 = Reviewer("Измаил", "Лаиходжа", )
student_2 = Student("Константин", "Щегалев", "М")

# Проверка наследования
print(isinstance(lecturer_1, Mentor)) # True
print(isinstance(reviewer_1, Mentor)) # True
print(lecturer_1.courses_attached)    # []
print(reviewer_1.courses_attached)    # []

# Назначение студентам активных курсов
student_1.courses_in_progress += ['Python', 'Java']
lecturer_1.courses_attached += ['Python', 'C++']
reviewer_1.courses_attached += ['Python', 'C++']

student_2.courses_in_progress += ['Python', "Git"]
lecturer_2.courses_attached += ['Python']
reviewer_2.courses_attached += ['Python']

# Назначение завершенных курсов
student_1.finished_courses += ["QA - тестирование"]
student_2.finished_courses += ["Введение в программирование"]

# Проверка оценивания у студентов
print("\n", student_1.rate_lecture(lecturer_1, 'Python', 7))  # None
print(student_1.rate_lecture(lecturer_1, 'Java', 8))  # Ошибка
print(student_1.rate_lecture(lecturer_1, 'С++', 8))  # Ошибка
# print(student_1.rate_lecture(reviewer_1, 'Python', 6))  # Ошибка без обработки

print(lecturer_1.grades)  # {'Python': [7]}

# Студенты оценивают
student_1.rate_lecture(lecturer_1, 'Python', 7.4)
student_1.rate_lecture(lecturer_2, 'Python', 8.8)
student_2.rate_lecture(lecturer_1, 'Python', 9.9)
student_2.rate_lecture(lecturer_2, 'Python', 6.9)

# Проверяющие оценивают
reviewer_1.rate_hw(student_1, "Python", 5.4)
reviewer_1.rate_hw(student_1, "Python", 8.2)
reviewer_2.rate_hw(student_2, "Python", 3.7)
reviewer_2.rate_hw(student_2, "Python", 9.9)

# Подсчет средней оценки - только после их выставления
for i in [student_1, student_2, lecturer_1, lecturer_2]:
    whole_score(i, "Python")

# Работоспособность переопределенного спец.метода __str__
print("\n", reviewer_1, lecturer_1, student_1, sep="\n\n")
print("\n", reviewer_2, lecturer_2, student_2, sep="\n\n")

# Проверка работы перегруженных операторов сравнения
print(
      "\n",
      student_1 == student_2,
      student_1 != student_2,
      student_1 < student_2,
      student_1 > student_2,
      sep="\n"
      )

print(
      "\n",
      lecturer_1 == lecturer_2,
      lecturer_1 != lecturer_2,
      lecturer_1 < lecturer_2,
      lecturer_1 > lecturer_2,
      sep="\n"
      )

# Дополнительно для определения средних оценок
student_3 = Student("Борис", "Большегубов", "М")
student_4 = Student("Фаина", "Скороходкина", "Ж")
student_5 = Student("Арамис", "Черный", "М")

student_3.courses_in_progress += ['Python']
student_4.courses_in_progress += ['Python']
student_5.courses_in_progress += ['Python']

reviewer_1.rate_hw(student_3, "Python", 1.0)
reviewer_1.rate_hw(student_4, "Python", 7.2)
reviewer_2.rate_hw(student_5, "Python", 2.8)

for i in [student_3, student_4, student_5]:
    whole_score(i, "Python")

# Использование функций для подсчета средней оценки у студентов и лекторов по определенному заданному курсу
print("\nСредняя оценка студентов по курсу \"Python\" составляет:", round(course_total_grade_std([student_1,student_2, student_3, student_4, student_5], "Python"), 1))
print("Средняя отметка лекторов по курсу \"Python\" составляет:",round(course_total_grade_lct([lecturer_1, lecturer_2], "Python"), 1))

# Для проверки ошибки того что студент не может поставить оценку проверяющему
# print(student_1.rate_lecture(reviewer_1, 'Python', 6))

#                                   Ну как оно? Уж больно страшно ждать ответа
#                          В Git я ничего и не сохранял :( не подумал об этом и не привык ещё
