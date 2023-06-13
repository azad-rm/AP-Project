from utils import field_name_from

class Grades:

    mathematics: float
    computer_science: float
    history: float
    physics: float


    def __init__(self, info: dict):
        for k,v in info.items():
            setattr(self, k, v)
    
    def saving_formatted(self) -> list:
        lines: list = []
        for k in Grades.__annotations__.keys():
            lines.append(f"{field_name_from(k):<16}: {getattr(self, k):.2f}\n")
        return lines

    def Prompt() -> dict: # static function
        info: dict = {} # temporarily saving
        for k in filter(lambda k: k != k.capitalize(), Grades.__annotations__.keys()): # filter annotations to just have non-capitalized attributes
            field_name = field_name_from(k)
            while True:
                i = input(f" {field_name}: ")
                v = 0.0
                try:
                    v = float(i)
                    if v <= 20 and v >= 0:
                        info[k] = v
                        break
                    else:
                        print(f"{v} is not acceptable as {field_name} grade, enter new value")
                        continue
                except ValueError:
                    print(f"unacceptable value for {field_name} grade, please try again")
                    continue
        return info

