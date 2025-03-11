import argparse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Student, Teacher, Group, Subject, Grade


class CRUDBase:
    model = None

    @classmethod
    def create(cls, **kwargs):
        '''
        Base function for create DB records
        '''
        session = SessionLocal()
        instance = cls.model(**kwargs)
        session.add(instance)
        session.commit()
        print(f"{cls.model.__name__} created with ID {instance.id}")
        session.close()

    @classmethod
    def list(cls):
        '''
        Base function for reading DB records
        '''
        session = SessionLocal()
        instances = session.query(cls.model).all()
        print(f"List of {cls.model.__name__}s")
        for instance in instances:
            row = instance.__dict__
            del row["_sa_instance_state"]
            print(row)
        session.close()

    @classmethod
    def update(cls, record_id, **kwargs):
        session = SessionLocal()
        instance = session.query(cls.model).filter(cls.model.id == record_id).first()
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            session.commit()
            print(f"{cls.model.__name__} ID {record_id} updated")
        else:
            print(f"{cls.model.__name__} with ID {record_id} not found")
        session.close()

    @classmethod
    def remove(cls, record_id):
        session = SessionLocal()
        instance = session.query(cls.model).filter(cls.model.id == record_id).first()
        if instance:
            session.delete(instance)
            session.commit()
            print(f"{cls.model.__name__} ID {record_id} removed")
        else:
            print(f"{cls.model.__name__} with ID {record_id} not found")
        session.close()


class CRUDTeacher(CRUDBase):
    model = Teacher


class CRUDStudent(CRUDBase):
    model = Student


class CRUDGroup(CRUDBase):
    model = Group


class CRUDSubject(CRUDBase):
    model = Subject


class CRUDGrade(CRUDBase):
    model = Grade


crud_classes = {
    "Teacher": CRUDTeacher,
    "Student": CRUDStudent,
    "Group": CRUDGroup,
    "Subject": CRUDSubject,
    "Grade": CRUDGrade,
}


def main():
    parser = argparse.ArgumentParser(description="CLI tool for database management")
    parser.add_argument(
        "-a",
        "--action",
        choices=["create", "list", "update", "remove"],
        required=True,
        help="CRUD action",
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=crud_classes.keys(),
        required=True,
        help="Model to apply action on",
    )
    parser.add_argument("--id", type=int, help="ID of the record")
    parser.add_argument("--name", type=str, help="Name of the entity")
    parser.add_argument("--group_id", type=int, help="Group ID (for Student)")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID (for Subject)")
    parser.add_argument("--subject_id", type=int, help="Subject ID (for Grade)")
    parser.add_argument("--student_id", type=int, help="Student ID (for Grade)")
    parser.add_argument("--grade", type=float, help="Grade value (for Grade)")

    args = parser.parse_args()

    crud_class = crud_classes[args.model]

    kwargs = {}
    if args.name:
        kwargs["name"] = args.name
    if args.model == "Student" and args.group_id:
        kwargs["group_id"] = args.group_id
    if args.model == "Subject" and args.teacher_id:
        kwargs["teacher_id"] = args.teacher_id
    if args.model == "Grade":
        if args.subject_id:
            kwargs["subject_id"] = args.subject_id
        if args.student_id:
            kwargs["student_id"] = args.student_id
        if args.grade is not None:
            kwargs["grade"] = args.grade

    if args.action == "create":
        crud_class.create(**kwargs)
    elif args.action == "list":
        crud_class.list()
    elif args.action == "update" and args.id:
        crud_class.update(args.id, **kwargs)
    elif args.action == "remove" and args.id:
        crud_class.remove(args.id)
    else:
        print("Invalid arguments.")


if __name__ == "__main__":
    main()
