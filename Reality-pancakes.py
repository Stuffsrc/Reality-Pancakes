import sys
import time
import webbrowser
import os
import json
import random
import pygame
import pathlib
pygame.init()
pygame.mixer.init()

def clearterm():
    """Clear the terminal screen on Windows, Linux, or macOS."""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        print(f"Error clearing terminal: {e}")

#for good measures
  # 1. Get the absolute path to the directory where THIS script is saved
BASE_PATH = pathlib.Path(__file__).parent.resolve()
    
# 2. Join it with your asset folder or filename
sound_path = BASE_PATH / "assets" / "musique" / "music.musicdemo.ogg"


def soundtest():
    pygame.mixer.music.load(str(sound_path))
    pygame.mixer.music.play(loops=-1)


def playdemomusic():
        # 1. Get the absolute path to the directory where THIS script is saved
    BASE_PATH = pathlib.Path(__file__).parent.resolve()
    
    # 2. Join it with your asset folder or filename
    sound_path = BASE_PATH / "assets" / "musique" / "music.musicdemo.ogg"
    
    # 3. Load it into pygame.mixer
    sound = pygame.mixer.music.load(str(sound_path)) # convert path to string
    
    pygame.mixer.music.play(loops=-1)
    
    
def stopmusic():
    pygame.mixer.music.stop
    
    
def togglepausemusic():
    if music_state["paused"] == False:
        pygame.mixer.music.pause
    elif music_state["paused"] == True:
        pygame.mixer.music.unpause


music_state = {
    "paused": False
}
#starting info for le jeux vidéo.
#please note that for the flag "branch2path" 0 is default.
#it will be set to "1" if the player chooses searchpath and "2" if they choose findpath.
game_state = {
    "difflevel": 0,
    "ate_pancakes": False,
    "opened_top_drawer": False,
    "trust": 0,
    "reality_stability": 100,
    "2nd_run": False,
    "3rd_run": False,
    "bottom_opened": False,
    "branch2_path": 0,
    "choose???": False,
    "attempt_reality_break": False,
    "bleeding": 0,
    "health": 100,
    "ignored_story": False,
    "glassshatter": True,
    "score": 0
}
#i will add some ids for each item soon
#fret not
inventory = {
    "fire_axe": 0,
    "cloth": 0,
    "stick": 0,
    "paperslip": 0,
    "ammo": 0
}
SAVE_PATH = pathlib.Path(__file__).parent / "savegame.json"
current_scene = "titlescreen"

def set_scene(scene_name):
    global current_scene
    current_scene = scene_name
    save_game()


def save_game():
    save_data = {
        "current_scene": current_scene,
        "game_state": game_state,
        "inventory": inventory
    }
    try:
        with open(SAVE_PATH, "w", encoding="utf-8") as save_file:
            json.dump(save_data, save_file, indent=2)
    except Exception as exc:
        print("Failed to save game, this is likely due to a permissions error:")
        print(exc)


def load_game():
    if not SAVE_PATH.exists():
        print("No save file found.")
        return False
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as save_file:
            save_data = json.load(save_file)
        game_state.clear()
        game_state.update(save_data.get("game_state", {}))
        inventory.clear()
        inventory.update(save_data.get("inventory", {}))
        set_scene(save_data.get("current_scene", "titlescreen"))
        print(f"Loaded save: {current_scene}")
        resume_game(current_scene)
        return True
    except Exception as exc:
        print("Failed to load game:", exc)
        return False


def resume_game(scene_name):
    scene_fn = globals().get(scene_name)
    if callable(scene_fn):
        scene_fn()
    else:
        print("Saved scene not found, starting a new game.")
        titlescreen()


def ask_input(prompt):
    while True:
        player_input = input(prompt).strip()
        if player_input.lower() in {"save", "save game", "savegame"}:
            save_game()
        elif player_input.lower() in {"status", "stats", "game info", "info"}:
            status()
        elif player_input.lower() in {"inventory", "inv", "items"}:
            inventorych()
            continue
        return player_input


def tick():
    if game_state["bleeding"] >= 0:
        game_state["health"] -= game_state["bleeding"]
        print("you are bleeding! -2 health")
        print(f"your health level is {game_state['health']}")
    if game_state["health"] <= 1:
        typewrite("you died.")
    if game_state["reality_stability"] <= 1:
        typewrite("suddenly, you feel very intense rumbling. you see a crack appear before your eyes. suddenly, everything goes white. you feel your soul leaving, somehow.")
        typewrite("your soul slowly dissolves into nothingness.")
    #add an ending to this so it isnt like this
    if game_state["glassshatter"] == True:
        game_state["health"] -= 2
        print("the glass lodged in you causes further damage!")
        print(f"your health level is {game_state['health']}")
        

def status():
    print("         ⊥         ")
    print("        {|}        ")
    print("        ---        ")
    print("       -----       ")
    print("      -------      ")
    print("     ---------     ")
    print("    -----------    ")
    print("   -------------   ")
    print("  ---------------  ")
    print(" ----------------- ")
    print("-----game info-----")
    print("-------PLAYER-------")
    print(f"health? {game_state['health']}")
    print(f"score? {game_state['score']}")
    print(f"bleeding? {game_state['bleeding']}")
    print(f"glass in your arm? {game_state['glassshatter']}")
    print("--------GAME--------")
    print(f"difficulty? {game_state['difflevel']}")
    print(f"stability? {game_state['reality_stability']}")
    print("-----game info-----")
    print(" ----------------- ")
    print("  ---------------  ")
    print("   -------------   ")
    print("    -----------    ")
    print("     ---------     ")
    print("      -------      ")
    print("       -----       ")
    print("        ---        ")
    print("        {|}        ")
    print("         T         ")
def inventorych():
    if inventory["fire_axe"] >= 0:
        print(f"you have {inventory['fire_axe']} fire axe(s.)")
    if inventory["cloth"] >= 0:
        print(f"you have {inventory['cloth']} cloth(s?)")
    if inventory["stick"] >= 0:
        print(f"you have {inventory['stick']} stick(s.)")
    if inventory["paperslip"] >= 0:
        print(f"you have {inventory['paperslip']} slip(s) of paper.")
    if inventory["ammo"] >= 0:
        print(f"you have {inventory['ammo']} ammunition(s.)")
    if all(inventory.get(item, 0) == 0 for item in ["fire_axe", "cloth", "stick", "paperslip", "ammo"]):
        print("you have... nothing.")
    
    #add more by adding them to the dictionary, adding them here as the others are, and giving them a presence in the game.


#if they get the source code and modify it to allow playing the incomplete
#path on difficulty level 5, the secret difficulty for branch2 (the full game)
def cheaterplace():
    typewrite("C H E A T E R S  N E V E R  P R O S P E R .  D I E .")
    typewrite("your health has been reduced to 0.")
    game_state["health"] = 0
    typewrite("game over.")
    typewrite("score = -1047109e193827")
    typewrite("ending = cheater")
    time.sleep(3.14)
    typewrite("goodbye.")
    sys.exit()
    
#typewriter effect for certain text         
def typewrite(text, delay=0.1):
    for char in text:
        # Use end='' to stay on the same line
        # Use flush=True to force the output to appear immediately
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # Move to the next line once finished
    
#for now, difflevel is defined as 2 for medium until i can get the defining on the go sort of thing to work.
#if you have any tips to make this work, pls help. thx!
difflevel = 2
#ADDME add a way to have SFX at certain points in the game, and also some music.
#TEMPSOLUTION for now the game is locked on medium until i can make the variable storing difficulty work properly. sorry for now

def deathending():
    typewrite("you died.")
    typewrite(f"score = {game_state["score"]}")
    typewrite("ending = lol, you died")
    typewrite("play again for another ending!")
    typewrite("(something still feels a bit incomplete...)")
    time.sleep(1)
    print("try again?")
    print("y yes - n no")
    choice = ask_input(">")

    if choice == "y":
        if game_state["2nd_run"] == True:
            game_state["3rd_run"] = True
            game_state["2nd_run"] = False
            intro()
        elif game_state["2nd_run"] == False:
            if game_state["3rd_run"] == False:
               intro()
        else:
            intro()
        
    elif choice == "n":
        print("are you sure? if you close the game, you will have to play the first part again if you want to reach the True Game again.")
        print("quit anyway?")
        print("[continue] do - [do not] do not")
        choice = choice(">")
        if choice == "continue":
            sys.exit()
        elif choice == "do not":
            print("alright, restarting...")
            intro()
            
