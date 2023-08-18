def testARG(*arg:int):
  return [*arg]

print(testARG(2,3,1)[1])