def fix_machine(debris, product):
    output = ""
    i = 0
    for char in product:
        print(debris, product[i])
        n = debris.find(char)
        if n == -1:
            break  
        output = char + output
    if output == product:
        return output
    else:
        return "Give me something that's not useless next time."
       
print(fix_machine('asdfasdfaffdsfasrthtyjrhbege', 'fed'))