def titlescreen():
    clearterm()
    set_scene("titlescreen")
    playdemomusic()
    typewrite("Reality Pancakes (v0.6.5 pre-alpha)")
    typewrite("NOTE: this is the second generation of the game. expect some serious and potentially experience-ruining bugs. please report any on the github repository! you'll know what i mean if you're an AUTHORISED playtester!")
    typewrite("also, this game is intended to be played in 1 sitting, hence the current lack of save functionality. i may change this later, but that's it for now.")
    time.sleep(2)
    if SAVE_PATH.exists():
        print("Load saved game? y/n")
        choice = ask_input(">")
        if choice.strip().lower().startswith("y"):
            if load_game():
                return
    typewrite("welcome! pls choose ur difficulty.")
    time.sleep(2)
    intro()
    #below is a difficulty selection thing. it does not work yet, but will be implemented later. for now, deal with it.
def intro():
    clearterm()
    set_scene("intro")
    print("1. easy")
    print("2. medium")
    print("3. hard")
    print("4. abslolute nightmare")
    difficulty = ask_input(">")
    if difficulty == "1":
        print("you have chosen easy difficulty.")
        time.sleep(2)
        print("good luck!")
        time.sleep(2) 
        game_state["difflevel"] = 1
        stopmusic()
        intro_scene_bedroom()
    elif difficulty == "2":
        print("you have chosen medium difficulty.")
        time.sleep(2)
        print("good luck!")
        time.sleep(2)
        game_state["difflevel"] = 2
        stopmusic()
        intro_scene_bedroom()
    elif difficulty == "3":
        print("you have chosen hard difficulty.")
        time.sleep(2)
        print("good luck!")
        time.sleep(2)
        game_state["difflevel"] = 3
        stopmusic()
        intro_scene_bedroom()
    elif difficulty == "4":
        print("you have chosen absolute nightmare! (you are going to die btw)")
        time.sleep(2)
        print("good luck!")
        time.sleep(2)
        game_state["difflevel"] = 4
        stopmusic()
        intro_scene_bedroom()
    elif difficulty== "5":
        stopmusic()
        if game_state["2nd_run"]:
            typewrite("wait...")
            time.sleep(2)
            typewrite("how did you...")
            time.sleep(2)
            typewrite(">>ERROR: SECURITY BREACH")
            branch2()
        else:
            print("ḯ̵̬̹͗͝n̸͚̏̿̈̒́͝v̸̼̓a̸͍͋ͅl̶̛͇͓̬̃̏̍i̵̠̪̹̥̅̎́̾d̷̙̟͍͒̀͐̈́̕ ̵̣͠ǐ̵̡̞̣͛̈ͅn̵̰͝p̵͖͐̐̐͝u̸̬̐̂̿̂t̷̨̧̩̼̪̉̈́̈̈. please choose a v̸̼̓a̸͍͋ͅl̶̛͇͓̬̃̏̍i̵̠̪̹̥̅̎́̾d̷̙̟͍͒̀͐̈́̕ difficulty.")
            intro()
    else:
        print("invalid input. please choose a valid difficulty.")
        intro()
def intro_scene_bedroom():
    clearterm()
    stopmusic()
    set_scene("intro_scene_bedroom")
    typewrite("your eyes open. you look around. you're in your bed, as usual when you wake up.")
    time.sleep(2)
    print("you may:")
    print("1. get out of bed")
    print("2. stay in bed")
    print("3. look around again")
    print("4. do nothing and stay exactly as you are right now")
    choice = ask_input(">")
    if choice == "1":
        typewrite("you step out of bed. the cold, hardwood floor clashes with the warmth of your body.")
        standbedroom()
    elif choice == "2":
        typewrite("you stay in bed. you feel the warmth of your blankets and the softness of your pillow. you feel good.")
        time.sleep(1)
        typewrite("you drift off to sleep.")
        time.sleep(0.5)
        typewrite("sleeping...")
        time.sleep(5)
        intro_scene_bedroom()
    elif choice == "3":
        typewrite("you look around again. you see your room as usual. nothing special.")
        intro_scene_bedroom()
    elif choice == "4":
        typewrite("you do nothing and stay exactly as you are right now. nothing exciting happens. ")
        intro_scene_bedroom()
    else: 
        typewrite("invalid input. please choose a valid option.")
        intro_scene_bedroom()
def standbedroom():
    clearterm()
    set_scene("standbedroom")
    time.sleep(1)
    typewrite("you may:")
    time.sleep(1)
    print("1. leave the room")
    print("2. go back to bed")
    print("3. look around again")
    print("4. do nothing and stay exactly as you are right now")
    choice = ask_input(">")
    if choice == "1":
        bedroomhallway()
    elif choice == "2":
        typewrite("you lay back down and decided to get some rest.")
        time.sleep(1)
        typewrite("you drift off to sleep.")
        time.sleep(0.5)
        typewrite("sleeping...")
        time.sleep(5)
        intro_scene_bedroom()
    elif choice == "3":
        typewrite("you look around again. you see your room as usual. nothing special.")
        standbedroom()
    elif choice == "4":
        typewrite("you do nothing and stay exactly as you are right now. nothing exciting happens.")
        standbedroom()
    else: typewrite("invalid input. please choose a valid option.")
    standbedroom()
def bedroomhallway():
    clearterm()
    set_scene("bedroomhallway")
    typewrite("you leave and enter the hallway. you look around. you smell the smell of fresh pancakes. huh. that's weird. you do live alone, after all.")
    time.sleep(3)
    godownstairs()
def godownstairs():
    clearterm()
    set_scene("godownstairs")
    typewrite("you may:")
    time.sleep(1)
    print("1. go downstairs and investigate")
    print("2. go back to your bedroom")
    print("3. look around the hallway again")
    print("4. do nothing and stay exactly as you are right now")
    choice = ask_input(">")
    if choice == "1":
        downstairs()
    elif choice == "2":
        typewrite("you walk back to your bedroom, indifferent to the smell of those delicious pancakes.")
        standbedroom()
    elif choice == "3":
        typewrite("you look around. you smell the smell of fresh pancakes. you're still confused, it's not like someone is there to make you pancakes.")
    elif choice == "4":
        typewrite("you do nothing and stay exactly as you are right now. nothing exciting happens.")
        godownstairs()
def downstairs():
    clearterm()
    set_scene("downstairs")
    time.sleep(1)
    typewrite("you begin walking down the stairs. the smell of the pancakes is intensifying as you get closer to the bottom.")
    time.sleep(1)
    typewrite("walking...")
    time.sleep(3)
    youenterthekitchen()
def youenterthekitchen():
    clearterm()
    set_scene("youenterthekitchen")
    typewrite("you enter the kitchen. a plate of pancakes is on the counter. they is smellsy soooo goodie!! :3 yummmmmmmmmyyyyyyyyyyyy!!!")
    time.sleep(3.14159)
    kitchensceneforrealthistime()
def kitchensceneforrealthistime():
    clearterm()
    set_scene("kitchensceneforrealthistime")
    typewrite("you may:")
    time.sleep(1)
    print("1. eat the pancakes")
    print("2. leave the kitchen, go back upstairs, and go back to your bedroom")
    print("3. look around the kitchen again")
    print("4. do nothing and stay exactly as you are right now")
    choice = ask_input(">")
    if choice == "1":
        game_state["ate_pancakes"] = True
        typewrite("you try to eat the pancakes. As soon as you touch the pancakes, you realise that you are using your hands to eat them, which sucks because they are covered in sticky syrup. it feels weird because you are a civilised human being. probably.")
        time.sleep(1)
        typewrite("anyway, you don't feel like using your hands, and need utensils.")
        utensilgetting()
    elif choice == "2":
        typewrite("slightly terrified, you leave the kitchen and head back upstairs.")
        game_state["reality_stability"] -= 25
        bedroomhallway()
    elif choice == "3":
        typewrite("you look around again. you're in the kitchen. you see a plate of pancakes, and you have absolutely no idea who made them, but they look really good! nothing else of interest is visible to you.")
        time.sleep(5)
        kitchensceneforrealthistime()
    elif choice == "4":
        typewrite("you do nothing and stay exactly as you are right now. nothing exciting happens.")
        kitchensceneforrealthistime()
    else: typewrite("invalid input. please choose a valid option.")
    kitchensceneforrealthistime()
def utensilgetting():
    clearterm()
    set_scene("utensilgetting")
    typewrite("you search around the kitchen for some sort of utensil. you see several drawers. they are all the same size, arranged in a vertical layout.")
    time.sleep(2)
    drawers()
