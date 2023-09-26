current = int(input("Enter current year : "))
print("=========================")
cnt = 0
child,teen,adult,middle,old = 0,0,0,0,0
born = 0000
while born != -1 :
  born = int(input("Enter born year  : "))
  age = current - born
  print("Age = %d"%age)
  print()
  if age == -1 :
    break
  elif age >= 0 and age <= 10 :
    child = child + 1
  elif age >= 11 and age <= 20 :
    teen = teen + 1
  elif age >= 21 and age <= 35 :
    adult = adult +1 
  elif age >= 36 and age <= 55 :
    middle = middle + 1
  elif age > 55 :
    old = old + 1
  cnt = cnt + 1
print("===========================")
print("Children   =  %d"%child)
print("Teenage    =  %d"%teen)
print("Adult      =  %d"%adult)
print("Middle age =  %d"%middle)
print("Old age    =  %d"%old)