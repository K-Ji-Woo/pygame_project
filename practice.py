import pygame
import os

from pygame.constants import K_LEFT, K_RIGHT

pygame.init()

screen_width = 640
screen_height = 480 
screen = pygame.display.set_mode((screen_width, screen_height))


pygame.display.set_caption("Nado Pang") 


clock = pygame.time.Clock()


current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

# 배경
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]
stage_y_pos = screen_height - stage_height

# 캐릭터
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width)
character_y_pos = screen_height - stage_height - character_height

# 캐릭터 이동 관련
character_to_x = 0
character_speed = 0.5

# 무기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []
weapon_speed = 4

# 공
balls_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png")) ]

ball_speed_y = [-18, -15, -12, -9]

balls = []

balls.append({
    "pos_x" : 5,
    "pos_y" : 5, # 처음에 공이 어디에서 생길지
    "img_idx" : 0, # 공 크기는 어떤지
    "to_x" : 3, # 공이 좌 우로 움직이는 속도
    "to_y" : -6, # 공이 생겼을 때 약간 위로 올라갔다가 내려옴
    "init_spd_y" : ball_speed_y[0] }) # 공이 바닥에 튕겼다가 올라가는 속도





running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + character_width / 2 - weapon_width / 2
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])


        if event.type == pygame.KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                character_to_x = 0

    # 캐릭터 위치
    character_x_pos += character_to_x * dt

    # 캐릭터 화면 내 유지
    if character_x_pos < 0 :
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]

    # 무기 천장에 닿으면 사라짐
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]


    for ball_index, ball_value in enumerate(balls):
        ball_pos_x = ball_value["pos_x"]
        ball_pos_y = ball_value["pos_y"]
        ball_img_idx = ball_value["img_idx"]

    ball_size = balls_images[ball_img_idx].get_rect().size
    ball_width = ball_size[0]
    ball_height = ball_size[1]

    if ball_pos_x == 0 or ball_pos_x > screen_width - ball_width:
        ball_value["to_x"] *= -1

    if ball_pos_y >= screen_height - stage_height - ball_height:
        ball_value["to_y"] = ball_value["init_spd_y"]
    else:
        ball_value["to_y"] += 1

    ball_value["pos_x"] += ball_value["to_x"]
    ball_value["pos_y"] += ball_value["to_y"]
        


    
    screen.blit(background, (0 , 0))
    
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = ball_value["pos_x"]
        ball_pos_y = ball_value["pos_y"]
        ball_img_idx = ball_value["img_idx"]
        screen.blit(balls_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0 , stage_y_pos))
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update()







pygame.quit()