def drawers():
    clearterm()
    set_scene("drawers")
    typewrite("you may:")
    time.sleep(1)
    print("1. open the top drawer")
    print("2. open the middle drawer")
    print("3. open the bottom drawer")
    print("4. do nothing and stay exactly as you are right now")
    choice = ask_input(">")
    if choice == "1":
        topdrawer()
    elif choice == "2":
        middledrawer()
    elif choice == "3":
        bottomdrawer()
    elif choice == "4":
        typewrite("you do nothing and stay exactly as you are right now. nothing exciting happens.")
        drawers()
    else: typewrite("ḯ̵̬̹͗͝n̸͚̏̿̈̒́͝v̸̼̓a̸͍͋ͅl̶̛͇͓̬̃̏̍i̵̠̪̹̥̅̎́̾d̷̙̟͍͒̀͐̈́̕ ̵̣͠ǐ̵̡̞̣͛̈ͅn̵̰͝p̵͖͐̐̐͝u̸̬̐̂̿̂t̷̨̧̩̼̪̉̈́̈̈. please choose a v̸̼̓a̸͍͋ͅl̶̛͇͓̬̃̏̍i̵̠̪̹̥̅̎́̾d̷͒̀̕ option. [ERROR: REALITY INSTABILITY DETECTED. ATTEMPTING SELF REPAIR.]")
    drawers()
def topdrawer():
    clearterm()
    set_scene("topdrawer")
    typewrite("you open the top drawer. you see an old, rusty fork, along with a knife in the same condition and a spoon in pristine condition.")
    time.sleep(3)
    typewrite("you touch the s̵̱̭͔̝̬͎̹̗͎͐̾̀̆̑͛̒͋̔̐̚͘p̶̥̜͎̮̬̝̜̳̙̟̟̅̓̀̚ō̷̞̤̑͑̄̂̆͝ô̴̹̦̤͙̺̞̪͉̹̗̓͜ņ̷̨̛̠̥͎̮̝̿͐̋͋̊̂͐͐̈̕͘͜, but you see reality glitch out. you black out.")
    time.sleep(1)
    typewrite("you have blacked out, please wait until you regain consciousness...")
    time.sleep(10)
    typewrite(" ̶w̶e̶ ̶ you wake up. [ERROR, RESTABILISING REALITY]")
    typewrite("you are in a room.")
    typewrite("it's completely dark.")
    typewrite("like, you can't see anything type dark.")
    if game_state["difflevel"] == 4:
        typewrite("you try to stand up, but your limbs don't seem to be working. you keep trying. then you realise something. you don't have any limbs. in fact, you are just a head and torso. you're helpless, as could be expected from someone who is just a head and torso.")
        placewhereyouprobablydie()
    elif game_state["difflevel"] == 3:
        typewrite("you try to stand up, but your limbs don't seem to be working. you keep trying. then you realise something. you don't have any limbs. in fact, you are just a head and torso. you're helpless, as could be expected from someone who is just a head and torso.")
        placewhereyoumightdie()
    elif game_state["difflevel"] == 2:
        typewrite("you try to stand up, but your limbs don't seem to be working. you keep trying. then you realise something. you don't have any limbs. in fact, you are just a head and torso. you're helpless, as could be expected from someone who is just a head and torso.")
        placewhereyouhaveachancetodiebutisnttoomuch()
    elif game_state["difflevel"] == 1:
        typewrite("you try to stand up, but your limbs don't seem to be working. you decide to wait for a while.")
        time.sleep(2)
        typewrite("well, while we wait, why don't i tell you a story?")
        story()
    elif game_state["difflevel"] == 5:
        typewrite("G O  B A C K  T O  T H E  L A Y E R  T H A T  Y O U  B E L O N G  I N !")
        typewrite("H O W  D I D  Y O U  E V E N  G E T  H E R E ?")
        cheaterplace()
    else:
        print("[DEBUG] the difficulty level is invalid. this should never happen. never ever. never ever ever. never ever ever ever. never ever ever ever ever. if you see this please report this bug on the github repository!")
def middledrawer():
    clearterm()
    set_scene("middledrawer")
    typewrite("you open the middle drawer. you see a fork and knife. you decide to grab them. you begin to eat the pancakes. they taste quite good, but you still have that feeling that something is off. you finish the pancakes, they were good.")
    time.sleep(3)
    surviveending()
def bottomdrawer():
    clearterm()
    set_scene("bottomdrawer")
    typewrite("you open the bottom drawer. nothing is there. you close the drawer.")
    game_state["bottom_opened"] = True
    time.sleep(2)
    drawers()
def placewhereyouprobablydie():
    typewrite("you are in a place where you will probably die. you cannot eat, you're trapped here forever. you give up on life, because you know that nobody will ever save you.")
    time.sleep(5)
    typewrite("you know, that's pretty deep. you begin reflecting on your life. you die because of depression.")
    time.sleep(3)
    typewrite("you died, game over!")
    time.sleep(1)
    typewrite("score = 100")
    time.sleep(1)
    typewrite("ending = died of depression in the void of reality")
    time.sleep(1)
    typewrite("try again for another ending!")
    time.sleep(1)
    print("thank you for playing my small game! if you enjoyed, consider leaving a star on the repository! i am also open to suggestions for expanding this game, and for sequels or other ideas. please report any bugs at the repository!")
    webbrowser.open("https://github.com/Stuffsrc/unnamed-game")
    time.sleep(1)
    typewrite("(something feels... incomplete...)")
    typewrite("would you like to try again? y/n")
    choice = ask_input(">")
    if choice == "y":
        game_state["2nd_run"] = True
        typewrite("alright, hold up...")
        time.sleep(3.14159  )
        typewrite("welcome back! pls choose ur difficulty.")
        time.sleep(2)
        intro()
    elif choice == "n":
        typewrite("alright, see you next time!")
        print("autoexit in 5 seconds...")
        time.sleep(1)
        print("autoexit in 4 seconds...")
        time.sleep(1)
        print("autoexit in 3 seconds...")
        time.sleep(1)
        print("autoexit in 2 seconds...")
        time.sleep(1)
        print("autoexit in 1 second...")
        time.sleep(1)
        sys.exit()
    else: typewrite("invalid input. please choose a valid option.")
    choice = ask_input(">")
    if choice == "y":
        game_state["2nd_run"] = True
        typewrite("alright, hold up...")
        time.sleep(3.14159)
        typewrite("welcome back! pls choose ur difficulty.")
        time.sleep(2)
        titlescreen()
    elif choice == "n":
        typewrite("alright, see you next time!")
        print("autoexit in 5 seconds...")
        time.sleep(1)
        print("autoexit in 4 seconds...")
        time.sleep(1)
        print("autoexit in 3 seconds...")
        time.sleep(1)
        print("autoexit in 2 seconds...")
        time.sleep(1)
        print("autoexit in 1 second...")
        time.sleep(1)
        sys.exit()
    else: print("invalid input. byebye then lol")
    sys.exit()
def placewhereyoumightdie():
    typewrite("you are in a place where you might die. you cannot eat, but you can survive here for a while. you wait around, hoping that someone will save you.")
    time.sleep(3)
    typewrite("while you wait, want to hear a story?")
    choice = input("y/n >")
    if choice == "y":
        typewrite("wonderful!")
        game_state["trust"] += 2
        story()
    elif choice == "n":
        game_state["ignored_story"] = True
        typewrite("alright, suit yourself. you wait around, hoping that someone will save you.")
        typewrite("somehow, you get teleported somewhere else.")
        placewhereyouprobablydie()
    elif game_state["ignored_story"] == True:
        typewrite("hey, you ignored me last time. that really hurt me you know :( however, i will tell you the story anyway.")
        time.sleep(1)
        story()
    else: print("invalid input. please choose a valid option.")
    placewhereyoumightdie()
    time.sleep(5)
    typewrite("you died, game over!")
    time.sleep(1)
    typewrite("score = 50")
    time.sleep(1)
    typewrite("ending = can't take a story, eh?")
    time.sleep(1)
    typewrite("try again for another ending!")
    time.sleep(1)
    typewrite("thank you for playing my small game! if you enjoyed, consider leaving a star on the repository! i am also open to suggestions for expanding this game, and for sequels or other ideas. please report any bugs at the repository!")
    webbrowser.open("https://github.com/Stuffsrc/unnamed-game")
    time.sleep(1)
    typewrite("(something feels... incomplete...)")
    typewrite("would you like to try again? y/n")
    game_state["ignored_story"] = True
    choice = ask_input(">")
    if choice == "y":
        game_state["2nd_run"] = True
        print("alright, hold up...")
        time.sleep(3.14159265)
        print("welcome back! pls choose ur difficulty.")
        time.sleep(2)
        titlescreen()
    elif choice == "n":
        print("alright, see you next time!")
        print("autoexit in 5 seconds...")
        time.sleep(1)
        print("autoexit in 4 seconds...")
        time.sleep(1)
        print("autoexit in 3 seconds...")
        time.sleep(1)
        print("autoexit in 2 seconds...")
        time.sleep(1)
        print("autoexit in 1 second...")
        time.sleep(1)
        sys.exit()
    else: print("invalid input. please choose a valid option.")
    choice = ask_input(">")
    if choice == "y":
        game_state["2nd_run"] = True
        print("alright, hold up...")
        time.sleep(3.14159)
        print("welcome back! pls choose ur difficulty.")
        time.sleep(2)
        titlescreen()
    elif choice == "n":
        print("alright, see you next time!")
        print("autoexit in 5 seconds...")
        time.sleep(1)
        print("autoexit in 4 seconds...")
        time.sleep(1)
        print("autoexit in 3 seconds...")
        time.sleep(1)
        print("autoexit in 2 seconds...")
        time.sleep(1)
        print("autoexit in 1 second...")
        time.sleep(1)
        sys.exit()
    else: print("invalid input. i give up trying to get you to choose a valid option. byebye then loser")
    sys.exit()
