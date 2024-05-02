# TODO: make everything complex number input supported
# TODO: finish stock market game

import math
import random
import os
from glob import glob
import pandas as pd
import numpy as np
from PIL import Image


def compare_image(photoOne: str, photoTwo: str, downSamplePercentage: float = 1) -> float:
    A = Image.open(photoOne)
    A = A.resize((int(A.width * downSamplePercentage),
                 int(A.height * downSamplePercentage)))
    A = np.array(A).flatten().astype(np.float64)
    A -= A.mean()

    B = Image.open(photoTwo)
    B = B.resize((int(B.width * downSamplePercentage),
                 int(B.height * downSamplePercentage)))
    B = np.array(B).flatten().astype(np.float64)
    B -= B.mean()

    bottom = math.sqrt(np.dot(A, A))*math.sqrt(np.dot(B, B))
    similarity = np.dot(A, B)/(bottom)

    return similarity


def copy_file(CopyThisFile: str, ToBecomeThisFile: str):
    src = CopyThisFile
    dst = ToBecomeThisFile
    if os.name == 'nt':  # Windows
        cmd = f'copy "{src}" "{dst}"'
    else:  # Unix/Linux
        cmd = f'cp "{src}" "{dst}"'
    os.system(cmd)


def check_file_existence(directory, filename):
    file_path = os.path.join(directory, filename)
    return os.path.exists(file_path)


def pick_images_cleverly(FilesToPickFrom: str, DestinationDir: str, fileType: str = ".jpg", downsamplePercent: float = 0.03, threshold: float = 0.78, printDeets: bool = False):
    n = 0
    k = 1
    key = None
    for folder in glob(FilesToPickFrom):
        for root, dirs, files in os.walk(folder):
            files.sort()
            files = [file for file in files if file.lower().endswith(fileType)]
            for i in range(len(files)-1):
                # Process each file
                if key == None:
                    key = os.path.join(root, files[i])
                    if not printDeets:
                        print(f"new keyframe at {key} (#{n})")
                    else:
                        print(f"created #{k} keyframe at image {key}")
                    copy_file(key, os.path.join(DestinationDir, files[i]))
                image = os.path.join(root, files[i+1])
                try:
                    n += 1
                    score = compare_image(key, image, downsamplePercent)
                except Exception as e:
                    if printDeets:
                        print(
                            f"unsuccesful compareing process  at #{n} when comparing:\n{key} and {image}\nErrorCode:\n{e}")
                    else:
                        print(e)
                    continue
                if score < threshold:
                    key = image
                    name = files[i+1]
                    tmp = 0
                    while check_file_existence(DestinationDir, name):
                        tmp += 1
                        name = f"({tmp})_{name}"
                    copy_file(key, os.path.join(DestinationDir, name))
                    if printDeets:
                        print(f"created #{k} keyframe at image {key} (#{n})")
                    else:
                        print(f"new keyframe at {key}")
                    k += 1
                else:
                    if printDeets:
                        print(f"skipped {image} (#{n}) Score: {score}")
                    else:
                        print(f"skipped {image}")

    print(f"processed: {n}    kept: {k/n*100} % ({k}/{n} files)")

def slightly_change_names(dir: str, whatToAddInFrontOfName: str):
    for file in os.listdir(dir):
        os.rename(f"{dir}/{file}", f"{dir}/{whatToAddInFrontOfName}_{file}")


def copy_random_files(FileOriginDir: str, DestinationDir: str, whatToAddInFrontOfName: str, percentage: int = 0.5):  # for windows
    for file in os.listdir(FileOriginDir):
        if random.random() <= percentage:
            src = f'{FileOriginDir}\{file}'
            dst = f'{DestinationDir}\{whatToAddInFrontOfName}_{file}'
            if os.name == 'nt':  # Windows
                cmd = f'copy "{src}" "{dst}"'
            else:  # Unix/Linux
                cmd = f'cp "{src}" "{dst}"'
            os.system(cmd)

# Checks if n is prime


