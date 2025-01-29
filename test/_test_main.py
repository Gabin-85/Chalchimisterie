import sys, pygame
sys.path.append("../src/")
#pygame.display.set_mode([50, 50])

import _test_file

class color:
    red = "\u001b[31m"
    green = "\u001b[32m"
    blue = "\u001b[34m"
    clear = "\u001b[0m"

checklist = []
score = [0, 0, 0]
def check(funcs:list):
    for func in funcs:
        match func():
            case True:
                checklist.append(f"{color.green}{str(func.__name__).capitalize()} (✓){color.clear}")
                score[0]+=1
            case False:
                checklist.append(f"{color.red}{str(func.__name__).capitalize()} (X){color.clear}")
                score[1]+=1
            case False:
                checklist.append(f"{color.blue}{str(func.__name__).capitalize()} (-){color.clear}")
                score[2]+=1    
        
check(_test_file.tests)

for line in checklist:
    print(line)
print()
print(f"Ok:{score[0]} | Fail:{score[1]} | Skip:{score[2]}")