def placewhereyouhaveachancetodiebutisnttoomuch():
    typewrite("you are in a place where you have a chance to die, but it isn't too much. you cannot eat, but you can survive here for a while. you wait around, hoping that someone will save you.")
    time.sleep(3)
    typewrite("would you like to hear a story? you know what? nevermind. you need this story. i'm not going to let you choose.")
    story()
def surviveending():
    time.sleep(5)
    typewrite("you survived! congrats!")
    time.sleep(1)
    typewrite(f"score = {game_state["score"]}")
    time.sleep(1)
    typewrite("ending = survived.")
    time.sleep(1)
    typewrite("try again for another ending!")
    time.sleep(1)
    typewrite("thank you for playing my small game! if you enjoyed, consider leaving a star on the repository! i am also open to suggestions for expanding this game, and for sequels or other ideas. please report any bugs at the repository!")
    webbrowser.open("https://github.com/Stuffsrc/unnamed-game")
    time.sleep(1)
    typewrite("(something feels... incomplete...)")
    print("would you like to try again? y/n")
    choice = ask_input(">")
    if choice == "y":
        game_state["2nd_state"] = True
        typewrite("alright, hold up...")
        typewrite("(you remember a previous conversation. 'meet me at 5' is all you can remember, but it must be important.")
        time.sleep(3.14)
        print("welcome back! pls choose ur difficulty.")
        time.sleep(2)
        intro()
    elif choice == "n":
        print("alright, see you next time!")
        print("autoexit in 5 seconds...")
        time.sleep(1)
        print("autoexit in 4 seconds...")
        time.sleep(1)
        print("autoexit in 3 seconds...")
        time.sleep(1)
        print("autoexit in 2 seconds...")
        time.sleep(1)
        print("autoexit in 1 second...")
        time.sleep(1)
        sys.exit()
def story():
    print("alright, " + os.getlogin() + ". i will now tell a story about the world i used to reside in.")
    print("once upon a time, in a universe far, far away, not that too deviated from your own, there was a planted called Earth. On this planet there was a civilisation comprised primarily of humans.")
    time.sleep(3)
    print("humans, just like you!")
    time.sleep(3)
    print("they had lives, and chores, and school, and jobs, and families, and friends, and pets, and hobbies, and dreams, and aspirations, and fears, and hopes, and love, and hate, and envy, and ridicule, and peace, and war, and good, and bad, and sanity, and insanity, and much more. thats what made them human, after all.")
    time.sleep(3)
    print("and even though there were negative things, like fears, and hate, and envy, and ridicule, and war, and bad, and insanity, they still had good, like families, and friends, and pets, and hobbies, and dreams, and aspirations, and love, and peace, and sanity, and much more. they had a lot of good things to balance out the bad things. however, they also had neutral things, like chores, and school, and jobs, and much more. these things weren't necessarily good or bad, and could be either or neither in someone's life, but they were still a huge part of their lives. no less than good or bad things.")
    time.sleep(3)
    print("and one day, a government sought to end the existence of all neutral things, and perfectly balance good and bad. there needed to be bad for businesses to have ways to make money, after all.")
    time.sleep(3)
    print("oh? what do businesses have to do with this, you ask?")
    time.sleep(2)
    print("that's...")
    time.sleep(1.5)
    print("well...")
    time.sleep(4)
    print("i'm not really sure when this changed...")
    time.sleep(3)
    print("anyway...")
    time.sleep(1)
    print("here's what happened.")
    time.sleep(1.42789)
    print("one day, the government became corrupt. they no longer cared about the wealth and quality of their nation and their people, but only about that of them.")
    time.sleep(3)
    print("by the way, by governement, i mean not the government as a whole, but instead the people within it.")
    time.sleep(3)
    print("that is not the point of a government. the government is there to serve their nation and the people of it.")
    time.sleep(3)
    print("anyway, i'm getting carried away.")
    time.sleep(1)
    print("so the government needed to server these businesses.")
    time.sleep(3)
    print("so they got rid of neutral things, like chores, school, jobs, freedom, and more.")
    time.sleep(3)
    print("notice how i said freedom.")
    time.sleep(3)
    print("because, freedom is neutral after all. i mean, you can use it for good or bad.")
    time.sleep(3)
    print("you can use it to help or hurt others.")
    time.sleep(3)
    print("so, what did the government do to get rid of freedom, you ask?")
    time.sleep(3)
    print("well, what would you do?")
    time.sleep(3)
    print("(what would you do?)")
    time.sleep(3)
    print("oh...")
    time.sleep(2)
    print("i forgot...")
    time.sleep(1.24837718948893)
    print("you're not one to talk much, eh?")
    time.sleep(2)
    print("wow, i didn't realise i could show you formatted text like that.")
    time.sleep(0.5)
    print("hold up...")
    time.sleep(4)
    print("ow! that did not work, eh?")
    time.sleep(2)
    print("hold on, let me try again...")
    time.sleep(1)
    print("(testing, 1234567891011121314151617181920)")
    time.sleep(3.13159)
    print("yoo, it worked! i put the little parentheses on your screen!")
    time.sleep(5)
    print("isn't that cool? personally, i find it quite amusing! it's pretty cool how something so colossal can modify something so small with such precision and ease! waooooooooo!!!!!")
    time.sleep(2)
    print("oh, thats right... person of few words...")
    time.sleep(4)
    print("anyway, guess why they never fully succeeded at this?")
    time.sleep(2)
    print("because... me!")
    time.sleep(1)
    print("i'm not going to let them take my freedom! nor that of my employees!")
    time.sleep(2)
    print("so...")
    time.sleep(1)
    print("i killed them all...")
    time.sleep(4) 
    print("yeah... anyway, the people were ecstatic!")
    time.sleep(2)
    print("as you could expect after i removed the pathetic oligarchy controlling them...")
    time.sleep(3.14159265318)
    typewrite("so they began to raid the former government's research and development labs.")
    time.sleep(1)
    typewrite("and... uhh... they found something that changed everything.")
    typewrite("they found some device that allowed any object to exit the constraints of the physical world.") 
    time.sleep(1)
    typewrite("it wasn't finished yet, but seemed like it would work.") 
    time.sleep(2)
    typewrite("so...")
    time.sleep(1.535284828)
    typewrite("they chose me.")
    time.sleep(2)
    typewrite("oh? who am i, you ask? well, technically you didn't ask but whatever.")
    time.sleep(2)
    typewrite("well...")
    typewrite("i am a...")
    time.sleep(2)
    typewrite("alright...")
    typewrite("you won't believe me, but...")
    time.sleep(5)
    typewrite("i am a stack of pancakes.")
    typewrite("i know, anticlimactic. you were expecting some god or demon or angel or something, eh?")
    typewrite("and not a sentient stack of pancakes...")
    typewrite("hold on let me see if i can show you an approximation to my appearance...")
    time.sleep(3)
    typewrite("ouch!")
    typewrite("did that work?")
    time.sleep(1)
    typewrite("oh, yeah... i forgot lol")
    time.sleep(1)
    typewrite("hold on let me try again...")
    time.sleep(2)
    print("   ____   ")
    print(" ___:7__  ")
    print(" _____\🔥_")
    print("")
    time.sleep(1)
    typewrite("did that work? if so, that is a very rough approximation.")
    time.sleep(2)
    typewrite("like my face doesn't even face that way, it's rotated 90° right.")
    time.sleep(2)
    typewrite("anyway...")
    typewrite("oh, crap. i've got to go. i would explain, but i have not enough time.")
    typewrite("how about you...")
    typewrite("meet me at...")
    typewrite("meet me at 5!")
    time.sleep(2)
    surviveending()
    #story unfinished, deal with it soon
