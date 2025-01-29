import sys, pygame
sys.path.append("../src/")
pygame.display.set_mode([50, 50])

import _file

class color:
    red = "\u001b[31m"
    green = "\u001b[32m"
    blue = "\u001b[34m"
    yellow = "\u001b[33m"
    clear = "\u001b[0m"

checklist = []
score = [0, 0, 0]
def check(name:str, funcs:list):
    checklist.append(f"{name.capitalize()}:")
    for func in funcs:
        try:
            func()
            checklist.append(f"{color.green}{str(func.__name__).capitalize()} (✓){color.clear}")
            score[0]+=1

        except Exception as err:
            print(f"{color.yellow}{err}{color.clear}")
            checklist.append(f"{color.red}{str(func.__name__).capitalize()} (X){color.clear}")
            score[1]+=1
            for i in range(funcs.index(func)+1, len(funcs)):
                checklist.append(f"{color.blue}{str(funcs[i].__name__).capitalize()} (-){color.clear}")
                score[2]+=1
            break

    checklist.append("")
        
check("File.py -> create", _file.create.tests)
check("File.py -> duplicate", _file.duplicate.tests)
check("File.py -> close", _file.close.tests)

for line in checklist:
    print(line)
print(f"Ok:{score[0]} | Fail:{score[1]} | Skip:{score[2]}")