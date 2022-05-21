# This is the code for the "Huggable Animals" text adventure.
# This program was written as a final project for the
# Codecademy CS101 curriculum.
# 
# The game will present the player with a randomly selected animal.
# The play must then select available actions to attempt to
# befriend the animal until it eventually allows them to hug
# it. The game is won if the player is able to successfully hug
# the dragon.

# This game was created by Bryan Smith in May 2022

import random
import time

##########################################################################################################################
# Establish object classes
##########################################################################################################################

# Define class for Player object.

class Player():
    name = "Huggy"
    health = 10
    tools = []
    items = []
    level = 1
    experience = 0

    # Create initialization funciton
    def __init__(self):
        self.change_name()
        self.set_stats()

    # Change the players name
    def change_name(self):
        name = input("Greetings, intrepid animal lover, what is your name? \n\n\n     ")

        if name == "":
            yn_ans = input("Well I have to call you SOMEthing. Will you please tell me your name? (Y/N) ")
            if yn_ans.upper() == "Y":
                name = input("What would you like me to call you? ")
            else: 
                print("Okay, then... I suppose I'll call you 'Huggy'")
                name = "Huggy"
            
        self.name = name

        print("\033c")


        print("Nice to meet you, {player_name}! It's time to get started on your adventure!\n\n".format(player_name = self.name))

    # Set the players initial stats
    def set_stats(self):
        pass

    #
    def gain_experience(self, xp_earned):
        self.experience += xp_earned

        

        if self.experience >= self.level**2 * 10:
            self.level_up()
            print_header(player)

            #print("You have gained {} experience!\n".format(xp_earned))

            print("Congratulations! you have leveled up! You are now level {}.\n".format(self.level))
            press_enter()

        else:
            print_header(player)
            print("You have gained {} experience!\n".format(xp_earned))
            press_enter()


    # Increase health and level value when leveling up
    def level_up(self):
        self.level += 1
        self.health = 10 + round(self.level**3)
        

    def add_health(self, num):
        self.health += num

    def gain_item(self, item):
        self.items.append(item)

# Define class for Animal object
class Animal():
    
    # Initiate an animal class with a list of stats in the following order: [name, difficulty, friendship, irritability, skittishness, docility, experience, attack]
    # Stat explanations:
    #  - name = the displayed name for the animal
    #  - difficulty, 1-100, indicates the challenge level of the animal 
    #  - friendship, -100 to 100, how receptive the animal is to the player's actions
    #  - irritiability, 1-100, how likely an animal is to attack after failed interaction
    #  - skittishness, 1-100, how likely an animal is to run after failed interaction
    #  - docility, 1-100, how likely an animal is to remain after a failed interaction
    #  - experience, >= 0, indicates how much experience is gained when hugging an animal
    #
    #   When an action fails, the irritability, skittishness, and docility will be combined with a random number generator
    #   to determine if the animal attacks, runs, or remains. These values can be adjusted based on interactions.
    #  
    def __init__(self, name):
        self.name = name
        #stat_list_titles = ["name", "difficulty", "friendship", "irritability", "skittishness", "docility", "experience", "attack"]
        self.actions = []
        self.base_stats = {}
        # loop_count = 0
        #for title in stat_list_titles:
        #    setattr(self, title, stats[loop_count])
        #    loop_count += 1
        self.art = ''

    def __repr__(self):
        out_string = ""
        
        out_string += "Name: " + self.name
        # out_string += "\nDifficulty: " + str(self.difficulty)
        # out_string += "\nFriendship: " + str(self.friendship)
        # out_string += "\nIrritability: " + str(self.irritability)
        # out_string += "\nSkittishness: " + str(self.skittishness)
        # out_string += "\nDocility: " + str(self.docility)
        # out_string += "\nExperience: " + str(self.experience)
        # out_string += "\nAttack: " + str(self.attack)

        out_string += "\n"

        return out_string
    
    def roll_new(self):
        # When rolling a new animal, the stats can vary +/- 25% of the base
        self.difficulty = round(self.base_stats["difficulty"] * (1 + (random.random()*0.5 - 0.25)))
        self.friendship = round(self.base_stats["friendship"] + (random.random()*15))
        self.irritability = round(self.base_stats["irritability"] * (1 + (random.random()*0.5 - 0.25)))        
        self.skittishness = round(self.base_stats["skittishness"] * (1 + (random.random()*0.5 - 0.25)))
        self.docility = round(self.base_stats["docility"] * (1 + (random.random()*0.5 - 0.25)))
        self.experience = self.difficulty
        self.attack = round(self.base_stats["attack"] * (1 + (random.random()*0.5 - 0.25)))
    