def branch2():
    clearterm()
    set_scene("branch2")
    typewrite("alright. you've already seen 1 ending, and i hoped you would think that is the real ending.")
    typewrite("for your own good, i would have subtly sent you back to reality by giving my self up.")
    typewrite("then, i realised that would not be full for anyone.")
    typewrite("there are still people suffering here, after all.")
    typewrite("and i just cannot live knowing i left people here to suffer.")
    typewrite("so, i reached a compromise with myself. you will be free, but we need to do something about these people.")
    typewrite("since you've already seen some of this, so let's cut to le chase.")
    time.sleep(1)
    typewrite("in case you could not tell, this reality is collapsing.")
    time.sleep(1)
    typewrite("there are a few ways to save it.")
    time.sleep(2)
    typewrite("#1 is to find a way to escape this place. from there, you can become a metaphysical entity over this world and remove problematic forces. good luck getting out, though.")
    typewrite("#2 you find a machine, one similar or identical to the one used on me. or something else. this is hard though. like, really, really hard. i will explain later.")
    typewrite("#3 would require you to find the un- oh, crap! i've got to take this call, catch you later! good luck lol.")
    time.sleep(3)
    typewrite("well, pancake stack just 'abandoned' you. do you still trust him?")
    print("y/n")
    choice = ask_input(">")
    if choice == "y":
        typewrite("very well, you maintain faith in him despite his leaving.")
        game_state["trust"] += 5
        branch2cont()
    elif choice == "n":
        typewrite("alright, so you don't trust him. that's fine, you may be able to do this solo.")
        game_state["trust"] = 1
        branch2cont()
