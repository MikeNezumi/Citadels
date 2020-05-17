import sys, math, random, pygame, pygame_textinput
from pygame.locals import *

""" ---------- CITADELS CLASSES ---------- """

class Player: #The human player
    def __init__(self, nickname, avatar, roles, gold, points, blueprints, citadel):
        self.nickname = nickname
        self.avatar = avatar
        self.roles = roles
        self.gold = gold
        self.points = points
        self.blueprints = blueprints
        self.citadel = citadel

class Role: #Persona the players play with
    def __init__(self, name, number, colour): #name is also the name of file (we have to add ".png", though)
        self.name = name
        self.number = number
        self.colour = colour

class Blueprint: #The blueprint for building
    def __init__(self, name, price, colour):
        self.name = name
        self.price = price
        self.colour = colour

""" ---------- GAME LOGIC FUNCTIONS ---------- """

def shuffle(cards): #shuffles any deck of cards -- cards is a list of Blueprint objects 
    for i in range(1000):
        index_a = i % len(cards) 
        index_b = random.randint(0, (len(cards) - 1))
        card = cards[index_a]
        cards[index_a] = cards[index_b]
        cards.remove(cards[index_b])
        cards.insert(index_b, card)
    return cards

def order(cards): #order cards by their numbers in ascending order -- cards is a list of Role objects
    ordered = []
    for i in range(8):
        for j in range(len(cards)):
            if cards[j].number == i + 1: 
                ordered.append(cards[j])
    cards = ordered
    return cards

""" ---------- PYGAME FUNCTIONS ---------- """
  
def terminate():
    pygame.quit()
    sys.exit()

    """ CLOSING GAME FORCEFULLY """

def check_for_quit(): 
    for event in pygame.event.get(pygame.QUIT):
        if event.type == pygame.QUIT:
            terminate()

    """ ONE FRAME (display update, quit button, clearing evets, next frame) """

def loop_footer(): #Belongs at the end of most game loops
    global FPS, FPS_CLOCK
    
    pygame.display.update()
    check_for_quit()
    pygame.event.clear()
    FPS_CLOCK.tick(FPS)

    """ INITIAL SCREEN """

