def checkPrime(Num:int) -> bool:
    if Num <= 1:
        return False
    elif Num == 2:
        return True
    elif Num%10 in [1,3,7,9]:
        return True

    return False