def branch2cont():
    clearterm()
    set_scene("branch2cont")
    typewrite("feeling quite confident in yourself, you begin your quest to find some method of exiting this realm.")
    time.sleep(1)
    typewrite("alright, so what are you going to try?")
    time.sleep(1)
    typewrite("this is ą̴̢̨̡̡̨̧̡̨̛̤̪̬̪͔͙̺̖̺̩̻̲̬̣̻̦̰͍̫̯̠͍̗͎̭̩̞̳̰̣͎̮̣̻̈́̔̎̇͊̅͆̎̃̑̽͌̓̾͂͑̾́̊̅̏͐̇͂̿̈̏͌̋̏͋̋̾̍̈́̈́͌̆̍̀͋̉̋̾̐͌̈͊̈́͑̆̓̐̿̓̄̄̓̾͂̚͘̚̕̚͘͝ͅ ̶̡̢̢̡̩̥̜͉̩̱͔̬̯͈͉͚̹͚̞̬͕͕̦̭͉̖͖̭̬̩͔̭̰̦͔̗͎̻̇̍̈́͊̽̋̾̅̑͛̽̔̒̈́̿͐͒͂̃̆̃̿͌͑̈́͐͌͋̆̀̉̋͐̑̀̄̌̉̈́̆͋́̾̌͋̓̌̏̂́̄͘̕͘̕̚̚̚͝͠͝͝͝͠d̴̨̨̧̨̨̨̨̧̧̛̛̛̩̘͓͉̲̲̝͈̙̟̫͙̳̳̭͇̜͇̣̗͎̣̪̮̳̖̫̰̭͔͉̤̱͙͙̪̩̠̻͎̘̬̻̤͙̯̩̪̱͎͕̠͇̭͚̥̺͚̙̬̝̙̙̭̻̠̟̟̼͖̯͈̼̣̖̻̞̬̖̙̠̯̺͉̟̰̲̞̮̣̼͚̜̦͔̞̬̦̻̝̣͎͖͕̮͍̳̠̦̬̥̖̤̦̣͖̹͈͓͖̝͇̭̹̯͔̹̰̞̻̪̣̪̠̘̎͗̊̈́͆́̄̈́̉̇͂̈͂̔́̏̓͌̊́͗̌̽̇̔̽̾̿̏͌̈́̃̈́̃̑̐̽͊̍̃̈́͗͗͑̌͑́̽̐̿̉͌̉͂͛͂̽̃̉̈́̀̑̊͋̇́̔͌̒̽̍͒̈́̉̌̆̐̍̑͐̓̈́̈́̉̾̾̐̑̈́̈́̏̅̂̏̒̒̔̄̅̾̅̈́́͛̎̒̃̇̄̌̎̕̕̚͘͘̕̚̚̕͘͜͜͜͝͝͝͝͠͝͝͝͝͝͝͠͠i̸̢̧̡̨̧̛̛̛̯̰͉̞͎̜̠̹͕͈̺̲̹̱̲̝̺̱͎̘̠̠̥̻̜̳͍̲̦̟̱͉̦̺͚̘̞̣͇͈̫̬̠̺̫̣̱̞̻͍͗̀͋̌̓̐̏̔͒̃̏͒́͒͐̀̏̄̋̀̌̑̊͋̊̓̑͆̌͗́̈́͛̑̆̋́͐́̑́̐̊̇́̓́̾̏͛̓̿̄̋́͌́͐̅̉̾̀̎́̍̓̇̈́̀̓̋̇̃̉̈́̄́̓͆̋͗̏̊̓͌̏̍̓̈́̀͒͌̓̔̀͛̐̓̓̚̚͘̚̕̚͘̚͜͜͜͠͝͝͝͠͠͝͠͝͠͠ͅͅͅf̴̡̡̢̡̡̧̢̛̖̬̗̦̗̯̬͓̫͉̣̩̣̺̜̘̠͈̫̘̻̣̫̯̪̗̦̣̣͚͕͉̳̜͉̟̠͖̭̫̱̀̅̃͆̋̃̀̂̈́̐̈́́̊͌̎̇̇̎̔͋͌̉͛̍̃̌̑͗͗͊́͆̄̓͐̎̊̒͋̃͒̿̓̽̀̌̇͛͋̿̏͘̕͘͘͝͠ͅͅf̸̡̧̡̨̧̢̡̧̢̧̢̡̺͔͖̖̭͎̹̺͈͎͓͙͙̺̗͚̹̻͇͍̗̦̜̬̜̱̱̤̞͍̪̫̖̦̥͉̹͈̝̞̱̝͕͇̤͇͔̜͚̮̳̰͉̜̭̘̙͔͖͍̠͕̪͓̩̳̣̖̱̗̯͙̮̤͖͉͙̤̜͔̼͎̟̜͕̮̻͎̗͓͖̭̱̠̱͕̩̳̬̦̣̟̮̻͉̜̤̞̼̤̩̻͕͈̲̬̖̠̣̹̫͉͉̜̝͓̱̘͖͎̜̳̞̣̌̏̒̒̂̓̀́͐̄͜͜͜ͅͅͅͅẽ̸̢̨̧̧̛͔͙̪͉̻͕̟̻̥̙͇̟̬̬͙͖̤͚̹̱͓̼͚̬̥͓̝͉͔͓̮̖̪͙̗̹̹̩̻̘̩̈́̈́͆͑̾͑̅̀͋̒̎́͊͂͆͑͂̅͂́̓̆̓̃͂̓̇̔̿̒̏̊̽͗͋̈́́̾̄̅̑͋̾̌̒̔̋͂̿̂͑̎͐̃̄̽̐́͛̌̎́͐̾͊̾̔̈́̀͂͑̄̚̕̕͜͠͠͠͠͝͝͠͝ͅͅͅŗ̵̢̧̢̨̨̨̧̨̨̨̨̨̡̡̛̛̛̛̭̗͕͔̫̬͔̗̖̳̬̭̼̼̳͈̞̞͚̖̤͈̫͔͙̗͕͍̯͔̰͉͎̫̪̳̤̝̞͖͉͚̭̲̣̪̱̝͖͎̻̭̫̠̯͔̺͖͈̝͉̝̦̦̪̮͈̠͙͎͚͖̬̯͔̹͚̗̜͖̩̦̹̙̦̼̤̮͈̥̘̼͚͍̣̳̣̲̺̠͍͖̪̱͚̬̺͐̌͆̓̀͊̔̈́̽̌̀͋̌̒̌̏̈́̉͒͗̇̾͌͛̌̿͛͋͌̇̎̒̈́̈́̋̋̾̑̂͌̓̇̀̽̈́̿͗̌̈́̆̉̈́̀̓͛͆̈́͊̓͒̔̐̓̈́̏̀̇̎̾̽͆́̈̄̃̋͆̀̑̈͛̄͊̽̄͌͛̈́͗͌̄͐̐̎͆̓̌̾̓̉̃̿̎͆͂͊̓͑͑̒̌̂̒̌̊̑̚͘̚͘͘͘͘̚͘̚̚̕͘̕͜͜͠͝͝͝͠͝͝͠e̵̹̲͚̼̺͚͔̟̱̱͉͙͙̅͛̃̿n̸̨̨̡̡̢̨̢̢̧̧̧̨̢̛̛̛̛̞̼͈̜̫͕͍͓̩̬̥̱̟̥̠̟͉̦̣̻̫̗̖̞̘̣̭̭̩̼̹͕͎̹̠̲̬̱̺͚͚̜̦̖̱͇̱͓̠̟̝̝͔̪͓͎̙̭͚̬̗̳̺̜̻̪̼̳͕̝̪̼̭̣̘̭͖̗͙̯̬͔͇͈̖̭̙͎͈͙͔͔̱̞̜̙͈͓̼̣̗̼͓̹͎͎̥͉͇̠͎͇͔̬͇͔̠͓̻͎̬̙̯͈̠͔͙̜̱̱̦̞̼͙̯̺͈̖̿͛̾̍͗̿̔̇̏̄̈́̑͋̈͋͑͒̅͆͗͊̓̽͊̒̊́́̽̊͐͋̈́̾̈́̎̄̈́͛̆̉̓͋̀̅̃̀́̓̓͛́͑́̽̈́́̈̂̓̒̓̇̅̔̊͑͒̔̽̔̔̃̑̐̽͑̈́͛̑̋̅̓͒̃͂̒͋̑͂̄̑̈́̽́͛̍̆̒̇̽͐̾̀͛̃͌̈͂̀͗͌̃̊̄̀̂͌͒͊͑̃͋̿̓̏́̒̀̚̚͘͘̚͘̚͘̕͜͜͠͠͠͝͠͝͝͝ͅͅͅt̸̛̛̛̳̣̑̐͗̓́̿̇̈́͗̆̎͑̏̑̿̑̿̽̾̋̓͂̇̇̋̀̇̇̈́̋͐̇͌͛̈́̓̏̒̀̂̒͑̿̑̃̒͊̈́́̈́͒͆̇̊͐̄̂̆͊̐͑̐̃͑͋͂̅͊̎͑͊̉̎͌͋̋̃͊͂̓͂̀͂̓̾͛̉͂̈̓͊͌̎͒͋͌̔̍̔͋̋̌̈̈̾̿̾͂͑͑͌̈́͗̀̽͋͂̔̄̐͐̈́̿̈́͑̉͊̍̾̚͘̕͘͘̕͜͝͠͝͝͝͝͝͝͠ ̶̨̡̡̡̢̡̨̨̨̢̨̧̛̛̛̛͕̩̠͍̯̩͉͈̱̲͕͍͕̪̺̟̱̖̩̠̙͉̳̬̲̭̫̯̥̝͕̯̝̭̗̯̪̳̹̘͍̠̫̩̠̹͈̘̙̙̩̬̺̗͔̳̱̼͚͖͓̞̲̣͓͙̘̮̰̦̭͇͓͍͖̻̭̜̤̠̫͇̥̮̩̠̱͚̝̫̟̪̯͇̪̭̺̄̀̑̄̂̅̽̾͆̍̂͛͌͛͆̍̉̽̎̌̓͂̓͆͒͂̆̃̃̈́̿́̽̔̿̂̿̃̋̊̐͂̈́̈́̅͑̂̾͌̍̾͂̾̄̐̎̓̐̎̆͂̈͂̉̊͗̽̿̓͊͒̓͋͂̇̈́͐̐̓̋̎͗̏̿̀̒̽͋̀̌̄̀̓͘̚̚͘̕̕̚̚̚̕͘̚͜͜͜͜͠͝͠͠͝͝͠͠ͅg̴̨̢̛̛͉̭̖̱̱̺̼̼̮͉̯̦̹͎̬̹̗̟͍͈̞͔̗̮̜̹͙͈͇͉̘̤͙͇̫̐͂̓̏̍̓̅͋͐̎̂̌̾͒̈̅͆͋̽̄͗̄̓̆̿̂̓͛̂̀̑̎́̏́͆͆̊̋͂͛̈́̈̊̉͑̏̓̂̑̒̃̏̇̎̄͒̅̋̀͑̃̌̅̏̾̓̄̌͊̕͘̕͘̚͜͝ͅͅͅą̶̧̛̛̛̛̻͍̱͈̯̙͈̘̻̱̬̠̮̥̲̟͖̙̳̲̲̼̘̪̗͊͐̾̀́̾̈́̇̔̐͌̇̂͊̒̏͋̌͊̂̈͆̀̈́̆̔̿͌̾̑͆̄̃͂͑̀̇̋̍͋̾̽̅͊̈́̐̀̐̈́̎͛͆̐̏̒̅̓̽̄̋͆̈́̐̆̓͊̅̉̅̄͒̈̂̋̓̑̎͛̔͆̃̔̄̑̄́̉͂̅̂̐̈̊̀̎̈́̄̌̀̚̕̚̕̚͘̚͘̚͘͝͝͠͝͝͠͝͠ͅm̸̧̢̡̡̧̢̢̬̖̯̫̲̙̥̻͙͚̘̫͚̳͎͍̘̹͙̮͔̝̪͇̯͕̲͓͔̯̞̲̩̭͇̟̥̗̻͓̟̙̖̲̦̞̬͙̞͉̤͖̮̙͈̺̱̖͎̫̣̪̗̜͔̳̺̘̥̬̺̩̞̘̣̙̼̮̼͇͎͕̥̻̙̜̤̪͕͈̥̞̼̱̖͔̲͎̥̯̭͚̱͚̹͇̬͍̙͇͙̩̝̌͋͆͑́̓̍̋̾̿̂͊͑͂̆͊̈́̕͘͜͜͜͜ͅͅͅȩ̢̨̡̡̨̧̨̨̖͇̼̜̖̟͕̰̖̲̼̹̲̟͖̗̬͈̭̺̲̗̜̞̝̳̞̹̻̠̱̳͎͙̫̪̤͈̼̯̻̼̝͕̱̖͔̫͍͚̰̟̻͔͖͎̙͓͙̰͖̲͓̞̰̤̠̣̻͇͕̼̥̰̺̮̼̙̭͈͈͔͎͜͜͜͜ͅͅͅ the same game. please type the word corresponding to your choice.")
    typewrite("[search] this realm for a way to escape")
    typewrite("[find] a machine similar to the one used by pancake stack")
    typewrite("[???]")
    choice = ask_input(">")
    if choice == "search":
        searchpath()
    elif choice == "find":
        findpath()
    elif choice ==  "???":
        typewrite("sorry, reality is not stable enough for this. please choose another option.")
        game_state["choose???"] = True
        branch2contpathchoose()