# Define environment objects to add flavor text to encounters
class Environment():
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Action():
    def __init__(self, name, success_threshold = 50, success_msg = '', failure_msg = ''):
        self.name = name
        self.success_threshold = success_threshold
        self.success_msg = success_msg
        self.failure_msg = failure_msg
    
    def __repr__(self):
        return self.name

####################################################################################################################################
# This section is dedicated to creating action objects
####################################################################################################################################

pet_head = Action("Pet Head", 25, "Success! The {name} really liked getting pet on the head!\n", "Uh oh! It looks like the {name} is not in the mood for head pets!\n")
chin_scritch = Action("Scritch Chin", 40, "OOOHohoho, those was some gUUUd chin scritches. The {name} is pleased.\n", "The {name} isn't having it. It doesn't know you well enough to let you scritch its chin like that.\n")
belly_rubs = Action("Belly Rubs", 60, "Somebody loves a good belly rub! And that somebody is this {name}. They are VERY satisfied\n", "The {name} jumps back and recoils in anger. How DARE you touch its precious belly!\n")
butt_brush = Action ("Brush Butt", 50, "The {name} starts boogeying, leaning into the brush. They seem to be having a great butt time!\n", "That was awfully presumptuous! How would you like it if the {name} brushed YOUR butt? Well, you might like it, but they certainly didn't\n")
offer_treat = Action("Offer Treat", 10, "A bold move offering that {name} a treat, you could have lost a finger! Yet fortune favors the bold,\n the {name} graciously accepts it.\n", "The {name} is allergic to that treat! What are you, tring to poison it?!?\n")
polish_horns = Action("Polish Horns", 80, "Forget the proverbs, you just LITERALLY grabbed the {name} by the horns, and not only did you survive, but you left them with a mirror-like finish\n", "This was a bad idea. You knew this was a bad idea, but the {name} just confirmed that this was a bad idea.\n")


####################################################################################################################################
# This section is dedicated to creating animal objects
####################################################################################################################################
# For reference: stat_list_titles = ["name", "difficulty", "friendship", "irritability", "skittishness", "docility", "experience", "attack"]

animals_list = []

# Stats for Golden Retriever
golden_ret = Animal("Golden Retriever")
animals_list.append(golden_ret)
golden_ret.base_stats = {
    "difficulty": 10,
    "friendship": 15,
    "irritability": 10,
    "skittishness": 10,
    "docility": 70,
    "experience": 10,
    "attack": 3
    }

golden_ret.description = "Eyes bright and tail wagging, a GOLDEN RETRIEVER bounds toward you excitedly!\n"
golden_ret.actions = [offer_treat, pet_head, chin_scritch, belly_rubs]


# Stats for Bunny
bunny = Animal("Bunny")
animals_list.append(bunny)
bunny.base_stats = {
    "difficulty": 20,
    "friendship": 0,
    "irritability": 10,
    "skittishness": 80,
    "docility": 70,
    "experience": 20,
    "attack": 1
    }
bunny.description = "A Bunny is here!\n"
bunny.actions = [offer_treat, pet_head]

# Stats for house cat
cat = Animal("House Cat")
animals_list.append(cat)
cat.base_stats = {
    "difficulty": 30,
    "friendship": 0,
    "irritability": 50,
    "skittishness": 40,
    "docility": 70,
    "experience": 30,
    "attack": 4
    }
cat.description = "It's a House Cat!\n"
cat.actions = [offer_treat, pet_head, chin_scritch]

# Stats for sea turtle
turtle = Animal("Sea Turtle")
animals_list.append(turtle)
turtle.base_stats = {
    "difficulty": 40,
    "friendship": 0,
    "irritability": 20,
    "skittishness": 10,
    "docility": 80,
    "experience": 40,
    "attack": 10
    }
turtle.description = "A Sea Turtle turts around on the beach in front of you.\n"
turtle.actions = [pet_head, butt_brush]

