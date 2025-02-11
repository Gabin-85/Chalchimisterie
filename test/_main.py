import sys, pygame
sys.path.append("../src/")
pygame.display.set_mode([50, 50])

import _file

class formating:
    red:str = "\u001b[31m"
    green:str = "\u001b[32m"
    blue:str = "\u001b[34m"
    yellow:str = "\u001b[33m"
    clear:str = "\u001b[0m"

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
                print(f"{formating.blue}[-] {function["function_name"]}(){formating.clear}")
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
                print(f"{formating.green}[✓] {function["function_name"]}(){formating.clear}")
                score["pass"] += 1
                continue
            else:
                print(f"{formating.red}[X] {function["function_name"]}(){formating.clear}")
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
                    print(f"   |{formating.green}{test}{formating.clear}")
                    continue
                else:
                    print(f"   |{formating.red}{test}{formating.clear}")
                del status

                if type(function["tests"][test]) == bool:
                    continue
                for case in function["tests"][test]:
                    if function["tests"][test][case] == True:
                        print(f"     |{formating.green}{case}{formating.clear}")
                    else:
                        print(f"     |{formating.red}{case} <--{formating.clear}")
    
    print(f"\nFiles: {score["file"]}")
    print(f"Functions: {score["function"]}")
    print(f"Tests: {score["test"]}")
    print(f"Cases: {score["case"]}")
    print(f"\n{formating.green}Pass: {score["pass"]}{formating.clear} | {formating.blue}Skip: {score["skip"]}{formating.clear} | {formating.red}Fail: {score["fail"]}{formating.clear}")

test_unit([_file])