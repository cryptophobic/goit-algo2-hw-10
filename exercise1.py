# Визначення класу Teacher
from dataclasses import dataclass, field
from typing import Set, List, Optional

@dataclass
class Teacher:
    first_name: str
    last_name: str
    age: int
    email: str
    can_teach_subjects: Set[str]
    # поля нижче не обов'язкові у вхідних даних, але зручні для результату
    assigned_subjects: List[str] = field(default_factory=list)

    def assign(self, subjects: Set[str]) -> None:
        """
        Призначає викладачу конкретні предмети (підмножину тих, що він уміє).
        """
        # Зберігаємо відсортовано для стабільності виводу
        self.assigned_subjects = sorted(subjects)


def create_schedule(subjects: Set[str], teachers: List[Teacher]) -> Optional[List[Teacher]]:
    """
    Жадібно підбирає мінімальний (наближено) набір викладачів, які покривають усі предмети.
    Крок алгоритму:
      1) Обрати викладача, що покриває найбільше ще НЕпокритих предметів.
      2) При рівності — обрати наймолодшого.
    Якщо покриття всіх предметів неможливе — повертає None.
    """
    uncovered = set(subjects)
    chosen: List[Teacher] = []

    # Створимо робочі копії викладачів без призначень (щоб не мутувати вхідні об’єкти)
    pool = [
        Teacher(t.first_name, t.last_name, t.age, t.email, set(t.can_teach_subjects))
        for t in teachers
    ]

    while uncovered:
        # Пошук найкращого кандидата цього кроку
        best_teacher = None
        best_cover: Set[str] = set()

        for t in pool:
            cover = t.can_teach_subjects & uncovered
            if not cover:
                continue

            if (
                best_teacher is None
                or len(cover) > len(best_cover)
                or (len(cover) == len(best_cover) and t.age < best_teacher.age)
            ):
                best_teacher = t
                best_cover = cover

        # Якщо жоден викладач не покриває жодного з решти предметів — провал
        if best_teacher is None:
            return None

        # Призначаємо і фіксуємо результат кроку
        best_teacher.assign(best_cover)
        chosen.append(best_teacher)
        uncovered -= best_cover

        # Можна видалити вибраного з пулу (необов'язково, але чистіше)
        pool.remove(best_teacher)

    return chosen


if __name__ == '__main__':
    # Множина предметів
    subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}

    # Створення списку викладачів
    teachers = [
        Teacher('Олександр', 'Іваненко', 45, 'o.ivanenko@example.com', {'Математика', 'Фізика'}),
        Teacher('Марія', 'Петренко', 38, 'm.petrenko@example.com', {'Хімія'}),
        Teacher('Сергій', 'Коваленко', 50, 's.kovalenko@example.com', {'Інформатика', 'Математика'}),
        Teacher('Наталія', 'Шевченко', 29, 'n.shevchenko@example.com', {'Біологія', 'Хімія'}),
        Teacher('Дмитро', 'Бондаренко', 35, 'd.bondarenko@example.com', {'Фізика', 'Інформатика'}),
        Teacher('Олена', 'Гриценко', 42, 'o.grytsenko@example.com', {'Біологія'}),
    ]

    # Виклик функції створення розкладу
    schedule = create_schedule(subjects, teachers)

    # Виведення розкладу
    if schedule:
        # Додаткова перевірка на випадок помилки в логіці
        covered = set().union(*[set(t.assigned_subjects) for t in schedule])
        if covered >= subjects:
            print("Розклад занять:")
            for teacher in schedule:
                print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
                print(f"   Викладає предмети: {', '.join(teacher.assigned_subjects)}\n")
        else:
            print("Неможливо покрити всі предмети наявними викладачами.")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")