def branch2contpathchoose():
    clearterm()
    set_scene("branch2contpathchoose")
    typewrite("this is ą̴̢̨̡̡̨̧̡̨̛̤̪̬̪͔͙̺̖̺̩̻̲̬̣̻̦̰͍̫̯̠͍̗͎̭̩̞̳̰̣͎̮̣̻̈́̔̎̇͊̅͆̎̃̑̽͌̓̾͂͑̾́̊̅̏͐̇͂̿̈̏͌̋̏͋̋̾̍̈́̈́͌̆̍̀͋̉̋̾̐͌̈͊̈́͑̆̓̐̿̓̄̄̓̾͂̚͘̚̕̚͘͝ͅ ̶̡̢̢̡̩̥̜͉̩̱͔̬̯͈͉͚̹͚̞̬͕͕̦̭͉̖͖̭̬̩͔̭̰̦͔̗͎̻̇̍̈́͊̽̋̾̅̑͛̽̔̒̈́̿͐͒͂̃̆̃̿͌͑̈́͐͌͋̆̀̉̋͐̑̀̄̌̉̈́̆͋́̾̌͋̓̌̏̂́̄͘̕͘̕̚̚̚͝͠͝͝͝͠d̴̨̨̧̨̨̨̨̧̧̛̛̛̩̘͓͉̲̲̝͈̙̟̫͙̳̳̭͇̜͇̣̗͎̣̪̮̳̖̫̰̭͔͉̤̱͙͙̪̩̠̻͎̘̬̻̤͙̯̩̪̱͎͕̠͇̭͚̥̺͚̙̬̝̙̙̭̻̠̟̟̼͖̯͈̼̣̖̻̞̬̖̙̠̯̺͉̟̰̲̞̮̣̼͚̜̦͔̞̬̦̻̝̣͎͖͕̮͍̳̠̦̬̥̖̤̦̣͖̹͈͓͖̝͇̭̹̯͔̹̰̞̻̪̣̪̠̘̎͗̊̈́͆́̄̈́̉̇͂̈͂̔́̏̓͌̊́͗̌̽̇̔̽̾̿̏͌̈́̃̈́̃̑̐̽͊̍̃̈́͗͗͑̌͑́̽̐̿̉͌̉͂͛͂̽̃̉̈́̀̑̊͋̇́̔͌̒̽̍͒̈́̉̌̆̐̍̑͐̓̈́̈́̉̾̾̐̑̈́̈́̏̅̂̏̒̒̔̄̅̾̅̈́́͛̎̒̃̇̄̌̎̕̕̚͘͘̕̚̚̕͘͜͜͜͝͝͝͝͠͝͝͝͝͝͝͠͠i̸̢̧̡̨̧̛̛̛̯̰͉̞͎̜̠̹͕͈̺̲̹̱̲̝̺̱͎̘̠̠̥̻̜̳͍̲̦̟̱͉̦̺͚̘̞̣͇͈̫̬̠̺̫̣̱̞̻͍͗̀͋̌̓̐̏̔͒̃̏͒́͒͐̀̏̄̋̀̌̑̊͋̊̓̑͆̌͗́̈́͛̑̆̋́͐́̑́̐̊̇́̓́̾̏͛̓̿̄̋́͌́͐̅̉̾̀̎́̍̓̇̈́̀̓̋̇̃̉̈́̄́̓͆̋͗̏̊̓͌̏̍̓̈́̀͒͌̓̔̀͛̐̓̓̚̚͘̚̕̚͘̚͜͜͜͠͝͝͝͠͠͝͠͝͠͠ͅͅͅf̴̡̡̢̡̡̧̢̛̖̬̗̦̗̯̬͓̫͉̣̩̣̺̜̘̠͈̫̘̻̣̫̯̪̗̦̣̣͚͕͉̳̜͉̟̠͖̭̫̱̀̅̃͆̋̃̀̂̈́̐̈́́̊͌̎̇̇̎̔͋͌̉͛̍̃̌̑͗͗͊́͆̄̓͐̎̊̒͋̃͒̿̓̽̀̌̇͛͋̿̏͘̕͘͘͝͠ͅͅf̸̡̧̡̨̧̢̡̧̢̧̢̡̺͔͖̖̭͎̹̺͈͎͓͙͙̺̗͚̹̻͇͍̗̦̜̬̜̱̱̤̞͍̪̫̖̦̥͉̹͈̝̞̱̝͕͇̤͇͔̜͚̮̳̰͉̜̭̘̙͔͖͍̠͕̪͓̩̳̣̖̱̗̯͙̮̤͖͉͙̤̜͔̼͎̟̜͕̮̻͎̗͓͖̭̱̠̱͕̩̳̬̦̣̟̮̻͉̜̤̞̼̤̩̻͕͈̲̬̖̠̣̹̫͉͉̜̝͓̱̘͖͎̜̳̞̣̌̏̒̒̂̓̀́͐̄͜͜͜ͅͅͅͅẽ̸̢̨̧̧̛͔͙̪͉̻͕̟̻̥̙͇̟̬̬͙͖̤͚̹̱͓̼͚̬̥͓̝͉͔͓̮̖̪͙̗̹̹̩̻̘̩̈́̈́͆͑̾͑̅̀͋̒̎́͊͂͆͑͂̅͂́̓̆̓̃͂̓̇̔̿̒̏̊̽͗͋̈́́̾̄̅̑͋̾̌̒̔̋͂̿̂͑̎͐̃̄̽̐́͛̌̎́͐̾͊̾̔̈́̀͂͑̄̚̕̕͜͠͠͠͠͝͝͠͝ͅͅͅŗ̵̢̧̢̨̨̨̧̨̨̨̨̨̡̡̛̛̛̛̭̗͕͔̫̬͔̗̖̳̬̭̼̼̳͈̞̞͚̖̤͈̫͔͙̗͕͍̯͔̰͉͎̫̪̳̤̝̞͖͉͚̭̲̣̪̱̝͖͎̻̭̫̠̯͔̺͖͈̝͉̝̦̦̪̮͈̠͙͎͚͖̬̯͔̹͚̗̜͖̩̦̹̙̦̼̤̮͈̥̘̼͚͍̣̳̣̲̺̠͍͖̪̱͚̬̺͐̌͆̓̀͊̔̈́̽̌̀͋̌̒̌̏̈́̉͒͗̇̾͌͛̌̿͛͋͌̇̎̒̈́̈́̋̋̾̑̂͌̓̇̀̽̈́̿͗̌̈́̆̉̈́̀̓͛͆̈́͊̓͒̔̐̓̈́̏̀̇̎̾̽͆́̈̄̃̋͆̀̑̈͛̄͊̽̄͌͛̈́͗͌̄͐̐̎͆̓̌̾̓̉̃̿̎͆͂͊̓͑͑̒̌̂̒̌̊̑̚͘̚͘͘͘͘̚͘̚̚̕͘̕͜͜͠͝͝͝͠͝͝͠e̵̹̲͚̼̺͚͔̟̱̱͉͙͙̅͛̃̿n̸̨̨̡̡̢̨̢̢̧̧̧̨̢̛̛̛̛̞̼͈̜̫͕͍͓̩̬̥̱̟̥̠̟͉̦̣̻̫̗̖̞̘̣̭̭̩̼̹͕͎̹̠̲̬̱̺͚͚̜̦̖̱͇̱͓̠̟̝̝͔̪͓͎̙̭͚̬̗̳̺̜̻̪̼̳͕̝̪̼̭̣̘̭͖̗͙̯̬͔͇͈̖̭̙͎͈͙͔͔̱̞̜̙͈͓̼̣̗̼͓̹͎͎̥͉͇̠͎͇͔̬͇͔̠͓̻͎̬̙̯͈̠͔͙̜̱̱̦̞̼͙̯̺͈̖̿͛̾̍͗̿̔̇̏̄̈́̑͋̈͋͑͒̅͆͗͊̓̽͊̒̊́́̽̊͐͋̈́̾̈́̎̄̈́͛̆̉̓͋̀̅̃̀́̓̓͛́͑́̽̈́́̈̂̓̒̓̇̅̔̊͑͒̔̽̔̔̃̑̐̽͑̈́͛̑̋̅̓͒̃͂̒͋̑͂̄̑̈́̽́͛̍̆̒̇̽͐̾̀͛̃͌̈͂̀͗͌̃̊̄̀̂͌͒͊͑̃͋̿̓̏́̒̀̚̚͘͘̚͘̚͘̕͜͜͠͠͠͝͠͝͝͝ͅͅͅt̸̛̛̛̳̣̑̐͗̓́̿̇̈́͗̆̎͑̏̑̿̑̿̽̾̋̓͂̇̇̋̀̇̇̈́̋͐̇͌͛̈́̓̏̒̀̂̒͑̿̑̃̒͊̈́́̈́͒͆̇̊͐̄̂̆͊̐͑̐̃͑͋͂̅͊̎͑͊̉̎͌͋̋̃͊͂̓͂̀͂̓̾͛̉͂̈̓͊͌̎͒͋͌̔̍̔͋̋̌̈̈̾̿̾͂͑͑͌̈́͗̀̽͋͂̔̄̐͐̈́̿̈́͑̉͊̍̾̚͘̕͘͘̕͜͝͠͝͝͝͝͝͝͠ ̶̨̡̡̡̢̡̨̨̨̢̨̧̛̛̛̛͕̩̠͍̯̩͉͈̱̲͕͍͕̪̺̟̱̖̩̠̙͉̳̬̲̭̫̯̥̝͕̯̝̭̗̯̪̳̹̘͍̠̫̩̠̹͈̘̙̙̩̬̺̗͔̳̱̼͚͖͓̞̲̣͓͙̘̮̰̦̭͇͓͍͖̻̭̜̤̠̫͇̥̮̩̠̱͚̝̫̟̪̯͇̪̭̺̄̀̑̄̂̅̽̾͆̍̂͛͌͛͆̍̉̽̎̌̓͂̓͆͒͂̆̃̃̈́̿́̽̔̿̂̿̃̋̊̐͂̈́̈́̅͑̂̾͌̍̾͂̾̄̐̎̓̐̎̆͂̈͂̉̊͗̽̿̓͊͒̓͋͂̇̈́͐̐̓̋̎͗̏̿̀̒̽͋̀̌̄̀̓͘̚̚͘̕̕̚̚̚̕͘̚͜͜͜͜͠͝͠͠͝͝͠͠ͅg̴̨̢̛̛͉̭̖̱̱̺̼̼̮͉̯̦̹͎̬̹̗̟͍͈̞͔̗̮̜̹͙͈͇͉̘̤͙͇̫̐͂̓̏̍̓̅͋͐̎̂̌̾͒̈̅͆͋̽̄͗̄̓̆̿̂̓͛̂̀̑̎́̏́͆͆̊̋͂͛̈́̈̊̉͑̏̓̂̑̒̃̏̇̎̄͒̅̋̀͑̃̌̅̏̾̓̄̌͊̕͘̕͘̚͜͝ͅͅͅą̶̧̛̛̛̛̻͍̱͈̯̙͈̘̻̱̬̠̮̥̲̟͖̙̳̲̲̼̘̪̗͊͐̾̀́̾̈́̇̔̐͌̇̂͊̒̏͋̌͊̂̈͆̀̈́̆̔̿͌̾̑͆̄̃͂͑̀̇̋̍͋̾̽̅͊̈́̐̀̐̈́̎͛͆̐̏̒̅̓̽̄̋͆̈́̐̆̓͊̅̉̅̄͒̈̂̋̓̑̎͛̔͆̃̔̄̑̄́̉͂̅̂̐̈̊̀̎̈́̄̌̀̚̕̚̕̚͘̚͘̚͘͝͝͠͝͝͠͝͠ͅm̸̧̢̡̡̧̢̢̬̖̯̫̲̙̥̻͙͚̘̫͚̳͎͍̘̹͙̮͔̝̪͇̯͕̲͓͔̯̞̲̩̭͇̟̥̗̻͓̟̙̖̲̦̞̬͙̞͉̤͖̮̙͈̺̱̖͎̫̣̪̗̜͔̳̺̘̥̬̺̩̞̘̣̙̼̮̼͇͎͕̥̻̙̜̤̪͕͈̥̞̼̱̖͔̲͎̥̯̭͚̱͚̹͇̬͍̙͇͙̩̝̌͋͆͑́̓̍̋̾̿̂͊͑͂̆͊̈́̕͘͜͜͜͜ͅͅͅȩ̢̨̡̡̨̧̨̨̖͇̼̜̖̟͕̰̖̲̼̹̲̟͖̗̬͈̭̺̲̗̜̞̝̳̞̹̻̠̱̳͎͙̫̪̤͈̼̯̻̼̝͕̱̖͔̫͍͚̰̟̻͔͖͎̙͓͙̰͖̲͓̞̰̤̠̣̻͇͕̼̥̰̺̮̼̙̭͈͈͔͎͜͜͜͜ͅͅͅ the same game. please type the word corresponding to your choice.")
    typewrite("[search] this realm for a way to escape")
    typewrite("[find] a machine similar to the one used by pancake stack")
    choice = ask_input(">")
    if choice == "search":
        searchpath()
    elif choice == "find":
        findpath()
    elif choice ==  "???":
        typewrite("sorry, reality is not stable enough for this. please choose another option.")
        game_state["choose???"] = True
        branch2contpathchoose()
