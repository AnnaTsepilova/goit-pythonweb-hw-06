from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from database import SessionLocal
from models import Student, Grade, Subject, Teacher, Group

def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    session = SessionLocal()
    result = (
        session.query(Student.name, func.avg(Grade.value).label("avg_grade"))
        .select_from(Student)
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .limit(5)
        .all()
    )
    session.close()
    return result

def select_2(subject_id):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    session = SessionLocal()
    result = (
        session.query(Student.name, func.avg(Grade.value).label("avg_grade"))
        .select_from(Student)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .first()
    )
    session.close()
    return result

def select_3(subject_id):
    """Знайти середній бал у групах з певного предмета."""
    session = SessionLocal()
    result = (
        session.query(Group.name, func.avg(Grade.value).label("avg_grade"))
        .select_from(Group)
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )
    session.close()
    return result

def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    session = SessionLocal()
    result = session.query(func.avg(Grade.value)).scalar()
    session.close()
    return result

def select_5(teacher_id):
    """Знайти які курси читає певний викладач."""
    session = SessionLocal()
    result = (
        session.query(Subject.name)
        .filter(Subject.teacher_id == teacher_id)
        .all()
    )
    session.close()
    return result

def select_6(group_id):
    """Знайти список студентів у певній групі."""
    session = SessionLocal()
    result = (
        session.query(Student.name)
        .filter(Student.group_id == group_id)
        .all()
    )
    session.close()
    return result

def select_7(group_id, subject_id):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    session = SessionLocal()
    result = (
        session.query(Student.name, Grade.value)
        .select_from(Student)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    session.close()
    return result

def select_8(teacher_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    session = SessionLocal()
    result = (
        session.query(func.avg(Grade.value))
        .select_from(Grade)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )
    session.close()
    return result

def select_9(student_id):
    """Знайти список курсів, які відвідує певний студент."""
    session = SessionLocal()
    result = (
        session.query(Subject.name)
        .select_from(Subject)
        .join(Grade, Subject.id == Grade.subject_id)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )
    session.close()
    return result

def select_10(student_id, teacher_id):
    """Список курсів, які певному студенту читає певний викладач."""
    session = SessionLocal()
    result = (
        session.query(Subject.name)
        .select_from(Subject)
        .join(Grade, Subject.id == Grade.subject_id)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )
    session.close()
    return result

def select_11(teacher_id, student_id):
    """Середній бал, який певний викладач ставить певному студентові."""
    session = SessionLocal()
    result = (
        session.query(func.avg(Grade.value))
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id, Grade.student_id == student_id)
        .scalar()
    )
    session.close()
    return result

def select_12(group_id, subject_id):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""
    session = SessionLocal()
    subquery = (
        session.query(Grade.student_id, func.max(Grade.date_received).label("last_date"))
        .join(Student)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .group_by(Grade.student_id)
        .subquery()
    )
    result = (
        session.query(Student.name, Grade.value)
        .join(Grade)
        .join(subquery, (Grade.student_id == subquery.c.student_id) & (Grade.date_received == subquery.c.last_date))
        .all()
    )
    session.close()
    return result


def run_all_queries():
    """Запускає всі запити один за одним і виводить результати в консоль."""
    queries = [
        ("5 студентів із найбільшим середнім балом", select_1, []),
        ("Студент із найвищим середнім балом з певного предмета", select_2, [1]),
        ("Середній бал у групах з певного предмета", select_3, [1]),
        ("Середній бал на потоці", select_4, []),
        ("Курси, які читає певний викладач", select_5, [1]),
        ("Список студентів у певній групі", select_6, [1]),
        ("Оцінки студентів у групі з певного предмета", select_7, [1, 2]),
        ("Середній бал, який ставить певний викладач", select_8, [4]),
        ("Список курсів, які відвідує певний студент", select_9, [20]),
        ("Курси, які певному студенту читає певний викладач", select_10, [20, 2]),

        ("Середній бал, який певний викладач ставить певному студентові", select_11, [2, 5]),
        ("Оцінки студентів у певній групі з певного предмета на останньому занятті", select_12, [3, 5]),
    ]

    for description, func_select, args in queries:
        print(f"\n{description}:")
        result = func_select(*args)
        print(result if result else "Немає даних")

if __name__ == "__main__":
    run_all_queries()