# Stats for black bear
b_bear = Animal("Black Bear")
animals_list.append(b_bear)
b_bear.base_stats = {
    "difficulty": 50,
    "friendship": 0,
    "irritability": 70,
    "skittishness": 30,
    "docility": 40,
    "experience": 50,
    "attack": 20
    }
b_bear.description = "Which bear is best? A Black Bear! And now one is staring you in the face.\n"
b_bear.actions = [pet_head, chin_scritch]

# Stats for tiger
tiger = Animal("Tiger")
animals_list.append(tiger)
tiger.base_stats = {
    "difficulty": 60,
    "friendship": 0,
    "irritability": 80,
    "skittishness": 10,
    "docility": 30,
    "experience": 60,
    "attack": 30
    }
tiger.description = "Eeny Meeny Miney Moe - Hugging tigers is super dope. Now's your chance, because a Tiger is here! \n"
tiger.actions = [pet_head, chin_scritch]

# Stats for viper
viper = Animal("Viper")
animals_list.append(viper)
viper.base_stats = {
    "difficulty": 70,
    "friendship": 0,
    "irritability": 80,
    "skittishness": 30,
    "docility": 10,
    "experience": 70,
    "attack": 70
    }
viper.description = "A deadly Viper slithers out from underneath your credenza! But you, intrepid animal-hugger, know that even the non-cuddly animals need hugs!\n" 
viper.actions = [pet_head, chin_scritch]

# Stats for Minotaur
minotaur = Animal("Minotaur")
animals_list.append(minotaur)
minotaur.base_stats = {
    "difficulty": 80,
    "friendship": 0,
    "irritability": 90,
    "skittishness": 10,
    "docility": 20,
    "experience": 80,
    "attack": 50
    }
minotaur.description = "With a mighty roar, a MINOTAUR charges you from a nearby hedge maze! A less committed hugger would cower, but you know that all they need is a friend.\n"
minotaur.actions = [pet_head, chin_scritch, polish_horns]

# Stats for Introvert
introvert = Animal("Introvert")
animals_list.append(introvert)
introvert.base_stats = {
    "difficulty": 90,
    "friendship": 0,
    "irritability": 20,
    "skittishness": 80,
    "docility": 90,
    "experience": 90,
    "attack": 10
    }
introvert.description = "Before you sits one of the most challenging animals for even the most professional of huggers. The INTROVERT! Careful, I hear they can be grumpy!\n"
introvert.actions = [pet_head, chin_scritch]

###### Dragon stats are test stats to be changed later
dragon = Animal("Dragon")
animals_list.append(dragon)
dragon.base_stats = {
    "difficulty": 100,
    "friendship": -50,
    "irritability": 90,
    "skittishness": 90,
    "docility": 10,
    "experience": 100,
    "attack": 100
    }
dragon.description = "In front of you looms a massive D R A G O N!!! They like to cuddle, right?\n"
dragon.actions = [pet_head, chin_scritch, polish_horns]

####################################################################################################################################
# This section is dedicated to creating environment objects
####################################################################################################################################

environment_list = []

forest_desc = "You wander into a warm and dense forest. beams of sunlight pierce the canopy to fall gently on the ground." + \
    " The air smells of fresh pine. Before you, you see..."
forest = Environment('Forest', forest_desc)
environment_list.append(forest)





#################################################################################################################################
# Core game functions
#################################################################################################################################
def failed_action(animal):
    # Roll a random number for irritability, skittishness, and docility, the largest will determine the animals actions
    irrit = roll_number()+animal.irritability
    skitt = roll_number() + animal.skittishness
    doc = roll_number() + animal.docility

    print_header(player)

    if doc >= irrit and doc >= skitt:
        # Return to start of encounter
        print('The {} glares at you disapprovingly\n'.format(animal.name))
        press_enter()

        # If animal neither runs nor attacks, increase the irritability or skittishness
        flip_coin = round(random.random())
        if flip_coin == 0:
            animal.irritability += animal.difficulty/4
        else:
            animal.skittishness += animal.difficulty/4
        
        return "animal stays"
    elif skitt >= irrit:
        # Animal runs, draw new animal
        print('You scared the {}! It ran away.\n'.format(animal.name))
        press_enter()

        return "animal runs"
    else:
        #animal attacks
        print('You angered the {}. It ATTACKS! Doing {} damage\n'.format(animal.name, animal.attack))
        press_enter()
        player.add_health(1-animal.attack)
        return "animal stays"


