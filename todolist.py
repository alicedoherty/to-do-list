from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

today = datetime.today()


def get_today_tasks():
    print(f'Today {today.day} {today.strftime("%b")}:')
    today_tasks = session.query(Table).filter(Table.deadline == today.date()).all()
    if not today_tasks:
        print('Nothing to do!')
    else:
        for x in range(len(today_tasks)):
            print(f'{x + 1}. {today_tasks[x]}')
    print()


def get_week_tasks():
    for x in range(7):
        day = today + timedelta(days=x)
        print(f'{day.strftime("%A")} {day.day} {day.strftime("%b")}:')
        day_tasks = session.query(Table).filter(Table.deadline == day.date()).all()
        if not day_tasks:
            print('Nothing to do!')
        else:
            for i in range(len(day_tasks)):
                print(f'{i + 1}. {day_tasks[i]}')
        print()


def get_all_tasks():
    print('All tasks:')
    all_tasks = session.query(Table).order_by(Table.deadline).all()
    if not all_tasks:
        print('Nothing to do!')
    for x in range(len(all_tasks)):
        print(f'{x + 1}. {all_tasks[x]}. {all_tasks[x].deadline.day} {all_tasks[x].deadline.strftime("%b")}')
    print()


def get_missed_tasks():
    print('Missed tasks:')
    missed_tasks = session.query(Table).order_by(Table.deadline).filter(Table.deadline < today.date()).all()
    if not missed_tasks:
        print('Nothing is missed!')
    for x in range(len(missed_tasks)):
        print(f'{x + 1}. {missed_tasks[x]}. {missed_tasks[x].deadline.day} {missed_tasks[x].deadline.strftime("%b")}')
    print()


def add_task():
    new_task = input('Enter task:\n')
    new_deadline = input('Enter deadline: (YYYY-MM_DD)\n')
    new_row = Table(task=new_task,
                    deadline=datetime.strptime(new_deadline, '%Y-%m-%d'))
    session.add(new_row)
    session.commit()
    print('The task has been added!')


def delete_task():
    print('Choose the number of the task you want to delete:')
    all_tasks = session.query(Table).order_by(Table.deadline).all()
    if not all_tasks:
        print('Nothing to delete')
    for x in range(len(all_tasks)):
        print(f'{x + 1}. {all_tasks[x]}. {all_tasks[x].deadline.day} {all_tasks[x].deadline.strftime("%b")}')
    task_number = int(input())
    task_to_delete = all_tasks[task_number - 1]
    session.delete(task_to_delete)
    session.commit()
    print('The task has been deleted!')


finished = False

while not finished:
    user_choice = int(input('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
'''))

    if user_choice == 1:
        get_today_tasks()
    elif user_choice == 2:
        get_week_tasks()
    elif user_choice == 3:
        get_all_tasks()
    elif user_choice == 4:
        get_missed_tasks()
    elif user_choice == 5:
        add_task()
    elif user_choice == 6:
        delete_task()
    elif user_choice == 0:
        finished = True
        print('Bye!')
