from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DATETIME, DATE
from datetime import datetime, timedelta, date

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(DATE, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

week = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}



while True:
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    command = input()
    if command == "1":
        today = date.today()
        print("\nToday", today.day, today.strftime('%b'))
        rows = session.query(Table).all()
        if rows != []:
            for row in rows:
                if row.deadline == today:
                    print(str(row.id) + ". " + row.task)
            print()
        else:
            print("Nothing to do!\n")

    elif command == "2":
        today = date.today()
        print()
        for i in range(7):
            next = today + timedelta(i)
            rows = session.query(Table).filter(Table.deadline == next).all()
            print(week[next.weekday()], next.strftime('%b'), next.day)
            if rows != []:
                for row in rows:
                    print(str(row.id) + ". " + row.task)
                print()
            else:
                print("Nothing to do!\n")

    elif command == "3":
        rows = session.query(Table).all()
        print()
        if rows != []:
            for row in rows:
                print(str(row.id) + ". " + row.task, row.deadline)
            print()
        else:
            print("Nothing to do!\n")

    elif command == "4":
        print("\nMissed Tasks:")
        rows = session.query(Table).filter(Table.deadline < date.today()).all()
        if rows != []:
            for row in rows:
                end = row.deadline
                print(str(row.id) + ". " + row.task + ".", end.day, end.strftime('%b'))
            print()
        else:
            print("Nothing is missed!\n")


    elif command == "5":
        print("\nEnter task")
        task = input()
        print("Enter Deadline")
        end = input()
        date = datetime.strptime(end, "%Y-%m-%d").date()
        try:
            new_row = Table(task=task, deadline=date)
            session.add(new_row)
            session.commit()
            print("The task has been added!\n")
        except Exception as e:
            print(e)

    elif command == "6":
        rows = session.query(Table).all()
        print("\nChose the number of the task you want to delete:")
        if rows != []:
            for row in rows:
                end = row.deadline
                print(str(row.id) + ". " + row.task + ".", end.day, end.strftime('%b'))
        else:
            print("Nothing to do!\n")
        id = int(input())
        try:
            session.query(Table).filter(Table.id == id).delete()
            session.commit()
            print("The task has been deleted!\n")
        except Exception as e:
            print(e)

    elif command == "0":
        print("\nBye!")
        break

    else:
        print("Enter valid option.")