# Function to process user commands other than Give Hug and Run Away (those are handled elsewhere)
def take_action(action, animal, affinity = 0):
    # Minimum score required for success:
    success_threshold = action.success_threshold 

    # Increase success threshold by animal difficulty
    success_threshold += animal.difficulty

    # Reduce threshold by friendship score and player level
    success_threshold -= animal.friendship/2
    success_threshold -= player.level*10

    num = roll_number()

    #print("Success Threshold = {}, you rolled: {}\n".format(success_threshold, num))



    if num >= success_threshold:
        print(action.success_msg.format(name = animal.name))

        # If the action is too easy, reduce the benefit.
        if (action.success_threshold + animal.difficulty)/2 + animal.friendship < action.success_threshold * 2:
            animal.friendship += (action.success_threshold + animal.difficulty)/2
        else:
            animal.friendship += (action.success_threshold + animal.difficulty)/5
        

        press_enter()
        return "animal stays"

    else:
        print(action.failure_msg.format(name = animal.name))
        animal.friendship -= (action.success_threshold + animal.difficulty)/2


        press_enter()
        return failed_action(animal)

# Give_hug is a special action that will either lead to success in the encounter or an attack from the animal.
# Threshold is defined as twice the animal difficulty minus the friendship level.
def give_hug(animal):
    # Hug should succeed 1 in 20 times before modifiers
    success_threshold = 95 + animal.difficulty - animal.friendship/2 - player.level * 10

    # print_header(player)
    num = roll_number()
    # num = 1000 # Set num to 1000 to force victory for testing purposes.

    #print_header(player)

    

    # If roll is successful increase player experience, check for player level up, end encounter
    if num >= success_threshold:
        
        # check_level_up(player)
        if animal.name == "Dragon":
            print_header(player)

            #print('Success Threshold = {}, you rolled: {}\n'.format(success_threshold, num))
            
            print("What?!?! No, that can't be! The Dragon is... HUGGING YOU BACK?!?!? This completely upends all of the conventional \nknowledge and scientific study on human-dragon interactions.\n")

            press_enter()
            return "win"
        else:
            print_header(player)
            #print('Success Threshold = {}, you rolled: {}\n'.format(success_threshold, num))
            print("The {} accepted your hug. You are now best buds!\n".format(animal.name))
            print("You gain {} experience.\n".format(animal.experience))
            press_enter()

            player.gain_experience(animal.experience)
            return "success"
    else: 
        player.add_health(-1*animal.attack)
        print_header(player)
        #print('Success Threshold = {}, you rolled: {}\n'.format(success_threshold, num))
        print("The {} is not ready to be hugged. It attacks! You take {} damage.\n".format(animal.name, animal.attack))
        animal.friendship -= (success_threshold)/2
        press_enter()
        return "animal stays"




def draw_animal(player):
    # Build weights list for each animal in animal list.
    # Compare player level * 10 to animal difficulty. Reduce likelihood by 1/2 for every 10 points of difference. Weight of 100 for  0 points.

    weight = []
    for item in animals_list:
        level_diff = abs(player.level * 10 - item.base_stats["difficulty"])
        weight.append((0.4**(level_diff/10))*100)

    #print(weight)
    #press_enter()

    return random.choices(animals_list, weights=weight)



def roll_number(num = 100):
    return round(random.random()*num)

# Function to print "Press enter to continue" prompt
def press_enter():
    input("Press enter to continue.\n")
    print("\033c")
    

# Function to determine if player died, returns boolean
def is_dead(player, animal):
    if player.health <= 0:
        print_header(player)
        print("You have {} health. Looks like that {} killed you. \n\nAt least you died doing what you loved - giving dangerous animals hugs.\n".format(player.health, animal.name))
        press_enter()
        return True

def print_header(player):
    print("\033c")
    print("--------------------------------------------------------------------------------------------------------------")
    print("||   {}                   Level: {}          Experience: {}                          Current Health = {} ||".format(player.name, player.level, player.experience, player.health))
    print("--------------------------------------------------------------------------------------------------------------\n")


##################################################################################################################################
# Start of main game code
##################################################################################################################################
# Intiate game_over and game_won tags
game_over = False
game_won = False