def checkPrime(n: int) -> bool:
    """Checks if n is a prime number or not"""

    if n <= 1:
        return False

    if n == 2 or n == 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    for i in range(5, int(math.sqrt(n))+1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False

    return True

# generates a factor tree of n as a list


def factorTree(n: int) -> list:
    """returns the factor tree in a list form (smallest to largest)"""
    tree = []
    while n > 1:
        for i in range(2, int(n)+1):
            if n % i == 0:
                tree.append(i)
                n /= i
                break
    return tree

# calculates the factors of n as a list


def factors(n: int) -> list:
    """returns all factors of n in a list (smallest to largest)"""
    list = factorTree(n)
    list.insert(0, 1)
    factorD = []
    for i in list:
        for j in list:
            factorD.append(i*j)
    return rangePick(rmSame(factorD), 1, n)

# calculates a root of n with custom root


def root(base: float, root: float) -> float:
    """takes the root of base"""
    return math.pow(base, 1/root)

# calculates the quadratic roots of ax^2 + bx + c
# Complex number supported


def Qroots(a: float, b: float, c: float) -> list:
    """returns the roots of ax^2 + bx + c as a list. If there is only one root, returns it as a float. If the roots are imaginary, returns [[a,b],[c,d]] where as the first root is a + b*i, and the second is c + d*i"""
    if math.pow(b, 2) - 4*a*c > 0:
        return [(-1*b+math.sqrt(math.pow(b, 2) - 4*a*c))/(2*a), (-1*b-math.sqrt(math.pow(b, 2) - 4*a*c))/(2*a)]
    elif math.pow(b, 2) - 4*a*c == 0:
        return (-1*b+math.sqrt(math.pow(b, 2) - 4*a*c))/(2*a)
    else:
        return [[(-1*b)/(a*2), math.sqrt(abs(math.pow(b, 2) - 4*a*c))], [(-1*b)/(a*2), math.sqrt(abs(math.pow(b, 2) - 4*a*c))*-1]]

# calculates the roots of a  polynominal equation
# Complex number supported


def rootsDK(poly: list, Iter: int = 100) -> list:
    """returns the roots of poly[0]*x^n + poly[1]*x^(n-1) + ... + poly[n-1]*x^1 + poly[n]*x^0 down to the imaginary numbers using the Durand-Kerner method. set the Iter to any natural value. The higher this value, the more accurate. Default value is 100. Return syntax: [root1:[(real part),(imaginary part)],root2:[(Re),(Im)], ... ,rootN[(Re),(Im)]]"""
    for i in range(1, len(poly)-1):
        poly[i] /= poly[0]
    poly[0] = 1

    points = []
    for i in range(len(poly)-1):
        points.append(Polar2Cart(root(abs(
            1/poly[len(poly)-1]), len(poly)-1), 2*math.pi/(len(poly)-1)*i+(math.pi/(2*(len(poly)-1)))))

    for g in range(Iter):
        for i in range(len(points)):
            deno = [1, 0]
            for j in range(len(points)):
                if j != i:
                    deno = CompMul(deno, CompSub(points[i], points[j]))
            points[i] = CompSub(points[i], CompDiv(
                CompPoly(points[i], poly), (deno)))
    return points

# calculates f(x)
# CompPoly for Complex number supported


def poly(input: float, eq: list) -> float:
    """for a polynominal equation f(x) = eq[0]*x^n + eq[1]*x^(n-1) + ... + eq[n-1]*x^1 + eq[n]*x^0 returns f(input)"""
    s = []
    for i in range(len(eq)):
        s.append(eq[i]*math.pow(input, len(eq)-1-i))
    return sum(s)

# derivative of a polynominal


def Dpoly(eq: list) -> list:
    """returns the first derivative of f(x) = eq[0]*x^n + eq[1]*x^(n-1) + ... + eq[n-1]*x^1 + eq[n]*x^0"""
    for i in range(len(eq)):
        eq[i] *= len(eq)-1-i
    eq.pop()
    return eq

# performs fixed point iteration on n
# CompPolyFPIter() for complex number supported


def polyFPIter(input: float, eq: list, iter: int) -> float:
    """Returns the input calculated through eq using fixed point iteration, iter times"""
    for i in range(iter):
        input = poly(input, eq)
    return input

# performs fixed point iteration on n
# CompPolyFPIter() for complex number supported


def CompPolyFPIter(input: list, eq: list, iter: int) -> list:
    """Returns the input calculated through eq using fixed point iteration, iter times. outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    for i in range(iter):
        input = CompPoly(input, eq)
    return input

# calculates f(x)
# Complex number supported


def CompPoly(input: list, eq: list) -> list:
    """for a polynominal equation f(x) = eq[0]*x^n + eq[1]*x^(n-1) + ... + eq[n-1]*x^1 + eq[n]*x^0 returns f(input[0] + input[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    s = []
    for i in range(len(eq)):
        if type(eq[i]) == list:
            s.append(CompMul(eq[i], CompPow(input, len(eq)-1-i)))
        else:
            s.append(CompMul([eq[i], 0], CompPow(input, len(eq)-1-i)))
    return CompSum(s)

# Adds two complex numbers
# Complex number supported


def CompAdd(A: list, B: list) -> list:
    """does (A[0] + A[1]*i) + (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    return [A[0] + B[0], A[1] + B[1]]

# Adds multiple complex numbers
# Complex number supported


def CompSum(A: list) -> list:
    """returns the sum of all complex numbers [(real part),(imaginary part)] in 2D array A outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    RealP = []
    ImagP = []
    for i in A:
        RealP.append(i[0])
        ImagP.append(i[1])
    return [sum(RealP), sum(ImagP)]

# Subtracs two complex numbers
# Complex number supported


def CompSub(A: list, B: list) -> list:
    """does (A[0] + A[1]*i) - (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    return [A[0] - B[0], A[1] - B[1]]

# Multiplies two complex numbers
# Complex number supported


def CompMul(A: list, B: list) -> list:
    """does (A[0] + A[1]*i) * (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    return [A[0]*B[0]-A[1]*B[1], A[1]*B[0]+A[0]*B[1]]

# Divides two complex numbers
# Complex number supported


def CompDiv(A: list, B: list) -> list:
    """does (A[0] + A[1]*i) / (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    BDash = math.pow(B[0], 2) + math.pow(B[1], 2)
    ADash = CompMul(A, [B[0], -1*B[1]])
    return [ADash[0]/BDash, ADash[1]/BDash]

# Takes the conjugate of a complex number
# Complex number supported


def CompConj(A: list) -> list:
    """returns the conjugate of A[0] + A[1]*i outputs as [(Real part),(imaginary part)]. All values must be float or int"""
    return [A[0], -1*A[1]]

# Takes the real part of a complex number
# Complex number supported


def Re(A: list) -> float:
    """returns the real part of the complex number A[0] + A[1]*i"""
    return A[0]

# Takes the imaginary part of a complex number
# Complex number supported


def Im(A: list) -> float:
    """returns the imaginary part of the complex number A[0] + A[1]*i"""
    return A[1]

# Takes the real exponent of a complex number
# Complex number supported


def CompPow(base: list, power: float):
    """returns the complex number base[0] + base[1]*i raised to the power of "power"(real number) as [(Real part),(imaginary part)]. All values must be float or int"""
    base = Cart2Polar(base[0], base[1])
    return Polar2Cart(math.pow(base[0], power), base[1]*power)

# Converts polar coordinates to Cartigean coordinates


def Polar2Cart(r: float, theta: float, mode: str = "RAD") -> list:
    """converts polar coordinate <r,theta> to cartigean coordinate (x,y) as a list [x,y]. Optional Argument "mode" can either be "RAD" for if theta is in radians, or "DEG" if it is in degrees. Default is "RAD"."""
    if mode == "DEG":
        theta = math.radians(theta)
    return [r*math.cos(theta), r*math.sin(theta)]

# Converts Cartigean coordinates to polar coordinates


def Cart2Polar(x: float, y: float, mode: str = "RAD") -> list:
    """converts cartigean coordinate (x,y) to polar coordinate <r,theta> as a list [r,theta]. Optional Argument "mode" can either be "RAD" for if you want theta to be in radians, or "DEG" for degrees. Default is "RAD"."""
    if mode == "DEG":
        if y >= 0:
            return [math.sqrt(pow(x, 2)+pow(y, 2)), math.degrees(math.acos(x/(math.sqrt(pow(x, 2)+pow(y, 2)))))]
        else:
            return [math.sqrt(pow(x, 2)+pow(y, 2)), math.degrees(2*math.pi-math.acos(x/(math.sqrt(pow(x, 2)+pow(y, 2)))))]
    else:
        if y >= 0:
            return [math.sqrt(pow(x, 2)+pow(y, 2)), math.acos(x/(math.sqrt(pow(x, 2)+pow(y, 2))))]
        else:
            return [math.sqrt(pow(x, 2)+pow(y, 2)), 2*math.pi-math.acos(x/(math.sqrt(pow(x, 2)+pow(y, 2))))]

# Converts a string into a list with a divider


def str2list(str: str, divider: str) -> list:
    """returns a string list made out of a string, where each element is distuingished with a divider (one letter). The divider is not included in the list"""
    output = [""]
    for i in str:
        if i == divider:
            output.append("")
        else:
            output[len(output)-1] += i
    if str[len(str)-1] == divider:
        output.pop()
    return output

# Converts a list into a string with a divider


def list2str(list: list, divider: str) -> str:
    """returns a list made out of a list, where each element is distuingished with a divider (one letter). The divider is not included in the string"""
    output = str(list[0])
    for i in list[1:]:
        output += divider + str(i)

    return output

# Removes any same values in a list


def rmSame(x: list) -> list:
    """removes any duplicated values"""
    y = []
    for i in x:
        if i not in y:
            y.append(i)
    return y

# Extracts numbers from a list in a certain range


def rangePick(list: list, min: float, max: float = "inf") -> list:
    """returns numbers in list that are bigger than min (included), smaller than max (included). leave max blank for infinity"""
    output = []
    if max == "inf":
        for i in list:
            if i >= min:
                output.append(i)
    else:
        for i in list:
            if (i >= min) and (i <= max):
                output.append(i)
    return output

# Outputs a random list of numbers


def ranList(length: int, min: float = 0, max: float = 1) -> list:
    """returns a list with length length, each element being a random value between min and max"""
    output = []
    for i in range(length):
        output.append(random.random()*(abs(max)+abs(min))-abs(min))
    return output

# Outputs the standard form of a polynominal equation


def polyPrint(eq: list) -> str:
    """returns a string that shows the polynominal equation in standard form"""
    output = ""
    for i in range(len(eq)):
        if type(eq[i]) != list:
            if i == 0:
                if eq[i] < 0:
                    if eq[i] == -1:
                        output += "-"
                    else:
                        output += str(eq[i])
                elif eq[i] > 0:
                    if eq[i] != 1:
                        output += str(eq[i])
            else:
                if eq[i] < 0:
                    if eq[i] == -1:
                        output += " - "
                    else:
                        if output == "":
                            output += str(eq[i])
                        else:
                            output += " - " + str(abs(eq[i]))
                elif eq[i] > 0:
                    if eq[i] == 1:
                        output += " + "
                    else:
                        if output == "":
                            output += str(eq[i])
                        else:
                            output += " + " + str(eq[i])
        else:
            if i == 0:
                output += "(" + compPrint(eq[i]) + ")"
            else:
                output += " + (" + compPrint(eq[i]) + ")"
        if eq[i] != 0:
            if len(eq)-1-i == 0:
                if eq[i] == 1 or eq[i] == -1:
                    output += "1"
            elif len(eq)-1-i == 1:
                output += "x"
            else:
                output += "x^" + str(len(eq)-1-i)
    return output


def compPrint(comp: list, precision: int = 2) -> str:
    """returns a string that shows the complex equation in standard form"""
    comp = [round(y, precision) for y in comp]
    if comp[0] == 0:
        if comp[1] == -1:
            return "-i"
        elif comp[1] == 1:
            return "i"
        elif comp[1] == 0:
            return str(comp[1])
        else:
            return str(comp[1]) + "i"
    else:
        if comp[1] < 0:
            if comp[1] == -1:
                return str(comp[0]) + "  - i"
            else:
                return str(comp[0]) + " - " + str(abs(comp[1])) + "i"
        elif comp[1] == 0:
            return str(comp[0])
        else:
            if comp[1] == 1:
                return str(comp[0]) + " + i"
            else:
                return str(comp[0]) + " + " + str(comp[1]) + "i"


def polyExpand(roots: list):
    """complex roots should be [(real part),(imaginary part)] and real numbers should be float"""
    poly = []
    for i in range(len(roots)):
        subMulti = []
        for j in range(math.factorial(len(roots))/math.factorial(len(roots)-(i+1))/math.factorial(i+1)):
            pass  # TODO


def printTable(table: list):
    try:
        print(table)
    except:
        print("array must be a 2 dimensional array")
        raise


def genRandomWord(length: int = 5, pronouncible: bool = True):
    if not pronouncible:
        word = ""
        for i in range(len):
            word += "qwertyuiopasdfghjklzxcvbnm"[random.randint(0,)]


def controledInput(type: str = "float", prompt: str = "", rePrompt: bool = True, invalidTXT: str = "Invalid input"):
    """"this only supports float and int controled input. When rePrompt is set to true, it will keep on prompting for the correct answer. invalidTXT is the text that appears when rePrompt is true, and the user inputed a wrong value. numMin <= <userinput> <= numMax This will return "" when rePrompt is False and the user inputs an invalid input."""
    if rePrompt:
        while True:
            user_input = input(prompt)
            try:
                if type == "float":
                    user_input = float(user_input)
                    return user_input
                elif type == "int":
                    user_input = int(user_input)
                    return user_input
            except ValueError:
                print(invalidTXT)
    else:
        user_input = input(prompt)
        try:
            if type == "float":
                user_input = float(user_input)
                return user_input
            elif type == "int":
                user_input = int(user_input)
                return user_input
        except ValueError:
            return ""


def startStockGame():
    print("\n\n\nStock Market Minigame")
    print("\nEnter at least 1 player names. leave blank to go to next")
    userinput = input("Player 1 name... ")
    players = []
    while userinput == "":
        userinput = input("Player 1 name... ")
    players.append(userinput)
    userinput = input("Player 2 name... ")
    n = 2
    while userinput != "":
        if userinput not in players:
            n += 1
            players.append(userinput)
        else:
            print("That player name already exist. Please enter another one.")
        userinput = input(f"Player {n} name... ")

    printTable([["Players"]+players])
    print("")
    userinput = input(
        "Would you like to add custom companies or randomly? [y/N]... ")
    if userinput != "":
        while not (userinput.lower() == "y" or userinput.lower() == "n"):
            userinput = input(
                "Would you like to add custom companies or randomly? [y/N]... ")
            if userinput == "":
                break

    sharesName = []
    sharesPrice = []
    sharesStrength = []
    if userinput.lower() == "y":
        print("\nEnter at least 1 company.")

        userinput = input("Company 1 name... ")
        while userinput == "":
            userinput = input("Company 1 name... ")
        sharesName.append(userinput)
        sharesPrice.append(controledInput(
            "float", f"  {sharesName[-1]} starting price... "))
        sharesStrength.append(controledInput(
            "float", f"  {sharesName[-1]} aggresiveness... "))
        n = 2
        print("")
        while True:
            userinput = input(f"Company {n} name... ")
            if userinput not in sharesName:
                n += 1
                if userinput == "":
                    break
                sharesName.append(userinput)
                sharesPrice.append(controledInput(
                    "float", f"  {sharesName[-1]} starting price... "))
                sharesStrength.append(controledInput(
                    "float", f"  {sharesName[-1]} aggresiveness... "))
                print("")
            else:
                print("That company name already exist. Please enter another one.")
    else:
        print("")
        userinput = int(controledInput(
            "int", "How many companies woudl you like... "))
        while not (userinput >= 1):
            userinput = int(controledInput(
                "int", "How many companies woudl you like... "))
        for i in range(userinput):
            sharesName.append()
            sharesPrice.append()
            sharesStrength.append()
        print("")

    printTable([["Companies"]+sharesName, ["Starting price"] +
               sharesPrice, ["aggresiveness"]+sharesStrength])
