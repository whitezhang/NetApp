import filecmp
fName1 = raw_input("Name one:")
fName2 = raw_input("Name two:")

print filecmp.cmp(fName1, fName2)