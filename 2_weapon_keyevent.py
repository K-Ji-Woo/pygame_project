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
weapon_speed = 10


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

    # 4. 충돌 처리


    #  5. 화면에 그리기
    # 코드 넣은 순서대로 화면에 그림(배경이 그래서 맨 아래에 깔리는거임)
    screen.blit(background, (0, 0)) 

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    screen.blit(stage,(0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    



    pygame.display.update() 


pygame.quit()

