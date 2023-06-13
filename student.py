from utils import cls, input_yes_no, create_if_not_exists, list_dir, path_exists, field_name_from
from time import sleep
from grades import Grades

def student_prompt_filter(pair):
    k, _ = pair
    return k not in ["student_id", "grades", "All", "Student_ids", "Needed_space_for_property_names"]


class Student:

    PRINTING_FORMAT = "{{k:<{f}}}: {{v}}"

    Needed_space_for_property_names: int = 0
    Student_ids: list = []
    All: dict = {}

    student_id: str
    first_name: str
    last_name: str
    age: int
    national_id: str
    education_started_at: int
    grades: Grades

    def __init__(self, info: dict, grades: Grades, save_to_file: bool = True):
        for k, v in info.items():
            setattr(self, k, v)
        self.grades = grades
        if save_to_file:
            self.student_id = f"{self.education_started_at}{len(Student.Student_ids) + 1:07d}"
            self.save()
            cls()
            print(f"{self.first_name} {self.last_name} is saved!")
        Student.All[self.student_id] = self
        
    def save(self):
        path = f"data/{self.student_id}.txt"
        create_if_not_exists(path)
        file = open(path, "w+")
        printing_format = Student.PRINTING_FORMAT.format(f=Student.Needed_space_for_property_names)
        for k in filter(lambda k: k != k.capitalize() and k != "grades", self.__annotations__):
            file.write(printing_format.format(k=k, v=getattr(self, k)) + "\n")
        file.writelines(["\n", *self.grades.saving_formatted()])
        file.close()
        Student.Student_ids.append(self.student_id)


    def Load_student_ids():
        files = list_dir("data/")
        for file in files:
            Student.Load_from_file(f"data/{file}")
            Student.Student_ids.append(file.removesuffix(".txt"))

    def Load(student_id: str):
        path = f"data/{student_id}.txt"
        if path_exists(path):
            file = open(path, "r")
            print("Student information")
            for line in file.readlines():
                print(f" {line}", end="")
                if line == "\n":
                    print("Grades:")
            file.close()
            print()
        else:
            print(f"student with id {student_id} is missing!")

    def Load_from_file(path: str):
        if path_exists(path):
            info: dict
            grades: dict
            dictionary: dict = {}
            file = open(path, "r")
            for line in file.readlines():
                if line != "\n":
                    k, v = [i.strip("\n ") for i in line.split(":")]
                    dictionary[k] = v
                else:
                    info = dictionary.copy()
                    dictionary = {}
            grades = dictionary.copy()
            Student(info, Grades(grades), save_to_file=False)



    def Search(student_id: str):
        if student_id in Student.Student_ids:
            Student.Load(student_id)
        else:
            print(f"student with id {student_id} not found!")      
    
    def Prompt():
        info: dict = {}
        for k, v in filter(student_prompt_filter, Student.__annotations__.items()):
            field_name = field_name_from(k)
            i = input(f" {field_name}: ")
            if v is str:
                info[k] = i
            else:
                while True:
                    try:
                        v = int(i)
                        checker = None
                        match k:
                            case "age":
                                checker = lambda age: age >= 15 and age <= 100
                            case "education_started_at":
                                checker = lambda year: year >= 1361
                            case other:
                                raise Exception(f"field {other} is not allowed")
                        while True:
                            if checker(v):
                                info[k] = v
                                break
                            else:
                                print(f"{v} is not acceptable as {field_name}, enter new value")
                                i = input(f" {field_name}: ")
                                v = int(i)
                        break
                    except ValueError:
                        print(f"unacceptable value for {field_name}, please try again")
                        i = input(f" {field_name}: ")
                        continue
        cls()
        print("Filling out grades")
        grades = Grades.Prompt()
        print("Creating new Student with\n")
        print("Information\n")
        print_info_format = " " + Student.PRINTING_FORMAT.format(f=Student.Needed_space_for_property_names)
        for k, v in info.items():
            print(print_info_format.format(k=k, v=v))
        print()
        print("Grades\n")
        for k, v in grades.items():
            print(print_info_format.format(k=k, v=v))
        print()
        if input_yes_no("is the shown info acceptable?"):
            return Student(info, Grades(grades))
        else:
            cls()
            print("starting over...")
            sleep(2)
            cls()
            return Student.Prompt()
        
    def Prepare():
        for k, _ in filter(student_prompt_filter, Student.__annotations__.items()):
            if Student.Needed_space_for_property_names < len(k):
                Student.Needed_space_for_property_names = len(k)
        Student.Load_student_ids()
    