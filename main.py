from utils import cls
from student import Student

# preparation phase

# load the old data
Student.Prepare()

help_info = """\tinsert: insert new student information
\tsearch: find student using sid
\thelp: show this message
\tquit: exit the program"""

cls()
print("Hello welcome to our community please follow the instructions below")
print(help_info)

while True:
    command = input("command: ")
    match command:
        case "insert":
            Student.Prompt()
        case "search":
            Student.Search(input("Insert student id to search: "))
        case "help":
            print(help_info)
            continue
        case "quit":
            print("goodbye... have a nice day! :D")
            break
        case other:
            print(f"command not found: {command}\n{help_info}")
            continue
    input("press enter to continue")
    cls()
    


