###########################################
# Version: 1.0.4 
# Author: sylvi
# Last Time edited: 20:20 28.02.2023
###########################################

# globals
# can change that as well cuz of security reasons NEEDED

teams = []
usage = {}
usage_moves = {}
usage_percentage = {}

# prep input: MANUAL OUTPUT FROM https://replaystats-eo.herokuapp.com/scouter/ WITH MANUAL INPUT WITH REPLAYS: .txt file
# input: oppname to get the file: string, alt: names from the opp: [string]
# output: formatted file ready to precess: .txt file
#
# algorithm: goes thru the input and only copies the winning team in the new file
#
# sample booty.txt file:
# REYSCARFACE:
# Breloom: Swords Dance / Spore / Bullet Seed / Mach Punch
# Volcarona: Quiver Dance / Bug Buzz
# Diancie: Stealth Rock / Substitute / Endeavor
# Dragonite: Dragon Dance / Supersonic Skystrike
# Magearna: Ice Beam / Calm Mind / Substitute
# Landorus-Therian: U-turn / Earthquake
#
# BOOTY:
# Mawile: Sucker Punch
# Gliscor: Toxic / Earthquake
# Chansey: Stealth Rock / Thunder Wave / Seismic Toss / Soft-Boiled
# Magnezone: Volt Switch
# Slowbro: Scald / Ice Beam
# Kartana: 
#
# in that case the array alt looks like this: ["BOOTY:/n"]. 
# IN this format the format is always a player name
# while lines in file:
#  1. check if name in alt. If true, copy everything until \n. if false, wait until \n
#  2. if \n ask again for flag for name because after a \n follows again a name 
#
# checks if the name is in the alt array 
#
# ideas: improve the space complexity
#
# Time O(n)

def make_copy (opp, alts):
    safe = False
    check = True
    for ind, alt in enumerate(alts):
        alts[ind]= f"{alt.upper()}:\n"
    with open(f"{opp}.txt", encoding="utf8") as f:
        with open(f"copy{opp}.txt", "w", encoding="utf8") as f2:
            for line in f:
                if safe:
                    f2.write(line)
                if check: 
                    if line in alts: 
                        safe = True
                    check = False
                if line in ["\n"]:
                    safe = False
                    check = True

# input: opponents name of the copyfile: string
# output: teams with full movesets: dict
#
# algorithm:
# 1. splits the current line in the file with the char ":" to seperate pokemon from their attacks
# 2. split the moves by "/" and some data cleaning, removes spaces as sd auto converts them anyhow (CAN IMPROVE ON THAT)
# example: ['Gliscor', ['Toxic', 'Earthquake']]
# 3. make a dict where the pkmn is the key and moves the value
# 4. repeat 3. so often until run out of teams and add all the dicts into a list
#
# Time O(n^2)
#
# DISCLAIMER: outdated version with fixed knwon bugs like '""' as a move when a pkmn doesnt reveal a moveset at all
# new version added asap

def make_teams (opp):
    with open(f"copy{opp}.txt") as f:
        team = []
        for line in f:
            if line not in ["\n"]:  
                moves = []
                pkmn = line
                pkmn = pkmn.split(":")
                pkmn[1] = pkmn[1].replace("\n","").replace(" ", "").split("/")
                for move in pkmn[1]:
                    moves.append(move)
                pokemon = {pkmn[0]: moves}
                team.append(pokemon)
            else:
                if len(team) != 0:
                    teams.append(team)
                team = []

# global: use of global teams: list[{string: [string]}]
# output: dict {pkmn: usage}
# 
# algorithm: 
# 1. loops tru all the keys in teams (all the pokemons)
# 2. if pkmn already in usage dict, increment the value in the usage dict
# 2. else: add pkmn to usage and set default value to 1 
#
# Time O(n^2)
#
# Optimize same code of line in usage and movesets method

