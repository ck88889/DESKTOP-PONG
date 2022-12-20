
import random 
import mysql.connector
from math import *
from tkinter import *

scoredb = mysql.connector.connect(
  host="localhost",
  user = "ckwan", 
  password = "hookslice89",
  database = "SCOREDB"
)

score_cursor = scoredb.cursor()
#score_cursor.execute("DELETE FROM leaderboard WHERE username = ''")
#scoredb.commit

namelist = [""]
scorelist = [0]

def update_board():
    score_cursor.execute("SELECT * FROM leaderboard")
    myresult = score_cursor.fetchall()
    #list of scores and their usernames 
    global namelist
    global scorelist
    namelist.clear()
    scorelist.clear()

    #read values from table into lists
    for x in myresult:
        namelist.append(x[0])
        scorelist.append(int(x[1]))
        print(x[0] + " -> " + x[1])
    
    for x in range(1, len(namelist)):
        scorelist[x-1] = scorelist[x]
    scorelist[len(scorelist) - 1] = 0

    #sort list 
    for i in range(len(namelist)):
        for x in range(i, len(namelist)):
            if scorelist[x] > scorelist[i]:
                n_tmp = namelist[x]
                s_tmp = scorelist[x]

                namelist[x] = namelist[i]
                scorelist[x] = scorelist[i]

                namelist[i] = n_tmp
                scorelist[i] = s_tmp

#make back screen 
WIDTH = 800; 
HEIGHT = 400; 

BOM_WIDTH = 800; 
BOM_HEIGHT = 60; 

TIME_LIMIT = 180 #seconds
SCORE = 0; 

FIRST = 1

main = Tk()
main.title("DESKTOP PONG")

update_board()

#canvas 
c = Canvas(main, width = WIDTH, height = HEIGHT, bg = "black")
c.pack()

#bottom canvas 
b = Canvas(main, width = BOM_WIDTH, height = BOM_HEIGHT, bg = "black")
b.pack()

#timer
timer = Label(c, text = "03:00")
timer.config(font=("Lato", 20, "bold"))
timer.config(fg=("white"))
timer.config(bg=("black"))
timer.place(x=WIDTH/2 - 35, y = 3)

#score
score = b.create_text((BOM_WIDTH/2,BOM_HEIGHT/2), text = "SCORE: {fscore}".format(fscore = SCORE), fill = "white", font=("Lato", 17, "bold"))

#create the net for the ping pong game 
for i in range(10): 
    y_value = 40*i; 
    divider = c.create_rectangle(WIDTH/2,30+y_value,WIDTH/2 + 5,4+y_value, fill="white")

#the user's paddle
user_paddle = c.create_rectangle(0,20, 10, 90, fill = "white")
c.moveto(user_paddle, 10, 50)

def up(event): 
    u_paddle = c.coords(user_paddle)
    if u_paddle[1] >= 30:
        y = -17
        c.move(user_paddle, 0, y)

def down(event):
    u_paddle = c.coords(user_paddle)
    if u_paddle[1] <= HEIGHT - 110:
        y = 17
        c.move(user_paddle, 0, y)

#bind the user function
main.bind("<Up>", up)
main.bind("<Down>", down)

#the game's paddle
game_paddle = c.create_rectangle(WIDTH - 10,HEIGHT -20, WIDTH -20, HEIGHT-90, fill = "white")

