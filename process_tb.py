# globals

usage = {}
teams = 0
'''
input: rtype: .txt
Output: rtype: dict
'''

# Pokemon can only appear after a whitespace a line before
# check if "=" in line as this indicates a new team in a ordner 
# check if an empty line follows after an empty line
def check_tb(file):
    with open (f"{file}.txt") as f:
        global teams
        flag = False
        for line in f:
            if flag and line[0] not in ["=", "\n"]:
                pokemon = line.strip()
                if pokemon in usage:
                    count = usage.get(pokemon)
                    usage[pokemon] = count+1
                else:
                    usage[pokemon] = 1
                flag = False
            if line in ["\n"]:
                  flag = True
            if line[0] in ["="]:
                teams+=1
            else:
                pass

# for example
check_tb("svscout")
print("Sorted: ")
usage = {k: v for k, v in sorted(usage.items(), key=lambda item: item[1], reverse= True)}
print (teams)

for key, val in usage.items():
    print(f"The Pokemon {key} was used {val} times. This is a usage of {str(round(val/teams,2))}%!")
    
print(usage)