### Startup ###
print("\033c")
print("""\
            000000000000000000000000000000000000000000000000000000000000000000000000000
        00000000000000000000000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000000000000                                                                           000000000000
000000000000                            The UnHuggables!!!                             000000000000
000000000000                                                                           000000000000
 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
        00000000000000000000000000000000000000000000000000000000000000000000000000000000000
            000000000000000000000000000000000000000000000000000000000000000000000000000    
    
    
    """)

press_enter()

# Invite player to input name
player = Player()

# for i in range(5):
#     print('.')
#     time.sleep(1)
press_enter()



### Begin Encounters ###

while game_over == False:
    print_header(player)
    print("!!!!!!!!!!!!!!!!!!!!  A NEW ANIMAL APPROACHES  !!!!!!!!!!!!!!!!!!!!!!\n")
    press_enter()



    print_header(player)
    # Draw animal
    animal = draw_animal(player)[0]
    
    # Reset object stats for new animal
    animal.roll_new()



    # Reset encounter end flag
    encounter_over = False

    #initiate encounter counter - force a new loop if too many actions are taken
    encounter_counter = 0
    
    while encounter_over == False:
        # Increment counter
        encounter_counter += 1
        
        # Clear screen and print encounter description
        # print("\033c")


        # Print encounter description

        #

        # Print character status
        print_header(player)

        print(animal.description)

        print('On a scale of 1 to Friendly, you would rate this {} a {}.\n'.format(animal.name, str(round(animal.friendship))))

        # Print action options

        print('You feel that you can...')

        action_count = 0
        action_options = ''
        for item in animal.actions:
            action_count += 1

            action_options += str(action_count) + ". {}   ".format(item.name)
        
        action_options += str(action_count + 1) + ". Give Hug   " + str(action_count + 2) + ". RUN AWAY!   \n"

        print(action_options)

        # Accept user selection with error handling for non-number or number out of range
        valid_input = False
        while not valid_input:
            try:
                action_choice = int(input("What do you do (enter number)? "))
            except:
                print("\nINVALID INPUT: Please enter a number between 1 and {}".format(action_count + 2))
                continue

            if action_choice > action_count + 2 or action_choice < 1:
                print("\nINVALID INPUT: Please enter a number between 1 and {}".format(action_count + 2))
            else:
                valid_input = True



        print("\033c")
        print_header(player)

        # while (not isnumber(action_choice)) or action_choice > action_count:
        #     print("INVALID INPUT: Please enter a number between 1 and " + str(action_count))
        if action_choice == action_count + 1:
            action_result = give_hug(animal)
            
            # encounter_over = True
            # game_over = True
            # Execute Hug code
        elif action_choice == action_count + 2:
            print("Terrified of the vicious {}, you run. Barely escaping with your life".format(animal.name))
            input("\nPress enter to continue.\n")
            break
        else:
            action_result = take_action(animal.actions[action_choice-1], animal)
            
        
        if action_result == "animal runs" or action_result == "success":
            break
        elif action_result == 'win':
            game_won = True
            game_over = True
            break

        if encounter_counter > (round(random.random()*20) + 3):
            print_header(player)
            print("The {} has grown bored of your company. It chooses to move on to bigger and better things.\n".format(animal.name))
            press_enter()
            break

        if animal.friendship <= (-100 * player.level):
            print_header(player)



            print("Uh oh! Looks like you may have made an enemy. The {} attacks dealing you {} damage, before angrily storming away.\n".format(animal.name, animal.attack))
            print("The angered look in its eyes will live in your dreams forever.\n ")
            press_enter()

            if is_dead(player, animal):
                game_over = True
                break


        if is_dead(player, animal):
            game_over = True
            break


if game_won:
    print("Congratulations!!! Against all odds, you have managed to hug the dragon and come out alive. Truly, {}, you are a master of hugging! There is no more challenge left for you here.\n".format(player.name))
    press_enter()
    print("""

                                *
                               ***
                              *****
                             *******
                            *********
                           ***********
                          *************
        *************************************************
           *******************************************
               ************  Victory  ***********
                   **************************  
                     ***********************
                    ************ ************
                   **********       **********
                  ********             ********
                 ******                   ******
                ****                         ****
               **                               **
    
    """)

else:
    print("\n\n\n")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      Game Over      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
    press_enter()