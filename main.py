import math


# Number theory stuff
def checkPrime(n: int) -> bool:

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


# Calculations
def root(base: float, root: float) -> float:
	return math.pow(base, 1/root)


# Complex Numbers
def CompAdd(A: list, B: list) -> list:
	"""does (A[0] + A[1]*i) + (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
	return [A[0] + B[0], A[1] + B[1]]


def CompSub(A: list, B: list) -> list:
	"""does (A[0] + A[1]*i) - (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
	return [A[0] - B[0], A[1] - B[1]]


def CompMul(A: list, B: list) -> list:
	"""does (A[0] + A[1]*i) * (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
	return [A[0]*B[0]-A[1]*B[1], A[1]*B[0]+A[0]*B[1]]


def CompDev(A: list, B: list) -> list:
	"""does (A[0] + A[1]*i) / (B[0] + B[1]*i) outputs as [(Real part),(imaginary part)]. All values must be float or int"""
	BDash = B[0] ^ 2 + B[1] ^ 2
	ADash = CompMul(A, [B[0], -1*B[1]])
	return [ADash[0]/BDash, ADash[1]/BDash]


def CompConj(A: list) -> list:
	"""returns the conjugate of A[0] + A[1]*i outputs as [(Real part),(imaginary part)]. All values must be float or int"""
	return [A[0], -1*A[1]]


# Conversions
def Polar2Cart(r: float, theta: float, mode: str = "RAD") -> list:
	"""converts polar coordinate <r,theta> to cartigean coordinate (x,y) as a list [x,y]. Optional Argument "mode" can either be "RAD" for if theta is in radians, or "DEG" if it is in degrees. Default is "RAD"."""
	if mode == "DEG":
		theta = math.radians(theta)
	return [r*math.cos(theta), r*math.sin(theta)]


def Cart2Polar(x: float, y: float, mode: str = "RAD") -> list:
	"""converts cartigean coordinate (x,y) to polar coordinate <r,theta> as a list [r,theta]. Optional Argument "mode" can either be "RAD" for if you want theta to be in radians, or "DEG" for degrees. Default is "RAD"."""
	if mode == "DEG":
		if y >= 0:
			return [math.sqrt(x ^ 2+y ^ 2), math.degrees(math.acos(x/(math.sqrt(x ^ 2+y ^ 2))))]
		else:
			return [math.sqrt(x ^ 2+y ^ 2), math.degrees(2*math.pi-math.acos(x/(math.sqrt(x ^ 2+y ^ 2))))]
	else:
		if y >= 0:
			return [math.sqrt(x ^ 2+y ^ 2), math.acos(x/(math.sqrt(x ^ 2+y ^ 2)))]
		else:
			return [math.sqrt(x ^ 2+y ^ 2), 2*math.pi-math.acos(x/(math.sqrt(x ^ 2+y ^ 2)))]
