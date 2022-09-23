test1="0.000000000000000000000123456"
test2="12345.98765432"
test3="1234.1"
test4="3456"
test5="12345.000000006789"
test6="0.056789"
test7="0.987665432"


def cutting(x):
    print(x)
    numbers = 0
    second_part = ""
    two_parts = x.split(".")
    # print(two_parts)
    for char in two_parts[1]:
        # if first part is not 0 then the second part is 3 numbers
        if two_parts[0] != "0":
            second_part += char
            numbers += 1
        # if the first part is 0 then the second part is 3 numbers that are not 0
        if two_parts[0] == "0":
            if char == "0":
                second_part += char
            else:
                second_part += char
                numbers += 1           
        # if there are 3 numbers then break the loop
        if numbers == 3:
            break
    # if the 3 numbers are 000 then there is no second part
    if second_part == "000":
        result = two_parts[0]
    else:
        result = two_parts[0] + "."+ second_part
    print(result)
    return result


# cutting(test1)
# cutting(test2)
# cutting(test3)
# cutting(test4)
# cutting(test5)
# cutting(test6)
# cutting(test7)




def OriCutting(x):
    print(x)
    numbers = 0
    second_part = ""
    two_parts = x.split(".")
    if len(two_parts) == 2:
        for char in two_parts[1]:
            second_part += char
            if char != "0":
                numbers +=1
            if numbers == 3:
                break
            if second_part == "000" and two_parts[0] != "0":
                break
    # print(second_part)
    if second_part == "000" or second_part == "":
        result = two_parts[0]
    else:
        result = two_parts[0] + "."+ second_part
    print(result)
    return result


OriCutting(test1)
OriCutting(test2)
OriCutting(test3)
OriCutting(test4)
OriCutting(test5)
OriCutting(test6)
OriCutting(test7)
