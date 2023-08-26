



import pygame as pyg
import time
import sys




WIDTH = 1080
HEIGHT = 720
TICK_RATE = 500 #low is faster ticks
POL_CAP = 5000

tab = 0 #count for which tab we are currently on (0-3)
ticks = 0
warn_time = [0, 0, 1, -1] #[time, have, required, tab] 
warn = {
    "time":0,
    "had":0,
    "req":1,
    "tab":-1
}
WIN = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Meltdown")
pyg.display.set_icon(pyg.image.load("build/exe.win-amd64-3.10/assets/img/icon.png"))


# Tab buttons (x, y, width, height)
tab1_rect = pyg.Rect(0, 0.675 * HEIGHT, WIDTH*0.25, HEIGHT*0.048)
tab2_rect = pyg.Rect(WIDTH*0.25, 0.675 * HEIGHT, WIDTH*0.25, HEIGHT*0.048)
tab3_rect = pyg.Rect(WIDTH*0.5, 0.675 * HEIGHT, WIDTH*0.25, HEIGHT*0.048)
tab4_rect = pyg.Rect(WIDTH*0.75, 0.675 * HEIGHT, WIDTH*0.25, HEIGHT*0.048)

#expansion buttons
exp_prov_rect = pyg.Rect(WIDTH*0.05, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
exp_nat_rect = pyg.Rect(WIDTH*0.20, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
exp_con_rect = pyg.Rect(WIDTH*0.35, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
exp_glo_rect = pyg.Rect(WIDTH*0.50, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)

#product buttons
pro_1_rect = pyg.Rect(WIDTH*0.05, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
pro_2_rect = pyg.Rect(WIDTH*0.20, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
pro_3_rect = pyg.Rect(WIDTH*0.35, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)
pro_4_rect = pyg.Rect(WIDTH*0.50, HEIGHT*0.78, WIDTH*0.1, WIDTH*0.1)


#the bar covering the pollution img (to hide progress ig)
#pol_bar_rect = pyg.Rect(WIDTH*0.025, HEIGHT*0.1223, WIDTH*0.045, HEIGHT*0.415)

pol_amt = 0.0 # tracks pollution amt
money_amt = 10.0 # tracks money amt

pol_rate = 0.5
money_rate = 0.15

upgrade_track = [0, 0, 0]
upgrade_costs = [
    [40, 100, 540, 1200],
    [10, 200, 1150, 1900]
]
news_queue = []

def imgImport(name, w, h, rot=0):
    return pyg.transform.rotate(pyg.transform.scale(pyg.image.load("build/exe.win-amd64-3.10/assets/img/" + name), (w, h)), rot)

EPOCH = time.time() * 1000
BACKIMG = imgImport("background_img.png", WIDTH, HEIGHT)

#(PARTO) my additions coming in, trying to mess with opacity
WORLDWATER = imgImport("water_1.png", int(WIDTH*0.8), int(HEIGHT*0.58)).convert_alpha()
alpha = 255
WORLDWATERPOLLUTION = imgImport("water_p_1.png", int(WIDTH*0.8), int(HEIGHT*0.58)).convert_alpha()
alpha_Water = 0 # IF THIS VALUE GETS HIGHER THE WATER GETS MORE POLLUTED (VALUE GOES TO 255 MAX)

WORLD = imgImport("world.png", int(WIDTH*0.8), int(HEIGHT*0.58))
TAB1 = imgImport("tab1.png", WIDTH, 0.35*HEIGHT)
TAB2 = imgImport("tab2.png", WIDTH, 0.35*HEIGHT)
TAB3 = imgImport("tab3.png", WIDTH, 0.35*HEIGHT)
TAB4 = imgImport("tab4.png", WIDTH, 0.35*HEIGHT)
POL_BAR = imgImport("pol_bar.png", WIDTH*0.05, HEIGHT*0.5)
NEWS_BOX = imgImport("news.png", WIDTH*.16, HEIGHT*.28)


lock = imgImport("buttons/lock.png", WIDTH*0.1, WIDTH*0.1)
buy = imgImport("buttons/buy.png", WIDTH*0.1, WIDTH*0.1)

exp_prov = imgImport("build/exe.win-amd64-3.10/assets/img/buttons/exp/exp_prov.png", WIDTH*0.1, WIDTH*0.1)
exp_nat = imgImport("buttons/exp/exp_nat.png", WIDTH*0.1, WIDTH*0.1)
exp_con = imgImport("buttons/exp/exp_con.png", WIDTH*0.1, WIDTH*0.1)
exp_glo = imgImport("buttons/exp/exp_glo.png", WIDTH*0.1, WIDTH*0.1)

pro_1 = imgImport("buttons/pro/pro_1.png", WIDTH*0.1, WIDTH*0.1)
pro_2 = imgImport("buttons/pro/pro_2.png", WIDTH*0.1, WIDTH*0.1)
pro_3 = imgImport("buttons/pro/pro_3.png", WIDTH*0.1, WIDTH*0.1)
pro_4 = imgImport("buttons/pro/pro_4.png", WIDTH*0.1, WIDTH*0.1)

#expansion descriptions
exp_prov_des = imgImport("buttons/exp/exp_prov_des.png", WIDTH*0.12, WIDTH*0.12)
exp_nat_des = imgImport("buttons/exp/exp_nat_des.png", WIDTH*0.12, WIDTH*0.12)
exp_con_des = imgImport("buttons/exp/exp_con_des.png", WIDTH*0.12, WIDTH*0.12)
exp_glo_des = imgImport("buttons/exp/exp_glo_des.png", WIDTH*0.12, WIDTH*0.12)

#product descriptions
pro_1_des = imgImport("buttons/pro/pro_1_des.png", WIDTH*0.12, WIDTH*0.12)
pro_2_des = imgImport("buttons/pro/pro_2_des.png", WIDTH*0.12, WIDTH*0.12)
pro_3_des = imgImport("buttons/pro/pro_3_des.png", WIDTH*0.12, WIDTH*0.12)
pro_4_des = imgImport("buttons/pro/pro_4_des.png", WIDTH*0.12, WIDTH*0.12)


pyg.font.init()
doc_font = pyg.font.Font("build/exe.win-amd64-3.10/assets/fonts/ShareTech.ttf", 16)



def time_passed():
    return int(time.time() * 1000 - EPOCH)

def draw_text(text, x, y, color):
    ##print(str(x) +  " " + str(y))
    img = doc_font.render(text, True, color)
    WIN.blit(img, (x, y))

def not_enough(required, current):
    warn["had"] = current
    warn['req'] = required
    print('not enough')



def draw():
    
    mx, my = pyg.mouse.get_pos()

    #WIN.fill((0, 0, 0))
    WIN.blit(BACKIMG, (0, 0)) #putting images at coordinates (origin top left)
    WIN.blit(WORLD, (WIDTH*0.18, HEIGHT*0.05))
    WIN.blit(WORLDWATER, (WIDTH*0.18, HEIGHT*0.05)) #draw the water background 
    WIN.blit(WORLDWATERPOLLUTION, (WIDTH*0.18, HEIGHT*0.05)) #draw the water background green
    WIN.blit(NEWS_BOX, (0.12*WIDTH, 0.3*HEIGHT))
    
    
    
    #tabs
    match tab:
        case 0: #expansion buttons

            WIN.blit(TAB1, (0, HEIGHT*0.65))
            WIN.blit(exp_prov, (WIDTH*0.05, HEIGHT*0.78))
            WIN.blit(exp_nat, (WIDTH*0.20, HEIGHT*0.78))
            WIN.blit(exp_con, (WIDTH*0.35, HEIGHT*0.78))
            WIN.blit(exp_glo, (WIDTH*0.50, HEIGHT*0.78))
            
            if(upgrade_track[0] < 1):
                WIN.blit(lock, (WIDTH*0.20, HEIGHT*0.78))
            if(upgrade_track[0] < 2):
                WIN.blit(lock, (WIDTH*0.35, HEIGHT*0.78))
            if(upgrade_track[0] < 3):
                WIN.blit(lock, (WIDTH*0.50, HEIGHT*0.78))
            
            if(upgrade_track[0] > 0):
                WIN.blit(buy, (WIDTH*0.05, HEIGHT*0.78))
            if(upgrade_track[0] > 1):
                WIN.blit(buy, (WIDTH*0.20, HEIGHT*0.78))
            if(upgrade_track[0] > 2):
                WIN.blit(buy, (WIDTH*0.35, HEIGHT*0.78))
            
            # descriptions
            if (exp_prov_rect.collidepoint(mx, my)):
                WIN.blit(exp_prov_des, (WIDTH*0.04, HEIGHT*0.6))
            elif exp_nat_rect.collidepoint(mx, my) and upgrade_track[0] > 0:
                WIN.blit(exp_nat_des, (WIDTH*0.19, HEIGHT*0.6))
            elif exp_con_rect.collidepoint(mx, my) and upgrade_track[0] > 1:
                WIN.blit(exp_con_des, (WIDTH*0.34, HEIGHT*0.6))
            elif exp_glo_rect.collidepoint(mx, my) and upgrade_track[0] > 2:
                WIN.blit(exp_glo_des, (WIDTH*0.49, HEIGHT*0.6))

            
            ###print("1")
        case 1:
            WIN.blit(TAB2, (0, HEIGHT*0.65))

            WIN.blit(pro_1, (WIDTH*0.05, HEIGHT*0.78))
            WIN.blit(pro_2, (WIDTH*0.20, HEIGHT*0.78))
            WIN.blit(pro_3, (WIDTH*0.35, HEIGHT*0.78))
            WIN.blit(pro_4, (WIDTH*0.50, HEIGHT*0.78))
            
            if(upgrade_track[1] < 1):
                WIN.blit(lock, (WIDTH*0.20, HEIGHT*0.78))
            if(upgrade_track[1] < 2):
                WIN.blit(lock, (WIDTH*0.35, HEIGHT*0.78))
            if(upgrade_track[1] < 3):
                WIN.blit(lock, (WIDTH*0.50, HEIGHT*0.78))
            
            if(upgrade_track[1] > 0):
                WIN.blit(buy, (WIDTH*0.05, HEIGHT*0.78))
            if(upgrade_track[1] > 1):
                WIN.blit(buy, (WIDTH*0.20, HEIGHT*0.78))
            if(upgrade_track[1] > 2):
                WIN.blit(buy, (WIDTH*0.35, HEIGHT*0.78))
            
            # descriptions
            if (pro_1_rect.collidepoint(mx, my)):
                WIN.blit(pro_1_des, (WIDTH*0.04, HEIGHT*0.6))
            elif pro_2_rect.collidepoint(mx, my) and upgrade_track[1] > 0:
                WIN.blit(pro_2_des, (WIDTH*0.19, HEIGHT*0.6))
            elif pro_3_rect.collidepoint(mx, my) and upgrade_track[1] > 1:
                WIN.blit(pro_3_des, (WIDTH*0.34, HEIGHT*0.6))
            elif pro_4_rect.collidepoint(mx, my) and upgrade_track[1] > 2:
                WIN.blit(pro_4_des, (WIDTH*0.49, HEIGHT*0.6))


        
        case 2:
            WIN.blit(TAB3, (0, HEIGHT*0.65))
        
        case 3:
            WIN.blit(TAB4, (0, HEIGHT*0.65))

    # pollution bar
    WIN.blit(POL_BAR, (WIDTH*0.03, HEIGHT*0.08))            
    pyg.draw.rect(WIN, (96, 107, 94), pyg.Rect(WIDTH*0.035, HEIGHT*0.1525, WIDTH*0.045, HEIGHT*0.415*(1 - pol_amt/POL_CAP)))




    # balance text
    draw_text(("Balance: $" + f"{round(money_amt, 2):,}" + "K " ), WIDTH*0.01, HEIGHT*0.04, (200, 200, 200))
    

    #pyg.display.update()

def pol_tick():
    global pol_amt
    pol_amt += pol_rate

def money_tick():
    global money_amt
    money_amt += money_rate

def main():
    global tab, ticks, pol_rate, money_rate, pol_amt, money_amt, upgrade_track, alpha_Water
    #clock = pyg.time.Clock() #controlls fps and whatnot
    pyg.mouse.set_cursor(pyg.cursors.diamond)
    
     

    run = True
    
    # game loop. this will be active to run the game
    pyg.init()
    while run:
        #clock.tick(FPS) #again, controls fps 
        #print(time_passed())
        print(money_rate)
        

        if(int(time_passed()/TICK_RATE) > ticks):
            ticks += 1
            pol_tick()
            money_tick()
            print("--------")
            

        
        enough = False
        for event in pyg.event.get():
            if event.type == pyg.QUIT: run = False

            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1: #left/primary click
                    mx, my = pyg.mouse.get_pos()
                    if tab1_rect.collidepoint(mx, my) and tab != 0:
                        #money_tick(5)
                        #print("clicked1")
                        tab = 0
                        #print(tab)

                    elif tab2_rect.collidepoint(mx, my) and tab != 1:
                        #money_tick(10000)
                        #print("clicked2")
                        tab = 1
                        #print(tab)
                    
                    elif tab3_rect.collidepoint(mx, my) and tab != 2:
                        #money_tick(5)
                        #print("clicked3")
                        tab = 2
                        #print(tab)
                    
                    elif tab4_rect.collidepoint(mx, my) and tab != 3:
                        #money_tick(5)
                        #print("clicked4")
                        tab = 3
                        #print(tab)

                    elif tab == 0:
                        if upgrade_track[0] == 4:
                            print("no dice")
                        elif exp_prov_rect.collidepoint(mx, my) and upgrade_track[0] == 0:
                            if(money_amt < upgrade_costs[0][0]):
                                not_enough(upgrade_costs[0][0], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[0][0]
                            money_rate += 0.208
                            pol_rate += 0.2
                            upgrade_track[0] += 1
                        elif exp_nat_rect.collidepoint(mx, my) and upgrade_track[0] == 1:
                            if(money_amt < upgrade_costs[0][1]):
                                not_enough(upgrade_costs[0][1], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[0][1]
                            money_rate += 0.392
                            pol_rate += 0.2
                            upgrade_track[0] += 1
                        elif exp_con_rect.collidepoint(mx, my) and upgrade_track[0] == 2:
                            if(money_amt < upgrade_costs[0][2]):
                                not_enough(upgrade_costs[0][2], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[0][2]
                            money_rate += 0.833
                            pol_rate += 0.3
                            upgrade_track[0] += 1
                        elif exp_glo_rect.collidepoint(mx, my) and upgrade_track[0] == 3:
                            if(money_amt < upgrade_costs[0][3]):
                                not_enough(upgrade_costs[0][3], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[0][3]
                            money_rate += 1.292
                            pol_rate += 0.7
                            upgrade_track[0] += 1

                    elif tab == 1:
                        if upgrade_track[1] == 4:
                            print("no dice")
                        elif pro_1_rect.collidepoint(mx, my) and upgrade_track[1] == 0:
                            if(money_amt < upgrade_costs[1][0]):
                                not_enough(upgrade_costs[1][0], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[1][0]
                            money_rate += 0.05
                            pol_rate += 0.5
                            upgrade_track[1] += 1
                        elif pro_2_rect.collidepoint(mx, my) and upgrade_track[1] == 1:
                            if(money_amt < upgrade_costs[1][1]):
                                not_enough(upgrade_costs[1][1], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[1][1]
                            money_rate += 0.125
                            pol_rate += 0.6
                            upgrade_track[1] += 1
                        elif pro_3_rect.collidepoint(mx, my) and upgrade_track[1] == 2:
                            if(money_amt < upgrade_costs[1][2]):
                                not_enough(upgrade_costs[1][2], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[1][2]
                            money_rate += 0.208
                            pol_rate += 0.75
                            upgrade_track[1] += 1
                        elif pro_4_rect.collidepoint(mx, my) and upgrade_track[1] == 3:
                            if(money_amt < upgrade_costs[1][3]):
                                not_enough(upgrade_costs[1][3], money_amt)
                                enough = True
                                continue
                            money_amt -= upgrade_costs[1][3]
                            money_rate += 0.625
                            pol_rate += 1.2
                            upgrade_track[1] += 1



        keys_pressed = pyg.key.get_pressed()
        


        # game is over

        ##print(pol_amt)
        alpha_Water = pol_amt/POL_CAP * 255
        WORLDWATERPOLLUTION.set_alpha(alpha_Water) #opacityyy 
        WORLDWATER.set_alpha(alpha)

        draw()
        if(enough):
            warn["tab"] = tab
            warn["time"] = time_passed()
            

        
        if time_passed() - warn["time"] <= 3000 and tab == warn["tab"]:
            
            draw_text(" !!    INSUFFICIENT FUNDS: $" + str(round(warn["had"], 2)) + "K / $" + str(warn["req"]) + "K    !!", WIDTH*0.68, HEIGHT*0.79, (0, 0, 0))
            print("______________________________")

        
        #updates display. display wont change if this isnt here
        pyg.display.update()
    pyg.quit()

# dont touch this; if u have question abt it dm jaden
if __name__ == "__main__":
    main()