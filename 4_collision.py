import os
import pygame


######################################################################
# 기본 초기화(반드시 해야하는 것들)
pygame.init() 


screen_width = 640
screen_height = 480 
screen = pygame.display.set_mode((screen_width, screen_height))


pygame.display.set_caption("Nado Pang") 


clock = pygame.time.Clock()
######################################################################

# 1. 사용자 게임 초기화(배경 화면, 게임 이미지, 좌표, 속도, 폰트 등 설정)

current_path = os.path.dirname(__file__) # 이 파일이 있는 위치를 반환
image_path = os.path.join(current_path, "images") #images 폴더 위치 반환


# 배경 만들기
background = pygame.image.load(os.path.join(image_path,"background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지의 높이 값을 받아서 캐릭터를 위에 두기 위함

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path,"character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width /2) - (character_width / 2)
character_y_pos = screen_height - (stage_height + character_height)

# 캐릭터 이동 방향
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 5

# 무기만들기
weapon = pygame.image.load(os.path.join(image_path,"weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 발사 속도
weapon_speed = 7

# 공 만들기(4개 크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path,"balloon1.png")),
    pygame.image.load(os.path.join(image_path,"balloon2.png")),
    pygame.image.load(os.path.join(image_path,"balloon3.png")),
    pygame.image.load(os.path.join(image_path,"balloon4.png")) ]

# 공 크기에 따른 최초 스피드(공 크기가 작아지면 바닥에 튕기는 높이도 다름) (공이 클 수록 튀어오르는 높이가 높음)
ball_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3에 해당하는 값

# 공들
balls = []

# 최초 생긴 큰 공 추가
balls.append({
    "pos_x" : 50, # 공의 x좌표
    "pos_y" : 50, # 공의 y좌표
    "img_idx" : 0, # 공 크기는 어떤지
    "to_x" : 3, # 공의 x축 이동방향 (왼쪽이면 -3, 오른쪽이면 +3)
    "to_y" : -6, # y축 이동방향(공이 처음에 시작될 때 살짝 위로 올라갔다가 내려옴)
    "init_spd_y" : ball_speed_y[0]}) # 공이 스테이지에 튕겨서 올라갈 때 최초 속도(올라갈 땐 점점 속도 느려지고 다시 내려올 때는 점점 빨라져야 포물선 모양으로 움직일테니)

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1


running = True 
while running:
    dt = clock.tick(60) 

    # 2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # 캐릭터 왼쪽으로
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT: # 캐릭터 오른쪽으로
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: # 무기 발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2) # 무기 발사 위치(캐릭터의 중간에서 쏘니까)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos]) # 무기의 위치를 (x, y)의 형태로 weapons 리스트에 저장

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width


    # 무기 위치 조정(위로 쭉 올라가게)
    # 만약 처음 시작점이 (100, 200)이면, 무기 발사 속도가 10이니까 (100, 190) (100, 180) (100, 170) 이렇게 쭉 쭉 올라감
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]

    

    # 천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0] 
    # t축은 아래로 내려가는게 양의 값인것을 기억해보셈(w[1] > 0 이면 화면 위로 아예 나가버렸다는 말이 되지?  )
    # 그러니까 if wp[1] > 0 이란 말은 무기가 천장 아래에 있을 때만 weapons에 추가하라는 의미가 됨



    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls): # ball 리스트에 ball_indext가 몇번째 index인지 그리고 그에 해당하는 ball_value를 반환
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로벽에 닿았을 때 공 위치 변경(벽에 닿으면 튕겨나오는 호과)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width :
            ball_val["to_x"] = ball_val["to_x"] * -1

        # 세로 위치
        # 공이 스테이지에 닿으면 튕겨서 오르는 
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: # 공이 포물선모양으로 움직이기 위한 코드(바닥에 튕기고 올라갈 때는 점점 속도 줄다가 떨어질 때는 점점 속도 빨라지게)
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]


    # 4. 충돌 처리 (두가지 경우 - 캐릭터와 공, 무기와 공)

    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        # 공 rect정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        
        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            break


        # 공과 무기들 충돌처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]
            
            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y


            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx
                break

    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove -1

    if weapon_to_remove >-1 :
        del weapons[weapon_to_remove]
        weapon_to_remove = -1
            



    #  5. 화면에 그리기
    # 코드 넣은 순서대로 화면에 그림(배경이 그래서 맨 아래에 깔리는거임)
    screen.blit(background, (0, 0)) 

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
        
    screen.blit(stage,(0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    



    pygame.display.update() 


pygame.quit()

