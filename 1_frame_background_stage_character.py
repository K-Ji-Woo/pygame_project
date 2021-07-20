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


running = True 
while running:
    dt = clock.tick(60) 

    # 2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 


    # 3. 게임 캐릭터 위치 정의



    # 4. 충돌 처리


    #  5. 화면에 그리기
    screen.blit(background, (0, 0)) 
    screen.blit(stage,(0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))



    pygame.display.update() 


pygame.quit()