def make_usage():
    global usage
    for team in teams:
        for pkmn in team:
            pokemon = list(pkmn.keys())
            pokemon = str(pokemon).replace("['","").replace("']","")
            if pokemon in usage:
                count = usage.get(pokemon)
                usage[pokemon] = count+1
            else:
                usage[pokemon] = 1

    usage = {k: v for k, v in sorted(usage.items(), key=lambda item: item[1], reverse= True)}
    print(teams)
    max_usage = len(teams)
    for key, value in usage.items():
        usage_percentage[key] = f"{round((value / max_usage)*100,2)}%"
    for k, v in usage_percentage.items():
        print(f"**{k}** was used _{v}_ in {max_usage} games!")

# global: use of global teams: list [[{pkmn: moves}],...]
# output: dict {pkmn: {move: usage}}
#
# same as make usage just with the add of the moves to loop thru as well
# 1. loops tru all the keys in teams (all the pokemons)
# 2. if the move of pkmn already in usage_moves dict, increment the value in the usage_moves dict
# 2. else: add move pkmn to usage and set default value to 1 
#
# Time O(n^3) Yikes..

def make_usage_moves():
    global usage_moves
    for team in teams:
        for pkmn in team:
            pokemon = list(pkmn.keys())
            pokemon = str(pokemon).replace("['","").replace("']","")
            moves = pkmn.get(pokemon)
            if pokemon not in usage_moves:
                usage_moves[pokemon] = {}
            for move in moves:
                if move in [""]:
                        break
                if move in usage_moves[pokemon]:
                            count = usage_moves[pokemon].get(move)
                            usage_moves[pokemon][move] = count + 1
                else:
                    usage_moves[pokemon][move] = 1
    for key, val in usage_moves.items():
        usage_moves[key] = {k: v for k, v in sorted(val.items(), key=lambda item: item[1], reverse= True)}
    for key, val in usage_moves.items():
        f = ""
        for k in val.items():
            f += f"_{k[0]} {k[1]}x_ , " 
        f = list(f)
        try:
            f[-2] = "!"
        except:
            pass
        f = "".join(f)
        print(f"**{key}** used {f}")




# global: teams: [[{pkmn: moves}],...], 
# input: opp: string, gen: string, tour: string
# output: paste: .txt
#
# makes an paste (which can be converted to ps first to get the appropiate spaces for moves)
# example:
'''
=== [gen7ou] SPL sab Scouting/ SPLXIV 1 ===

Mawile 
- SuckerPunch 

Gliscor 
- Toxic 
- Earthquake 

Chansey 
- StealthRock 
- ThunderWave 
- SeismicToss 
- Soft-Boiled 

Magnezone 
- VoltSwitch 

Slowbro 
- Scald 
- IceBeam 

Kartana 
-  
'''
# loop through all the Teams and write them in the pokepaste format in their own folder 
# making a folder cuz it is easier to work with the output later
#
# Time: O(n)
# Space O(n)

def paste(opp, tier, tour):
    with open (f"{opp}paste.txt", "w") as f:
        for ind, team in enumerate(teams):
            f.write(f"=== [{tier}] SPL {opp} Scouting/{tour} {str(ind+1)} ===\n")
            f.write("\n")
            for pkmn in team:    
                pokemon = list(pkmn.keys())
                pokemon = str(pokemon).replace("['","").replace("']","")
                moves = pkmn.get(pokemon)
                f.write(f"{pokemon} \n")
                for move in moves:
                    f.write(f"- {move} \n")
                f.write("\n")

# input: opp: string, alts: [string], tier: string, tor: string,
# output: void
#
# just a nice method to make the overview of the methods better

def main(opp, alts, tier, tour="Team"):
    make_copy(opp, alts)
    make_teams(opp)
    make_usage()
    print("\n")
    make_usage_moves()
    paste(opp, tier, tour)
    max_usage = len(teams)
    print(f"Tested on {max_usage} replays!")
    print("--------------------------------")
    
    print("\n")

# example run 
main("sab", ["SABeLLA", "BOOTY", "BARGAIN BOOTY"], "gen7ou")