#the ping pong ball class 
class Ball: 
    def __init__(self):
        self.shape = c.create_oval(20, 20, 50, 50, fill="white")
        c.moveto(self.shape, WIDTH - 100, random.randint(100, HEIGHT-100))
        self.speedx = 5 
        self.speedy = 5
        self.active = True
        self.move_active()

    def ball_update(self):
        c.move(self.shape, self.speedx, self.speedy)
        pos_ball = c.coords(self.shape)
        pos_upaddle = c.coords(user_paddle)
        if pos_ball[2] >= (WIDTH - 40): #bounce off game side 
            self.speedx *= -1
        if pos_ball[3] >= HEIGHT or pos_ball[1] <= 0: #checks if its within vertical boundaries
            self.speedy *= -1
        if (pos_upaddle[0]) > pos_ball[0] and pos_ball[0] > 0: #checks if the paddle and ball connect 
            if pos_upaddle[1]-5 <= pos_ball[1] and pos_upaddle[3]+5 >= pos_ball[3]:
                    global SCORE; 
                    SCORE += 1; 
                    b.itemconfigure(score, text = "SCORE: {fscore}".format(fscore = SCORE))
                    self.speedx *= -1

    def move_active(self):
        if self.active:
            self.ball_update()
            main.after(15, self.move_active) # frame time  

#create ball object 
ball = Ball()

#move game's paddle 
def g_paddle(): #recursion 
    pos_ball = c.coords(ball.shape)
    if pos_ball[2] > (WIDTH/2) and pos_ball[2] < WIDTH:
        c.moveto(game_paddle, WIDTH - 20, pos_ball[1] - 50)
    main.after(15, g_paddle)

main.after(15, g_paddle)

def new_ball():
    y_value = random.randint(100, HEIGHT-100)
    c.moveto(ball.shape, WIDTH - 80, y_value)

def reset():  
    new_ball()
    global TIME_LIMIT
    global SCORE 
    c.moveto(game_paddle, WIDTH - 20, y_value)
    c.moveto(user_paddle, 10, 50) 
    TIME_LIMIT = 180
    SCORE = 0
    b.itemconfigure(score, text = "SCORE: {fscore}".format(fscore = SCORE))

#username
uname = "UNKNOWN PLAYER"

isclicked_done = bool(FALSE)
isclicked_exit = bool(FALSE)

def callback():
    global isclicked_done
    isclicked_done = not isclicked_done 

isclicked_done = bool(FALSE)

def callback_e():
    global isclicked_exit
    isclicked_exit = not isclicked_exit 

#reset menu for game 
class MENU():
    def __init__(self):
        self.menu_bg = c.create_rectangle(WIDTH/4, HEIGHT/8*2, WIDTH/4*3, HEIGHT/8 * 6, fill = "white")
        self.title = Label(c, text = "NEW PLAYER", font=("Lato", 20, "bold"), fg=("black"), bg=("white")) #heading 
        self.title.place(x=WIDTH/2 - 90, y = HEIGHT/4 + 30)
        self.uname_l = Label(c, text = "Enter your username: ", font=("Lato", 14), fg=("black"), bg=("white")) #directions
        self.uname_l.place(x=WIDTH/2 -145, y = HEIGHT/4 + 80)
        self.uname_entry = Entry(main, font = ('calibre',12,'normal'), bg = "black", fg = "white", width = 31)#entry 
        self.old_uname = self.old_uname = self.uname_entry.get()
        c.create_window(WIDTH/4 + 200, HEIGHT/4 + 120, window = self.uname_entry)
        self.okay_btn = Button(c, text='OK', width= 10,height= 1, command = callback, font=("Lato", 11, "bold")) #okay button
        self.okay_btn.place(x=WIDTH/2 - 50, y=HEIGHT/2 + 40)
        self.exit_btn = Button(c, text='EXIT', width= 7,height= 1, command = callback_e, font=("Lato", 11, "bold")) #exit button
        self.exit_btn.place(x=WIDTH/2 + 110, y=HEIGHT/2 + 60)
           
    def delete_m(self):
        c.delete(self.menu_bg)
        self.title.destroy()
        self.uname_l.destroy()
        self.uname_entry.destroy()
        self.okay_btn.destroy()
        self.exit_btn.destroy()
    
    def update_lb(self):
        self.old_uname = self.uname_entry.get()
        action = "INSERT INTO leaderboard (username, score) VALUES (%s, %s)"
        if(self.uname_entry.get() == ""):
            val = ("UNKNOWN PLAYER", SCORE)
        else:
            val = (self.old_uname, SCORE)
        score_cursor.execute(action, val)
        scoredb.commit()

    def stop(self):
        global isclicked_done
        if isclicked_done:
            #insert info into table
            self.update_lb()
            self.uname_entry.delete(0, END)
            #reset visual elements of the game 
            self.delete_m()
            reset()
            return
        else:
            c.moveto(ball.shape, 1000, 1000)
            c.moveto(user_paddle, 10, 50) 
            c.moveto(game_paddle, WIDTH -20, 50)
            b.itemconfigure(score, text = "SCORE: 0")
            timer.config(text = "03:00")
        
        global isclicked_done_e
        if isclicked_exit:
            self.update_lb()
            exit()
        
        main.after(15, self.stop)    

