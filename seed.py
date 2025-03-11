# seed.py - Заповнення бази випадковими даними
from faker import Faker
from random import randint, choice
from database import SessionLocal
from models import Group, Grade, Teacher, Student, Subject

def seed_database():
    session = SessionLocal()
    fake = Faker()

    groups = [Group(name=fake.word()) for _ in range(3)]
    teachers = [Teacher(name=fake.name()) for _ in range(randint(3, 5))]
    subjects = [Subject(name=fake.word(), teacher=choice(teachers)) for _ in range(randint(5, 8))]
    students = [Student(name=fake.name(), group=choice(groups)) for _ in range(randint(30, 50))]

    session.add_all(groups + teachers + subjects + students)
    session.commit()

    grades = [Grade(student=choice(students), subject=choice(subjects), value=randint(1, 10)) for _ in range(500)]
    session.add_all(grades)
    session.commit()
    session.close()

if __name__ == "__main__":
    seed_database()
