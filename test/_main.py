import sys, pygame
sys.path.append("../src/")
pygame.display.set_mode([50, 50])
import args
args.consoleLevel = set()

import _file

class color:
    red = "\u001b[31m"
    green = "\u001b[32m"
    blue = "\u001b[34m"
    yellow = "\u001b[33m"
    clear = "\u001b[0m"

def check_function(func) -> dict:
    checklist:dict = {"function_name":str(func.__name__)} 

    try:
        func.setup()
    except Exception:
        checklist["setup"] = False
        return checklist
    
    checklist["setup"] = True
    checklist["tests"] = {}
    for test in func.tests:
        checklist["tests"][test] = {}

        if type(func.tests[test]) != dict:
            try:
                func.tests[test]()
                checklist["tests"][test] = True
            except Exception:
                checklist["tests"][test] = False
            continue

        for case in func.tests[test]:
            try:
                func.tests[test][case]()
                checklist["tests"][test][case] = True
            except Exception:
                checklist["tests"][test][case] = False
    return checklist
            
def check_file(file) -> dict:
    checklist:dict = {"file_name":str(file.__name__), "functions":[]}

    for func in file.functions:
        checklist["functions"].append(check_function(func))
    return checklist

def test_unit(files:list) -> dict[int]:
    score = {"pass":0, "skip":0, "fail":0, "file":0, "function":0, "test":0, "case":0}

    for file in files:
        score["file"] += 1
        checklist = check_file(file)

        print(f"\n[{checklist["file_name"]}.py]:\n")

        for function in checklist["functions"]:
            score["function"] += 1

            if function["setup"] == False:
                print(f"{color.blue}[-] {function["function_name"]}(){color.clear}")
                score["skip"] += 1
                continue

            status = True
            for test in function["tests"]:
                score["test"] += 1
                
                if type(function["tests"][test]) == bool:
                    score["case"] += 1
                    if function["tests"][test] == False:
                        status = False
                    continue

                for case in function["tests"][test]:
                    score["case"] += 1
                    if function["tests"][test][case] == False:
                        status = False

            if status == True:         
                print(f"{color.green}[✓] {function["function_name"]}(){color.clear}")
                score["pass"] += 1
                continue
            else:
                print(f"{color.red}[X] {function["function_name"]}(){color.clear}")
                score["fail"] += 1
            del status

            for test in function["tests"]:

                status = True
                if type(function["tests"][test]) == bool:
                    if function["tests"][test] == False:
                        status = False
                else:
                    for case in function["tests"][test]:
                        if function["tests"][test][case] == False:
                            status = False
                            break

                if status == True:         
                    print(f"   |{color.green}{test}{color.clear}")
                    continue
                else:
                    print(f"   |{color.red}{test}{color.clear}")
                del status

                if type(function["tests"][test]) == bool:
                    continue
                for case in function["tests"][test]:
                    if function["tests"][test][case] == True:
                        print(f"     |{color.green}{case}{color.clear}")
                    else:
                        print(f"     |{color.red}{case} <--{color.clear}")
    
    print(f"\nFiles: {score["file"]}")
    print(f"Functions: {score["function"]}")
    print(f"Tests: {score["test"]}")
    print(f"Cases: {score["case"]}")
    print(f"\n{color.green}Pass: {score["pass"]}{color.clear} | {color.blue}Skip: {score["skip"]}{color.clear} | {color.red}Fail: {score["fail"]}{color.clear}")

test_unit([_file])