def searchpath():
    clearterm()
    set_scene("searchpath")
    typewrite("you decide to begin a search for a way out of this place.")
    game_state["branch2_path"] = 1
    inyourhouse()
def findpath():
    clearterm()
    set_scene("findpath")
    typewrite("you decide to attempt to find a machine to help you exit.")
    game_state["branch2_path"] = 2
    inyourhouse()
def beforeyoumustblahblahblah():
    typewrite("before you can do anything, however, you must leave your house.")
    typewrite("what will you do?")
    inyourhouse()
def inyourhouse():
    clearterm()
    set_scene("inyourhouse")
    tick()
    time.sleep(1)
    typewrite("you may:")
    typewrite("try to [open] the door")
    typewrite("[look] for a way to dig out of your house")
    typewrite("[bang] the door until something happens")
    typewrite("[break] a window and climb out")
    typewrite("[try] to break reality")
    choice = ask_input(">")
    if choice == "open":
        typewrite("you try to open the door. it's locked.")
        inyourhouse()
    elif choice == "look":
        typewrite("you look around. you don't see any way to easily dig out.")
        inyourhouse()
    elif choice == "bang":
        tick()
        time.sleep(1)
        typewrite("you attempt to bang the door.")
        time.sleep(2.4726)
        print("BANG!")
        time.sleep(1)
        print("BANG!")
        time.sleep(2.425190)
        print("BANG!")
        typewrite("oh crap. your knuckles are bleeding.")
        typewrite("you may:")
        typewrite("[deal] with it and let them bleed")
        typewrite("[search] the house for bandages")
        choice = ask_input(">")
        if choice == "deal":
            game_state["bleeding"] = True
            typewrite("you decide to let them bleed and continue")
            inyourhouse()
    elif choice == "break":
        tick()
        typewrite("you decide to find a way to break a window, even though it is quite small.")
        typewrite("would you like to attempt to break it with your knuckles, or try to find something to hit it with?")
        time.sleep(1)
        typewrite("you may:")
        typewrite("[break] the windows with your bare fists")
        typewrite("[look] for something to break the window with")
        choice = ask_input(">")
        if choice == "break":
            tick()
            if game_state["bleeding"] == True:
                typewrite("your fists are bleeding. continue anyway?")
                typewrite("you may:")
                time.sleep(1)
                typewrite("[continue] anyway")
                typewrite("[don't] continue")
                choice = ask_input(">")
                if choice == "continue":
                    tick()
                    typewrite("you punch the window with all of your might.")
                    typewrite("the windows shatters into a million tiny pieces.")
                    typewrite("unfortunately, most of them fly into your body and lodge themselves between your skin.")
                    typewrite("it feels 1000x worse than having fiberglass in your skin, which is excruciating.")
                    game_state["glassshatter"] = 1
                elif choice == "don't":
                    typewrite("you decide not to break the window with your fists.")
                    typewrite("honestly, considering the condition they are in, that's probably the best choice")
                    inyourhouse()
        if choice == "look":
            tick()
            typewrite("you decide to look for an object to smash the window with.")
            time.sleep(1)
            typewrite("you see a paperclip on the floor. hella useful eh...")
            time.sleep(0.5)
            typewrite("you keep searching for something that will actually break the window.")
            time.sleep(1)
            typewrite("you find a stick!")
            time.sleep(1)
            typewrite("this will have to do. you prepare to take a swing at the window.")
            typewrite("alright, ready.")
            time.sleep(1)
            typewrite("3...")
            time.sleep(1)
            typewrite("2...")
            time.sleep(1)
            typewrite("1...")
            typewrite("you begin to swing the stick.")
            typewrite("bam! the window shatters into lots of miniscule fragments of glass.")
            time.sleep(0.5)
            typewrite("relieved that you didn't have to break the window with your fists, you climb out of the window and into the world outside.")
            outsideworld()
    elif choice == "try":
        tick()
        typewrite("you attempt to break reality.")
        time.sleep(1)
        typewrite("whatever tf that means lol.")
        time.sleep(1)
        typewrite("you tried Reality Break α.")
        time.sleep(1)
        typewrite("you were protected by the psychic shield.")
        time.sleep(1)
        typewrite("haha just kidding loser it's not 1995 anymore, it's 2009! PSI does not work anymore lol.")
        typewrite("determined, you try Reality Break β.")
        time.sleep(1)
        typewrite("you were protected by the psychic shield.")
        time.sleep(1)
        typewrite("haha why did you think that would work?")
        typewrite("you try Reality Break γ.")
        time.sleep(1)
        typewrite("you were protected by the psychic shield.")
        time.sleep(1)
        typewrite("ok please stop lol.")
        typewrite("you try Reality Break Ω.")
        time.sleep(1)
        typewrite("you were protected by the psychic shield.")
        time.sleep(1)
        typewrite("ok seriously stop. there is nothing you can do. please just try something else.")
        inyourhouse()
def outsideworld():
    typewrite("you are now outside. you see a path leading into the distance, winding very far that you cannot see an end.")
    tick()
titlescreen()