def wait_for_start(surface): #initial screen
    global WINDOW_WIDTH, WINDOW_HEIGHT, FPS_CLOCK, FPS, BASIC_FONT
    
    title = pygame.transform.scale(pygame.image.load("launch/title.png"), (400, 350))
    background = pygame.transform.scale(pygame.image.load("backgrounds/welcome.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
    for i in range(FPS//2):
        surface.blit(background, (0, 0))
        surface.blit(title, (60, 50 - i*2))    
        loop_footer()
    done = False
    pygame.time.wait(500)
    while not done:
        for i in range(25):
            if i == 0:
                surface.blit(BASIC_FONT.render(" - press any key to play - ", True, (0, 0, 0)), (110, 280)) 
            elif i == 12:
                surface.blit(background, (0, 0))
                surface.blit(title, (60, 22))
            for event in pygame.event.get(pygame.KEYUP):
                done = True
                break
            loop_footer()

    """ NAMING PLAYERS """

def check_in(surface): #People join the game and name themselves
    global BASIC_RENDER, ALL_PLAYERS, Player
    
    people = 0
    players = names = []
    modes = ["two", "three", "four", "five", "six", "seven"]
    ordinals = ["First", "Second", "Third", "Forth", "Fifth", "Sixth", "Seventh"]
    men = shuffle(["man1", "man2", "man3", "man4", "man5", "man6", "man7"])
    women = shuffle(["woman1", "woman2", "woman3", "woman4", "woman5", "woman6", "woman7"])
    icons = [pygame.transform.scale(pygame.image.load("icons/" + mode + ".png"), (200, 200)) for mode in modes]
    background = pygame.transform.scale(pygame.image.load("backgrounds/menu.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    surface.blit(background, (0, 0))
    for i, icon in zip(range(len(icons)), icons): #Initial animation
        pygame.time.wait(200)
        surface.blit(icon, (40 + 200*i, 70))
        text_rect = pygame.Rect(40 + 200*i, 100, 200, 50)
        text_rect.center = (170 + (i//4)*10 - (i//5)*16 + 200*i, 240)
        text_surf = BASIC_FONT.render(modes[i] + " players", True, (0, 0, 0))
        surface.blit(text_surf, text_rect)
        loop_footer()

    yellow_rect = pygame.transform.scale(pygame.image.load("icons/yellow.png"), (430, 200))
    yellow_button = pygame.transform.scale(pygame.image.load("icons/yellow.png"), (100, 100))
    button_mark = pygame.transform.scale(pygame.image.load("icons/button.png"), (116, 116))
    done = False
    while not done: #Waits for click
        surface.blit(background, (0, 0))
        for i, icon in zip(range(len(icons)), icons):
            icon_rect = pygame.Rect(40 + 200*i, 50, 200, 200)
            if icon_rect.collidepoint(pygame.mouse.get_pos()):
                x = 10
            else:
                x = 0
            surface.blit(icon, (40 + 200*i, 70 - x))
            text_rect = pygame.Rect(40 + 200*i, 100, 200, 50)
            text_rect.center = (170 + (i//4)*10 - (i//5)*16 + 200*i, 240 - x)
            text_surf = BASIC_FONT.render(modes[i] + " players", True, (0, 0, 0))
            surface.blit(text_surf, text_rect)
        for event in pygame.event.get(pygame.MOUSEBUTTONUP):
            for i in range(len(icons)):
                button_rect = pygame.Rect((40 + 200*i, 100), (200, 200))
                (x, y) = pygame.mouse.get_pos()
                if button_rect.collidepoint(x, y):
                   people = i + 2
                   done = True
                   break
        loop_footer()
    
    for i in range(people): #1 cycle for each player 
        for j in range(10): #In animation
            surface.blit(background, (0, 0))
            surface.blit(yellow_rect, (45*j, 70))
            text_rect = pygame.Rect(30 + 45*j, 100, 200, 50)
            text_surf = BASIC_FONT.render(ordinals[i] + " player, introduce thyself:", True, (0, 0, 0))
            surface.blit(text_surf, text_rect)
            loop_footer()
            
        textinput = pygame_textinput.TextInput('','font/narkisim.ttf')
        surface.blit(background, (0, 0))
        
        finished = False
        man = True
        man_rect = pygame.Rect((100, 100), (500, 300))
        woman_rect = pygame.Rect((100, 100), (735, 300))
        while not finished: #naming a character
            check_for_quit()

            surface.blit(yellow_rect, (450, 70))
            surface.blit(yellow_button, (500, 300))
            surface.blit(yellow_button, (735, 300))

            for click in pygame.event.get(MOUSEBUTTONUP):
                (x, y) = pygame.mouse.get_pos()
                if man_rect.collidepoint(x, y):
                    man = True
                    surface.blit(background, (0, 0))
                elif woman_rect.collidepoint(x, y):
                    man = False
                    surface.blit(background, (0, 0))
                    
            if man == True:
                surface.blit(yellow_rect, (450, 70))
                surface.blit(yellow_button, (500, 300))
                surface.blit(yellow_button, (735, 300))
                surface.blit(button_mark, (492, 292))
            else:
                surface.blit(yellow_rect, (450, 70))
                surface.blit(yellow_button, (500, 300))
                surface.blit(yellow_button, (735, 300))
                surface.blit(button_mark, (727, 292))
                        
            text_rect = pygame.Rect(480, 100, 200, 50)
            text_surf = BASIC_FONT.render(ordinals[i] + " player, introduce thyself:", True, (0, 0, 0))
            surface.blit(text_surf, text_rect)
            man_rect = pygame.Rect(525, 335, 116, 116)
            man_surf = BASIC_FONT.render("man", True, (0, 0, 0))
            surface.blit(man_surf, man_rect)
            woman_rect = pygame.Rect(745, 335, 116, 116)
            woman_surf = BASIC_FONT.render("woman", True, (0, 0, 0))
            surface.blit(woman_surf, woman_rect)
                
            events = pygame.event.get()
            if textinput.update(events) == True:
                name = textinput.get_text()
                if name not in names:
                    if man == True:
                        player = Player(name, men.pop(), [], 2, 0, [], [])
                    else:
                        player = Player(name, women.pop(), [], 2, 0, [], [])
                    names.append(name)
                    ALL_PLAYERS.append(player)
                    finished = True
                    break
                else: #Player already named this way.
                    for j in range(40):
                        surface.blit(yellow_rect, (450, 70))
                        text_rect = pygame.Rect(480, 100, 200, 50)
                        text_surf = BASIC_FONT.render("Already picked, sorry.", True, (0, 0, 0))
                        surface.blit(text_surf, text_rect)
                        loop_footer()
                        
            surface.blit(textinput.get_surface(), (500, 180))
            loop_footer()
                
        for j in range(20): #Out animation
            surface.blit(background, (0, 0))
            surface.blit(yellow_rect, (450 + 45*j, 70))
            text_rect = pygame.Rect(480 + 45*j, 100, 200, 50)
            text_surf = BASIC_FONT.render(ordinals[i] + " player, introduce thyself:", True, (0, 0, 0))
            surface.blit(text_surf, text_rect)
            loop_footer()
        loop_footer()
    return ALL_PLAYERS
        
    """ PICKING CARDS """
    
def offer_cards(surface, cards, number, captions = None, alt_col = (0, 0, 0)): #returnes list of clicked cards
    global FPS, ALL_COLOURS, ALL_ROLES, BASIC_FONT, WINDOW_WIDTH, WINDOW_HEIGHT

    corners = { #tuples represent top left corners of cards
        1 : [(540, 205)],
        2 : [(430, 205), (650, 205)],
        3 : [(320, 205), (540, 205), (760, 205)],
        4 : [(210, 205), (430, 205), (650, 205), (870, 205)], 
        5 : [(320, 35), (540, 35), (760, 35), (430, 375), (650, 375)],
        6 : [(320, 35), (540, 35), (760, 35), (320, 375), (540, 375), (760, 375)],
        7 : [(210, 35), (430, 35), (650, 35), (870, 35), (320, 375), (540, 375), (760, 375)],
        8 : [(210, 35), (430, 35), (650, 35), (870, 35), (210, 375), (430, 375), (650, 375), (870, 375)],
        9 : [(100, 35), (320, 35), (540, 35), (760, 35), (980, 35), (210, 375), (430, 375), (650, 375), (870, 375)],
        10 : [(100, 35), (320, 35), (540, 35), (760, 35), (980, 35), (100, 375), (320, 375), (540, 375), (760, 375), (980, 375)]
    }
    background = pygame.transform.smoothscale(pygame.image.load("backgrounds/wood.png"), (WINDOW_WIDTH, WINDOW_WIDTH))
    bar = pygame.image.load("backgrounds/bar.png")
    
    for i in range(int(WINDOW_HEIGHT / 20)):
        surface.blit(background, (0, 40*i - 2 * WINDOW_HEIGHT))
        loop_footer()
        
    for i, card in zip(range(len(cards)), cards): #this loops prints cards
        if card in ALL_ROLES:
            image = pygame.transform.scale(pygame.image.load("roles/" + card.name + ".png"), (200, 320))
        else:
            image = pygame.transform.scale(pygame.image.load("blueprints/" + card.name + ".png"), (200, 320))
        surface.blit(image, (corners[len(cards)])[i])
        pygame.time.wait(200)
        loop_footer()
        
    picked_cards = []
    for i in range(number):
        if captions != None:
            if i == 0:
                caption_surf = BASIC_FONT.render("- " + captions[i] + " -", True, BLACK)
            else:
                caption_surf = BASIC_FONT.render("- " + captions[i] + " -", True, alt_col)    
            caption_rect = caption_surf.get_rect()
            caption_rect.center = (WINDOW_WIDTH / 2, 15)
            layer_surf = bar
            surface.blit(layer_surf, caption_rect)
            surface.blit(caption_surf, caption_rect)
        done = False
        while not done:
            pygame.display.update()
            for event in pygame.event.get(MOUSEBUTTONUP):
                for corner in corners[len(cards)]:
                    card = cards[corners[len(cards)].index(corner)]
                    card_rect = pygame.Rect(corner, (200, 320))
                    if card not in picked_cards:
                        (x, y) = pygame.mouse.get_pos()
                        if card_rect.collidepoint(x, y):
                            mark_x_y = (corner[0] - 5, corner[1] - 5)
                            mark_size = (210, 330)
                            mark = pygame.Rect((mark_x_y), (mark_size))
                            if i == 0:
                                pygame.draw.rect(surface, BLACK, mark, 8)
                            else:
                                pygame.draw.rect(surface, alt_col, mark, 8)
                            picked_cards.append(card)
                            done = True
                            break
            loop_footer()
        for _ in range(10):
            loop_footer()
    return picked_cards

    """ DISPLAYING PRESENT GAME TABLE LAYOUT """
    
def get_icon_center(angle):
    global WINDOW_WIDTH, WINDOW_HEIGHT

    angle = angle % 360
    radius = 300
    (x, y) = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + radius)
    
    if angle < 180:
        if angle < 90:
            a = math.sin(math.radians(angle)) * radius
            x += a 
            y -= radius - math.cos(math.radians(angle)) * radius 
        else:
            a = math.sin(math.radians(180 - angle)) * radius
            x += a
            y -= radius + math.cos(math.radians(180 - angle)) * radius
    else:
        angle -=(angle - 180) * 2
        if angle < 90:
            a = math.sin(math.radians(angle)) * radius
            x -= a 
            y -= radius - math.cos(math.radians(angle)) * radius
        else:
            a = math.sin(math.radians(180 - angle)) * radius
            x -= a
            y -= radius + math.cos(math.radians(180 - angle)) * radius
    return int(x), int(y)

def table(surface, players = None):
    global WINDOW_WIDTH, WINDOW_HEIGHT, DISPLAY_SURFACE
    global CARPET_PIC, TABLE_PIC
    
    if players != None:
        angle = 360 / len(players)
        floor = CARPET_PIC
        surface.blit(floor, (0, 0))    
        for i in range(len(players)):
            icon = pygame.image.load("avatars/" + players[i].avatar + ".png")
            icon = pygame.transform.rotate(icon, angle * i + 180)
            icon_rect = icon.get_rect()
            icon_rect.center = get_icon_center(angle * i)
            surface.blit(icon, icon_rect)
            loop_footer()
              
    table = TABLE_PIC
    table_rect = table.get_rect()
    table_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    surface.blit(table, table_rect)
        
    loop_footer()

    """ TRANSITION BETWEEN PLAYERS """
    
def rotate_table(surface, players, next_player): #rotates the table (animation), so that the next player is sat below (closest) by the table
    global WINDOW_HEIGHT, WINDOW_WIDTH, ALL_COLOURS
    global CARPET_PIC, TABLE_PIC

    floor = CARPET_PIC
    avatars = [pygame.image.load("avatars/" + player.avatar + ".png") for player in players]
    angle = (180 // len(players))
    next_index = players.index(next_player)
    table = TABLE_PIC
    table_rect = table.get_rect()
    table_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    surface.blit(table, table_rect)
    
    for i in range(angle * next_index): #rotation animation
        surface.blit(floor, (0, 0))
        for j, avatar in zip(range(len(avatars)), avatars):
            avatar = pygame.transform.rotate(avatar, i * 2 + j * int(angle) * 2 + 180)
            avatar_rect = avatar.get_rect()
            avatar_rect.center = get_icon_center((i * 2 + j * int(angle) * 2))
            surface.blit(avatar, avatar_rect)
        surface.blit(table, table_rect)
        loop_footer()

    for i in range(next_index):
        p = []
        p.append(players.pop(-1))
        players = p + players
    return players

    """ DISPLAYING MESSAGES """

def message(surface, title, waiting = False, player = None):
    global BASIC_FONT, ALL_COLOURS, WINDOW_WIDTH, WINDOW_HEIGHT
    global TABLE_PIC

    title_surf = pygame.font.Font('font/narkisim.ttf', 42).render(title, True, BLACK)
    title_rect = title_surf.get_rect()
    title_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        
    if waiting == False:
        surface.blit(title_surf, title_rect)
            
    else:
        table = TABLE_PIC
        table_rect = table.get_rect()
        table_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        sub_surf = BASIC_FONT.render(" - press a key, " + player.nickname + " - ", True, BLACK) 
        sub_rect = sub_surf.get_rect()
        sub_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 60)
                    
        done = False
        while not done:
            for i in range(35):
                surface.blit(table, table_rect)
                surface.blit(title_surf, title_rect)
                if i < 20:
                    surface.blit(sub_surf, sub_rect)
                for event in pygame.event.get(pygame.KEYUP):
                    done = True
                    break
                loop_footer()

def player_info(surface, players, current, returning = False, special = False, with_bank = False):
    global BASIC_FONT, ALL_COLOURS, WINDOW_WIDTH, WINDOW_HEIGHT
    global TABLE_PIC

    table = TABLE_PIC
    table_rect = table.get_rect()
    table_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    i = 1
    for player in players:
        if player != current:
            player_rect = pygame.Rect((0, 0), (80, 80))
            player_rect.center = get_icon_center((360 / (len(players))) * i)
            i += 1
            update = False
            init = True
            while player_rect.collidepoint(pygame.mouse.get_pos()):
                
                for event in pygame.event.get(MOUSEBUTTONUP):
                    return player
                
                if init == True:
                    surface.blit(table, table_rect)

                    name_surf = pygame.font.Font('font/narkisim.ttf', 50).render(player.nickname, True, BLACK)
                    name_rect = name_surf.get_rect()
                    name_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100)
                    surface.blit(name_surf, name_rect)

                    gold_surf = BASIC_FONT.render(str(player.gold) + " coins", True, BLACK)
                    gold_rect = gold_surf.get_rect()
                    gold_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 70)
                    surface.blit(gold_surf, gold_rect)

                    card_surf = BASIC_FONT.render(str(len(player.blueprints)) + " blueprints", True, BLACK)
                    card_rect = card_surf.get_rect()
                    card_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 40)
                    surface.blit(card_surf, card_rect)

                    if current.roles[0] == magician and with_bank == False:
                        instruction_surf = BASIC_FONT.render("- click to trade cards -", True, BLACK)
                        instruction_rect = instruction_surf.get_rect()
                        instruction_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 175)
                        surface.blit(instruction_surf, instruction_rect)

                    for j, card in zip(range(len(player.citadel)), player.citadel): 
                        surface.blit(pygame.transform.smoothscale(pygame.image.load("blueprints/" + card.name + ".png"), (110, 170)), ((WINDOW_WIDTH / 2 + 20 - 50*len(player.citadel)) + j*50, WINDOW_HEIGHT / 2 - 15))
                
                    update = True
                    init = False
                    
                loop_footer()
                
            if update == True:
                surface.blit(table, table_rect)

    if returning == True:
                return None

    if special == True:
        update = False
        init = True
        player_rect = pygame.Rect(0, 0, 50, 50)
        player_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 300)
        while player_rect.collidepoint(pygame.mouse.get_pos()):

            if init == True:
                surface.blit(table, table_rect)
                special_surf = BASIC_FONT.render("- click to use purple cards -", True, BLACK)
                special_rect = special_surf.get_rect()
                special_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
                surface.blit(special_surf, special_rect)

                init = False
                update = True

            for event in pygame.event.get(MOUSEBUTTONUP):
                return True

            loop_footer()

        if update == True:
            surface.blit(table, table_rect)
                
    loop_footer()
                
    
    """ BUTTONS CONTROLLING THE GAME """

def panel(surface, players, player, role = None, used = [], with_bank = True, rest = []): #waits for click on any button, returns the clicked button string
    global BASIC_FONT, WINDOW_HEIGHT, WINDOW_WIDTH, ALL_COLOURS, DISPLAY_SURFACE
    global SCROLL_PIC, TABLE_PIC

    table = TABLE_PIC
    table_rect = table.get_rect()
    table_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    surface.blit(table, table_rect)

    end = pygame.Rect(0, 30, 310, 120) #Rect
    end_content = BASIC_FONT.render(player.nickname, True, BLACK) #Surf
    end_alt = BASIC_FONT.render("- click to end turn -", True, BLACK) #Surf

    broken = BASIC_FONT.render("- you can't use this now -", True, BLACK) #Surf
    skill = pygame.Rect(0, 150, 310, 120) #Rect
    skill_content = [] #list of Surfs
    for r in player.roles:
        skill_content.append(pygame.transform.smoothscale(pygame.image.load("roles/" + r.name + ".png"), (110, 170))) #Surf
    if role.name == "assassin":
        skill_alt = BASIC_FONT.render("- click to murder a role -", True, BLACK) #Surf
    elif role.name == "thief":
        skill_alt = BASIC_FONT.render("- click to rob a role -", True, BLACK) #Surf
    elif role.name == "magician":
        skill_alt = BASIC_FONT.render("- click to trade blueprints -", True, BLACK) #Surf
    elif role.name == "warlord":
        skill_alt = BASIC_FONT.render("- click to destroy a building -", True, BLACK) #Surf
    else:
        skill_alt = broken

    gold = pygame.Rect(0, 270, 310, 120) #Rect
    gold_content = [pygame.transform.smoothscale(pygame.image.load("icons/gold.png"), (60, 60)), BASIC_FONT.render(" X " + str(player.gold), True, BLACK)] #list of Surfs
    gold_alt = BASIC_FONT.render("- click to get 2 coins -", True, BLACK) #Surf
    
    blueprint = pygame.Rect(0, 390, 310, 120) #Rect
    blueprint_content = [] #list of Surfs
    if len(player.blueprints) == 0:
        blueprint_content = BASIC_FONT.render("you have no blueprints", True, BLACK) #Surf  
    for b in player.blueprints:
        blueprint_content.append(pygame.transform.smoothscale(pygame.image.load("blueprints/" + b.name + ".png"), (100, 160))) #Surf
    blueprint_alt = BASIC_FONT.render("- click to get a blueprint -", True, BLACK) #Surf
        
    build = pygame.Rect(0, 510, 310, 120)
    build_content = [] #list of Surfs
    if len(player.citadel) == 0:
        build_content = BASIC_FONT.render("you haven't built anything", True, BLACK) #Surf  
    for c in player.citadel:
        build_content.append(pygame.transform.smoothscale(pygame.image.load("blueprints/" + c.name + ".png"), (100, 160))) #Surf
    
    yes_alt = BASIC_FONT.render("- click to build stuff -", True, BLACK) #Surf
    no_alt = BASIC_FONT.render("- there's nothing to build -", True, BLACK) #Surf
    build_alt = no_alt

    special = pygame.Rect(0, 510, 310, 120)

    buttons = [[end, end_content, end_alt], [skill, skill_content, skill_alt], [gold, gold_content, gold_alt, []], [blueprint, blueprint_content, blueprint_alt], [build, build_content, build_alt]]
    for i in used:
        (buttons[i])[2] = broken
    scroll = SCROLL_PIC
    returns = ["end", "skill", "gold", "blueprint", "build"] 

    update = True
    switched = 10
    rejected = False
    while True: #waiting for selection (phase before this function returns anything)

        if with_bank == False: #Wizard
            assaulted = player_info(surface, players, player, False, False, False)
            if assaulted != None:
                table_rect = TABLE_PIC.get_rect()
                table_rect.center = (WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2)
                cache_blueprints = []
                cache_blueprints = player.blueprints
                player.blueprints = assaulted.blueprints
                assaulted.blueprints = cache_blueprints
                loop_footer()
                message(surface, "cards switched")
                for k in range(30):
                    loop_footer()
                return "magic"
            
        elif (smithy1 in player.citadel or laboratory1 in player.citadel or graveyard1 in player.citadel) and rejected == False:
            if smithy1 in player.citadel and (player.gold < 2 or 51 in rest):
                rejected = True
                continue
            if laboratory1 in player.citadel and (len(player.blueprints) < 2 or 52 in rest):
                rejected = True
                continue    
            if graveyard1 in player.citadel and (player.gold < 1 or 53 in rest):
                rejected = True
                continue

            print("passed")
            click = player_info(surface, players, player, False, True)
            summonable = []
            for card in player.citadel:
                if card in [smithy1, laboratory1, graveyard1]:
                    summonable.append(card)
            if click != None:
                summoned = offer_cards(DISPLAY_SURFACE, summonable, 1, ["choose the card"])[0]
                loop_footer()
                print(summoned.name)
                return summoned.name

        else:
            player_info(surface, players, player)
        
        if 4 not in used:
            (buttons[4])[2] = no_alt
            for blue in player.blueprints:
                if blue.price <= player.gold: 
                    (buttons[4])[2] = yes_alt           
            
        for button in buttons:
            if button[0].collidepoint(pygame.mouse.get_pos()) and switched == 10:
                b = button[1]
                button[1] = button[2]
                button[2] = b
                update = True
                switched = buttons.index(button)
                break
            loop_footer()
                
        if update == True: #displaying scroll
            surface.blit(scroll, (-170, -70)) 
            for button in buttons:
                if type(button[1]) != list:
                    button_rect = button[1].get_rect()
                    button_rect.center = button[0].center
                    button_rect.y += 15
                    surface.blit(button[1], button_rect)
                elif len(button) == 4:
                    button_rect_a = (button[1])[0].get_rect()
                    button_rect_a.x = 85
                    button_rect_a.y = button[0].y + 50
                    button_rect_b = (button[1])[1].get_rect()
                    button_rect_b.x = 160
                    button_rect_b.y = button[0].y + 58
                    surface.blit((button[1])[0], button_rect_a)
                    surface.blit((button[1])[1], button_rect_b)
                else:
                    for card, i in zip(button[1], range(len(button[1]))):
                        bonus_y = 0
                        if buttons.index(button) == 4:
                            bonus_y += 48 
                        card_rect = card.get_rect()
                        card_rect.x = i*50 + 10
                        card_rect.y = button[0].y - 10 + bonus_y
                        surface.blit(card, card_rect)
            
            update = False
        
        if switched != 10 and role != None:
            while (buttons[switched])[0].collidepoint(pygame.mouse.get_pos()): #two posible outcomes: reprinting or returning value    
                for event in pygame.event.get(MOUSEBUTTONUP):
                    return returns[switched]
                loop_footer()
            b = (buttons[switched])[1]
            (buttons[switched])[1] = (buttons[switched])[2]
            (buttons[switched])[2] = b
            switched = 10
            update = True
            
        loop_footer()
        
def game_over(surface, players, winner): 
    global WINDOW_WIDTH, WINDOW_HEIGHT, ALL_COLOURS

    others = []
    others_surfs = []
    top = 0
    combo = ["yellow", "green", "blue", "red", "purple"]
    bonus = True
    one = True
    hunted = False
            
    for player in players:
        others.append(player)
        colours = []
        for card in player.citadel:
            player.points += card.price
            colours.append(card.colour)
            if card in [dragon_gate1, university1]:
                player.points += 2

        for colour in combo:
            if colour not in colours:
                if haunted_city1 in player.citadel and hunted == False:
                    colours.append(colour)
                    hunted = True
                else:
                    bonus = False

        if bonus == True:
            player.points += 3
        if player == winner:
            player.points += 2
        if len(player.citadel) >= 8:
            player.points += 2

        if player.points > top:
            one = True
            top = player.points
            winner = player
        elif player.points == top:
            one = False
        
    instruction = pygame.font.Font('font/narkisim.ttf', 35).render("- click any key to close -", True, WHITE) #Surf
    background = pygame.transform.smoothscale(pygame.image.load("backgrounds/dark.png"), (WINDOW_WIDTH, WINDOW_HEIGHT)) #Surf
    if one == True:
        sentence = pygame.font.Font('font/narkisim.ttf', 60).render(winner.nickname + " has won the game! (" + str(winner.points) + " points)", True, WHITE) #Surf
    else:
        sentence = pygame.font.Font('font/narkisim.ttf', 60).render("There are multiple winners!", True, WHITE) #Surf

    for guy in others:
        others_surfs.append(BASIC_FONT.render(guy.nickname + " - " + str(guy.points) + " points", True, WHITE))
            

    while True:      
        surface.blit(background, (0, 0))
        surface.blit(sentence, (60, 40))
        for surf, i in zip(others_surfs, range(len(others_surfs))):
            surface.blit(surf, (100, 110 + i*35))

        for i in range(15):
            for _ in pygame.event.get(MOUSEBUTTONUP):
                terminate()
            for _ in pygame.event.get(pygame.KEYUP):
                terminate()
            loop_footer()

        surface.blit(background, (0, 0))
        surface.blit(sentence, (60, 40))
        for surf, i in zip(others_surfs, range(len(others_surfs))):
            surface.blit(surf, (100, 110 + i*35))
        surface.blit(instruction, (740, WINDOW_HEIGHT / 2 + 180))
                
        for i in range(20):
            for _ in pygame.event.get(MOUSEBUTTONUP):
                terminate()
            for _ in pygame.event.get(pygame.KEYUP):
                terminate()
            loop_footer()
                
        loop_footer()
        
            
""" ---------- CREATING ROLES' OBJECTS ---------- """

assassin = Role("assassin", 1, "grey")
thief = Role("thief", 2, "grey")
magician = Role("magician", 3, "grey")
king = Role("king", 4, "yellow")
bishop = Role("bishop", 5, "blue")
merchant = Role("merchant", 6, "green")
architect = Role("architect", 7, "grey")
warlord = Role("warlord", 8, "red")

""" ---------- CREATING BLUEPRINTS' OBJECTS ---------- """

temple1 = Blueprint("Temple", 1, "blue")
temple2 = Blueprint("Temple", 1, "blue")
temple3 = Blueprint("Temple", 1, "blue")
tavern1 = Blueprint("Tavern", 1, "green")
tavern2 = Blueprint("Tavern", 1, "green")
tavern3 = Blueprint("Tavern", 1, "green")
tavern4 = Blueprint("Tavern", 1, "green")
tavern5 = Blueprint("Tavern", 1, "green")
watchtower1 = Blueprint("Watchtower", 1, "red")
watchtower2 = Blueprint("Watchtower", 1, "red")
watchtower3 = Blueprint("Watchtower", 1, "red")

church1 = Blueprint("Church", 2, "blue")
church2 = Blueprint("Church", 2, "blue")
church3 = Blueprint("Church", 2, "blue")
market1 = Blueprint("Market", 2, "green")
market2 = Blueprint("Market", 2, "green")
market3 = Blueprint("Market", 2, "green")
market4 = Blueprint("Market", 2, "green")
trading_post1 = Blueprint("Trading Post", 2, "green")
trading_post2 = Blueprint("Trading Post", 2, "green")
trading_post3 = Blueprint("Trading Post", 2, "green")
prison1 = Blueprint("Prison", 2, "red")
prison2 = Blueprint("Prison", 2, "red")
prison3 = Blueprint("Prison", 2, "red")
haunted_city1 = Blueprint("Haunted City", 2, "purple")

manor1 = Blueprint("Manor", 3, "yellow")
manor2 = Blueprint("Manor", 3, "yellow")
manor3 = Blueprint("Manor", 3, "yellow")
manor4 = Blueprint("Manor", 3, "yellow")
manor5 = Blueprint("Manor", 3, "yellow")
monastery1 = Blueprint("Monastery", 3, "blue")
monastery2 = Blueprint("Monastery", 3, "blue")
monastery3 = Blueprint("Monastery", 3, "blue")
docks1 = Blueprint("Docks", 3, "green")
docks2 = Blueprint("Docks", 3, "green")
docks3 = Blueprint("Docks", 3, "green")
battlefield1 = Blueprint("Battlefield", 3, "red")
battlefield2 = Blueprint("Battlefield", 3, "red")
battlefield3 = Blueprint("Battlefield", 3, "red")
keep1 = Blueprint("Keep", 3, "purple")
keep2 = Blueprint("Keep", 3, "purple")

castle1 = Blueprint("Castle", 4, "yellow")
castle2 = Blueprint("Castle", 4, "yellow")
castle3 = Blueprint("Castle", 4, "yellow")
harbor1 = Blueprint("Harbor", 4, "green")
harbor2 = Blueprint("Harbor", 4, "green")
harbor3 = Blueprint("Harbor", 4, "green")

palace1 = Blueprint("Palace", 5, "yellow")
palace2 = Blueprint("Palace", 5, "yellow")
palace3 = Blueprint("Palace", 5, "yellow")
cathedral1 = Blueprint("Cathedral", 5, "blue")
cathedral2 = Blueprint("Cathedral", 5, "blue")
town_hall1 = Blueprint("Town Hall", 5, "green")
town_hall2 = Blueprint("Town Hall", 5, "green")
fortress1 = Blueprint("Fortress", 5, "red")
fortress2 = Blueprint("Fortress", 5, "red")
laboratory1 = Blueprint("Laboratory", 5, "purple")
smithy1 = Blueprint("Smithy", 5, "purple")
graveyard1 = Blueprint("Graveyard", 5, "purple")
observatory1 = Blueprint("Observatory", 5, "purple")

library1 = Blueprint("Library", 6, "purple")
school_of_magic1 = Blueprint("School of Magic", 6, "purple")
university1 = Blueprint("University", 6, "purple")
dragon_gate1 = Blueprint("Dragon Gate", 6, "purple")

""" ---------- GLOBAL VARIABLES ---------- """

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TURQUOISE = (0, 128, 128)
YELLOW = (250, 204, 0)

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 30
BASIC_FONT_SIZE = 28

restrictions = []

""" ---------- GLOBAL LISTS ---------- """

ALL_PLAYERS = [] #Citadels is a game for 2 to 7 players, specified by the sit_down() function
ALL_BLUEPRINTS = [temple1, temple2, temple3, tavern1, tavern2, tavern3, tavern4, tavern5, watchtower1, watchtower2, watchtower3, church1, church2, church3, market1, market2, market3, market4, trading_post1, trading_post2, trading_post3, prison1, prison2, prison3, haunted_city1, manor1, manor2, manor3, manor4, manor5, monastery1, monastery2, monastery3, docks1, docks2, docks3, battlefield1, battlefield2, battlefield3, keep1, keep2, harbor1, harbor2, harbor3, castle1, castle2, castle3, palace1, palace2, palace3, cathedral1, cathedral2, town_hall1, town_hall2, fortress1, fortress2, laboratory1, smithy1, graveyard1, observatory1, library1, school_of_magic1, university1, dragon_gate1]
ALL_ROLES = [assassin, thief, magician, king, bishop, merchant, architect, warlord]
ALL_COLOURS = [BLACK, WHITE, YELLOW, TURQUOISE]

""" ---------- LOADING STATIC PICTURES ---------- """

CARPET_PIC = pygame.transform.smoothscale(pygame.image.load("backgrounds/carpet.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
TABLE_PIC = pygame.transform.smoothscale(pygame.image.load("icons/table.png"), (500, 500))
SCROLL_PIC = pygame.transform.smoothscale(pygame.image.load("icons/scroll.png"), (600, WINDOW_HEIGHT + 200))

""" ---------- PYGAME MAIN FUNCTION ---------- """

def main():
    global FPS_CLOCK, DISPLAY_SURFACE, BASIC_FONT
    global ALL_PLAYERS, ALL_BLUEPRINTS, ALL_ROLES, ALL_COLOURS #all cards

    pygame.init()

    """ ---------- ADDITIONAL PYGAME VARIABLES ---------- """
    
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font('font/narkisim.ttf', BASIC_FONT_SIZE)

    """ ---------- GAME STARTS ---------- """ ########################################### SERIOUSLY, GAME STARTS, MATE #######################################

    pygame.display.set_caption('Citadels') 
    
    wait_for_start(DISPLAY_SURFACE) #initial screen
    
    for player in check_in(DISPLAY_SURFACE): #greeting players, handing each one four bluerints
        for _ in range(4):
            player.blueprints.append(shuffle(ALL_BLUEPRINTS).pop())

    king_player = ALL_PLAYERS[1] #picks role first
    players = ALL_PLAYERS #list of players sorted according to the current orer around the table
    damaged = None
    
    """ ---------- ONE GAME ROUND LOOP ---------- """

    winner = None
    well_played = False
    while not well_played: #Each run represents one game round (picking roles, changeover of players)
            
        """ PICKING ROLES """
        
        unplayed_roles = []
        for role in ALL_ROLES:
            unplayed_roles.append(role)
        unplayed_roles = shuffle(unplayed_roles)
        players = rotate_table(DISPLAY_SURFACE, players, king_player)

        if len(players) in [4, 5]: #for 4 and 5 player games, some roles are put aside each round
            for _ in range(5 - len(ALL_PLAYERS)):
                role = unplayed_roles.pop(0)
                message(DISPLAY_SURFACE, role.name + "'s out")
                for i in range(90):
                    loop_footer()
                table(DISPLAY_SURFACE)

        thrown_away = unplayed_roles.pop(0)
        unplayed_roles = order(unplayed_roles)
        unpicked_roles = [] 
        picked = []
        for role in unplayed_roles:
            unpicked_roles.append(role)
        
        if len(players) == 2:
            for i in range(4):
                message(DISPLAY_SURFACE, players[0].nickname + " picks roles", True, players[0])
                if i == 0 or i == 3:
                    picked = offer_cards(DISPLAY_SURFACE, unpicked_roles, 1, ["pick a role"])
                    (players[0].roles).append(picked[0])
                    unpicked_roles.remove(picked[0])
                    if i != 3:
                        players = rotate_table(DISPLAY_SURFACE, players, players[1])
                    else:
                        unplayed_roles.remove(unpicked_roles[0])
                else:
                    picked = offer_cards(DISPLAY_SURFACE, unpicked_roles, 2, ["pick a role", "remove a role"], WHITE)
                    (players[0].roles).append(picked[0])
                    unpicked_roles.remove(picked[0])
                    unpicked_roles.remove(picked[1])
                    unplayed_roles.remove(picked[1])
                    players = rotate_table(DISPLAY_SURFACE, players, players[1])
            for player in players:
                player.roles = order(player.roles)
                if "king" == player.roles[0].name or "king" == player.roles[1].name:
                    king_player = player
           
        elif len(players) == 3:
            for i in range(6):
                message(DISPLAY_SURFACE, players[0].nickname + " picks roles", True, players[0])    
                picked = offer_cards(DISPLAY_SURFACE, unpicked_roles, 1, ["pick a role"])
                (players[0].roles).append(picked[0])
                unpicked_roles.remove(picked[0])
                if i != 5:
                    players = rotate_table(DISPLAY_SURFACE, players, players[1])
                else:
                    unplayed_roles.remove(unpicked_roles[0])
            for player in players:
                player.roles = order(player.roles)
                if "king" == player.roles[0].name or "king" == player.roles[1].name:
                    king_player = player
                             
        else:
            for i in range(len(players)):
                message(DISPLAY_SURFACE, players[0].nickname + " picks roles", True, players[0])
                picked = offer_cards(DISPLAY_SURFACE, unpicked_roles, 1, ["pick a role"])
                (players[0].roles).append(picked[0])
                unpicked_roles.remove(picked[0])
                if len(players) == 7 and i == 5:
                    unplayed_roles.append(thrown_away)
                    unpicked_roles.append(thrown_away)
                if i != len(players) - 1:
                    players = rotate_table(DISPLAY_SURFACE, players, players[1])
                else:
                    unplayed_roles.remove(unpicked_roles[0])
            for player in players:
                if "king" == player.roles[0].name:
                    king_player = player
                  
        """ PLAYING ROLES """
        
        robbed = None
        robber = None
        untouchable = None
        raided = None
        
        for player in players:
            for role in player.roles:
                if role == bishop:
                    untouchable = player
                    
        for role in unplayed_roles:
            next_player = None
            for player in players:
                if role in player.roles:
                    next_player = player
            if next_player == None:
                continue

            if next_player.roles[0] == robbed: #Thief's skill
                tax = next_player.gold
                next_player.gold = 0
                robber.gold += tax

            if next_player.roles[0] == merchant: #Merchant's bonus
                next_player.gold += 1
            
            
            if next_player.roles[0] == architect: #Architect's bonus
                (next_player.blueprints).append(ALL_BLUEPRINTS.pop())
                (next_player.blueprints).append(ALL_BLUEPRINTS.pop())

            if next_player.roles[0] in [king, bishop, merchant, warlord]: #Taxes
                for build in next_player.citadel:
                    if build.colour == role.colour:
                        next_player.gold +=1

            if (next_player.roles[0]).colour != "grey" and school_of_magic1 in next_player.citadel: #School of Magic tax
                next_player.gold += 1    
            
            if players.index(next_player) == 0:
                table(DISPLAY_SURFACE, players)   
            players = rotate_table(DISPLAY_SURFACE, players, next_player)
            message(DISPLAY_SURFACE, next_player.nickname + "'s turn", True, next_player)

            with_bank = True
            if next_player.roles[0] == magician:
                with_bank = False
            mana = True
            switchable = []
                
            arch_stamina = 2
            restrictions = [] #used skills' indexes, not to be used again
            rest = []
            rest_dict = {0 : "end", 1 : "skill", 2 : "gold", 3 : "blueprint", 4 : "build"}
            while True:

                if next_player != damaged:
                    rest.append(53)

                action = panel(DISPLAY_SURFACE, players, next_player, role, restrictions, with_bank, rest)
                
                invalid = False
                for i in restrictions:
                    if action == rest_dict[i]:
                        invalid = True
                        break
                if invalid:
                    continue

                if action == "Smithy":
                    table(DISPLAY_SURFACE, players)
                    next_player.gold -= 2
                    for _ in range(3):
                        (next_player.citadel).append(ALL_BLUEPRINTS.pop())
                    rest.append(51)
                    loop_footer()
                    continue
                elif action == "Laboratory":
                    table(DISPLAY_SURFACE, players)
                    disowned = offer_cards(DISPLAY_SURFACE, next_player.blueprints, 1, ["pick a role"])[0]
                    (next_player.blueprints).remove(disowned)
                    ALL_BLUEPRINTS.append(disowned)
                    table(DISPLAY_SURFACE, players)
                    next_player.gold += 1
                    rest.append(52)
                    loop_footer()
                    continue
                elif action == "Graveyard":
                    table(DISPLAY_SURFACE, players)
                    if raided != None:
                        (next_player.blueprints).append(raided)
                        raided = None

                    rest.append(53)
                    loop_footer()
                    continue
                    
                elif action == "end":
                    break
                elif action == "skill" and mana == True: #Wizard
                    restrictions.append(1)
                    if role.name in ["king", "bishop", "merchant", "architect"]:
                        continue
                    elif role.name == "assassin":
                        victims = []
                        for victim in ALL_ROLES:
                            if victim.name != "assassin" and victim not in next_player.roles:
                                victims.append(victim)
                        dead = offer_cards(DISPLAY_SURFACE, victims, 1, ["murder one of these guys"])
                        if dead[0] in unplayed_roles:
                            unplayed_roles.remove(dead[0])
                        for p in ALL_PLAYERS:
                            if dead[0] in p.roles:
                                (p.roles).remove(dead[0])
                        table(DISPLAY_SURFACE, players)
                        message(DISPLAY_SURFACE, next_player.nickname + "'s turn")
                        continue
                    elif role.name == "thief": 
                        victims = []
                        for victim in ALL_ROLES:
                            if victim.name not in ["assassin", "thief"] and victim not in next_player.roles: 
                                victims.append(victim)
                        robbed = offer_cards(DISPLAY_SURFACE, victims, 1, ["rob one of these guys"])[0]
                        robber = next_player
                        table(DISPLAY_SURFACE, players)
                        message(DISPLAY_SURFACE, next_player.nickname + "'s turn")
                        continue
                    
                    elif role.name == "magician":
                        for paper in next_player.blueprints:
                            switchable.append(paper)
                        if len(switchable) == 0:
                            mana = False
                        else:
                            restrictions.remove(1)
                            with_bank = True 
                            rejected = offer_cards(DISPLAY_SURFACE, switchable, 1, ["pick the card you wish to get rid of"])[0]
                            switchable.remove(rejected)
                            (next_player.blueprints).remove(rejected)
                            (next_player.blueprints).append(ALL_BLUEPRINTS.pop())
                            table(DISPLAY_SURFACE, players)
                        continue
                    
                    elif role.name == "warlord":
                        attackable = []
                        for player in players:
                            if player not in [untouchable, next_player]:
                                for card in player.citadel:
                                    if card.price <= next_player.gold + 1 and card.name != "Keep":
                                        attackable.append(player)
                                        
                        if attackable == []:
                            continue
                        else:
                            message(DISPLAY_SURFACE, "Pick a player to attack")
                            for _ in range(30):
                                loop_footer()
                            table_rect = TABLE_PIC.get_rect()
                            table_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
                            DISPLAY_SURFACE.blit(TABLE_PIC, table_rect)
                            attacked = None
                            while attacked == None:
                                attacked = player_info(DISPLAY_SURFACE, players, next_player)
                                damaged = attacked
                                if attacked == None:
                                    loop_footer()
                                    continue
                                elif attacked in attackable:
                                    raidable = []
                                    for card in attacked.citadel:
                                        if card.price <= next_player.gold:
                                            raidable.append(card)
                                    raided = offer_cards(DISPLAY_SURFACE, raidable, 1, ["destroy one of these"], WHITE)[0]
                                    (attacked.citadel).remove(raided)
                                    ALL_BLUEPRINTS.append(raided)
                                    next_player.gold -= (raided.price - 1)
                                    table(DISPLAY_SURFACE, players)
                                    loop_footer()
                                    continue
                                else:
                                    attacked = None
                                    message(DISPLAY_SURFACE, "Oops, not this lad")
                                    for _ in range(30):
                                        loop_footer()
                                    table_rect = TABLE_PIC.get_rect()
                                    table_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
                                    DISPLAY_SURFACE.blit(TABLE_PIC, table_rect)
                                loop_footer()
                        continue
                elif action == "gold":
                    restrictions.append(2)
                    restrictions.append(3)
                    next_player.gold += 2
                    continue
                elif action == "blueprint":
                    if library1 in next_player.citadel and observatory1 not in next_player.citadel:
                        (next_player).blueprints.append(ALL_BLUEPRINTS.pop(0))
                        (next_player).blueprints.append(ALL_BLUEPRINTS.pop(0))
                    else:
                        restrictions.append(2)
                        restrictions.append(3)
                        choice = []
                        choice.append(ALL_BLUEPRINTS.pop(0))
                        choice.append(ALL_BLUEPRINTS.pop(0))
                        if observatory1 in next_player.citadel:
                            choice.append(ALL_BLUEPRINTS.pop())
                        if library1 in next_player.citadel:
                            chosen = offer_cards(DISPLAY_SURFACE, choice, 2, ["pick 2 cards"])
                            (next_player).blueprints.append(chosen.pop())
                        else:
                            chosen = offer_cards(DISPLAY_SURFACE, choice, 1, ["pick a card"])
                        ALL_BLUEPRINTS.append(choice[0])
                        if observatory1 in next_player.citadel:
                            ALL_BLUEPRINTS.append(choice[1])
                        (next_player).blueprints.append(chosen[0])
                        table(DISPLAY_SURFACE, players)
                        message(DISPLAY_SURFACE, next_player.nickname + "'s turn")
                        continue
                elif action == "build":
                    if role != architect or arch_stamina == 0:
                        restrictions.append(4)
                    else:
                        arch_stamina -= 1
                    buildable = []
                    for blueprint in next_player.blueprints:
                        if blueprint.price <= next_player.gold:
                            buildable.append(blueprint)
                    if buildable != []:
                        chosen = offer_cards(DISPLAY_SURFACE, buildable, 1, ["build one of these"])
                        (next_player.citadel).append(chosen[0])
                        (next_player.blueprints).remove(chosen[0])
                        next_player.gold -= chosen[0].price
                        table(DISPLAY_SURFACE, players)
                        message(DISPLAY_SURFACE, next_player.nickname + "'s turn")
                        continue

                elif action == "magic":
                    restrictions.append(1)
                    with_bank = True
                    continue
                loop_footer()
                
            for player in players:
                if len(player.citadel) >= 8:
                    winner = player
                    well_played = True
            (next_player.roles).remove(role)
            if next_player == damaged:
                damaged = None
            loop_footer()
        players = rotate_table(DISPLAY_SURFACE, players, next_player)
        loop_footer()
    
    game_over(DISPLAY_SURFACE, ALL_PLAYERS, winner)
    
if __name__ == '__main__':
    main()
