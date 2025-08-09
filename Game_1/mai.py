import pygame, sys, random
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
game_font=pygame.font.Font('04B_19.TTF',30)

#=============================Function=============================
#SCORE
def score_view():
    if game_play:
        score_f=game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rectangle=score_f.get_rect(center=(80,30))
        screen.blit(score_f,score_rectangle)
    if game_play==False:
        hscore_f=game_font.render(f'High Score: {int(hscore)}',True,(255,255,255))
        hscore_rectangle=hscore_f.get_rect(center=(315,180))
        screen.blit(hscore_f,hscore_rectangle)

        score_f=game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rectangle=score_f.get_rect(center=(315,230))
        screen.blit(score_f,score_rectangle)
def Score():
    global score, hscore
    for pipe in pipe_list:
        if pipe.centerx < bird_rectangle.centerx and pipe not in scored_pipes and pipe.bottom > 600:
            scored_pipes.append(pipe)
            score += 1
            score_sound.play()
            if score > hscore:
                hscore = score
    score_view()
#MOVE FLOOR
def move_floor():
    screen.blit(fl,(fl_x,470))
    screen.blit(fl,(fl_x+336,470))
#CHECK COLLISION
def check_collision(pipes):
    for pipe in pipes:
        if bird_rectangle.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rectangle.bottom>=450 or bird_rectangle.top<=0:
        bird_die.play()
        return False
    else:
        return True
#TẠO ỐNG
def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop=(600,random_pipe_pos))
    top_pipe=pipe_surface.get_rect(midtop=(600,random_pipe_pos-650))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for move in pipes:
        move.centerx-=2
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom>600:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)
#BIRD ANIMATION    
def rotate_bird(bird1):
    new_bird=pygame.transform.rotozoom(bird1, -bird_y*3, 1)
    return new_bird
def bird_animation():
    new_bird=bird_list[bird_index]
    return new_bird, bird_rectangle

#=============================Variable=============================
#Initialization variable in game
gravity=0.25 
score=0
game_play=True
hscore=0
waiting=True
#GAME WINDOW
screen=pygame.display.set_mode((630,650))
icon=pygame.image.load(r'assets\yellowbird-downflap.png')
pygame.display.set_icon(icon)
tiltle=pygame.display.set_caption('Flappy bird')
#STANDBY SCREEN
standby_screen=pygame.image.load(r'assets\message.png')
standby_screen=pygame.transform.scale2x(standby_screen)
standby_screen_rectangle=standby_screen.get_rect(center=(315,300))
#BACKGROUND
bg=pygame.image.load(r'assets\background.png')
bg=pygame.transform.scale2x(bg)
#FLOOR
fl=pygame.image.load(r'assets\floor.png')
fl=pygame.transform.scale2x(fl)
fl_x=0
#BIRD
bird_down=pygame.transform.scale2x(pygame.image.load(r'assets\yellowbird-downflap.png'))
bird_mid=pygame.transform.scale2x(pygame.image.load(r'assets\yellowbird-midflap.png'))
bird_up=pygame.transform.scale2x(pygame.image.load(r'assets\yellowbird-upflap.png'))
bird_list=[bird_down, bird_mid, bird_up]
bird_index=2
bird=bird_list[bird_index]
#Timer bird
birdflap=pygame.USEREVENT+1
pygame.time.set_timer(birdflap,200)
bird_rectangle=bird.get_rect(center=(100,250))
bird_y=0
#PIPE
pipe_surface=pygame.image.load(r'assets\pipe-green.png')
pipe_surface=pygame.transform.scale2x(pipe_surface)
pipe_list=[]
scored_pipes=[]
#TIMER
spawpipe=pygame.USEREVENT
pygame.time.set_timer(spawpipe,2000)
pipe_height=[200, 300, 400]
#MÀN HÌNH GAME OVER
Screen_over=pygame.image.load(r'assets\gameover.png')
Screen_over=pygame.transform.scale2x(Screen_over)
Screen_over_rectangle=Screen_over.get_rect(center=(315,100))
#SOUND
flap_sound=pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound=pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound=pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown=100
bird_die=pygame.mixer.Sound('sound/sfx_die.wav')

#=============================GAME LOOP=============================
#WHILE LOOP
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                if waiting:
                    waiting=False
                    bird_y=-6
                    flap_sound.play()
                elif game_play:
                    bird_y=-6
                    flap_sound.play()
                else:
                    game_play=True
                    bird_y=-5
                    bird_rectangle.center=(100,250)
                    score=0
                    score_sound_countdown = 100
                    pipe_list.clear()
                    scored_pipes.clear()
        if event.type==spawpipe:
            pipe_list.extend(create_pipe())
        if event.type==birdflap:
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0
            bird, bird_rectangle = bird_animation()
    if waiting:        
        screen.blit(bg,(0,0))
        screen.blit(fl,(fl_x,470))
        screen.blit(standby_screen,standby_screen_rectangle)
    elif game_play:
        screen.blit(bg,(0,0))
        pipe_list=move_pipe(pipe_list)
        draw_pipe(pipe_list)
        fl_x-=1
        if fl_x==-336:
                fl_x=0
        move_floor()      
        bird_y+=gravity
        bird_rectangle.centery+=bird_y
        rotated_bird= rotate_bird(bird)
        screen.blit(rotated_bird,bird_rectangle)
        Score()
        game_play=check_collision(pipe_list)
    else:
        screen.blit(Screen_over,Screen_over_rectangle)
        score_view()
    pygame.display.update()