reset_menu = MENU()
reset_menu.stop()

def new_game():
    global isclicked_done 
    isclicked_done = bool(FALSE)
    reset_menu = MENU()
    reset_menu.stop()

reset_btn = Button(b, text='RESTART', width= 10,height= 1, command = new_game)
reset_btn.config(font=("Lato", 11, "bold"))
reset_btn.place(x=BOM_WIDTH - 110, y=BOM_HEIGHT/4)

def show_lb():
    update_board()
    global namelist
    global scorelist

    new_window = Toplevel(main)
    new_window.configure(bg='black')
    new_window.title("LEADERBOARD")
    new_window.geometry("700x600")

    heading = Label(new_window, text = "HIGH SCORES", font=("Lato", 20, "bold"), fg=("white"), bg=("black"))
    heading.place(x=700/2 - 100, y = 500/12)
    
    heading_r = Label(new_window, text = "RANK", font=("Lato", 17, "bold"), fg=("white"), bg=("black"))
    heading_r.place(x= 700/10, y = 500/10 + 55)

    heading_n = Label(new_window, text = "NAME", font=("Lato", 17, "bold"), fg=("white"), bg=("black"))
    heading_n.place(x= 700/10*3, y = 500/10 + 55)

    heading_n = Label(new_window, text = "SCORE", font=("Lato", 17, "bold"), fg=("white"), bg=("black"))
    heading_n.place(x= 700/10 * 8, y = 500/10 + 55)

    for x in range(10):
        rank = Label(new_window, text = str((x + 1)).zfill(2), font=("Lato", 15, "bold"), fg=("white"), bg=("black"))
        rank.place(x= 700/10*1.25, y = 500/10 + 100 + 40*x)
        name = Label(new_window, text = namelist[x], font=("Lato", 12, "bold"), fg=("white"), bg=("black"))
        name.place(x= 700/10*3, y = 500/10 + 100 + 40*x)
        score = Label(new_window, text = str(scorelist[x]).zfill(2), font=("Lato", 15, "bold"), fg=("white"), bg=("black"))
        score.place(x= 700/10 * 8.35, y = 500/10 + 100 + 40*x)

sboard_btn = Button(b, text='HIGH SCORES', command = show_lb, width= 15,height= 1)
sboard_btn.config(font=("Lato", 11, "bold"))
sboard_btn.place(x=10, y=BOM_HEIGHT/4)

def game_t(): 
    global TIME_LIMIT 
    TIME_LIMIT -= 1
    minutes = '{:.0f}'.format(trunc((TIME_LIMIT)/60)).zfill(2) 
    seconds = '{:.0f}'.format(TIME_LIMIT - trunc((TIME_LIMIT)/60)*60).zfill(2)
    timer.config(text = minutes + ":" + seconds)

    pos_ball = c.coords(ball.shape) 
    if pos_ball[2] < 0: #display time
        new_ball()

    if(TIME_LIMIT == 0):
        new_game()

    main.after(1000, game_t) #recursion 


main.after(1000, game_t)

mainloop()