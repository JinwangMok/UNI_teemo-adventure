import pygame
import game
import imp
imp.reload(game)

#초기화
pygame.mixer.init()
pygame.init()

#스크린 생성
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 650
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
title = "Teemo Adventure"
pygame.display.set_caption(title)
icon = pygame.image.load('images/title_icon.png')
pygame.display.set_icon(icon)

#시간 생성
clock = pygame.time.Clock()
FPS = 60

#인트로 관련
intro_animation = []
intro_animation.append(pygame.transform.scale(pygame.image.load('images/intro_1.png'), [SCREEN_WIDTH, SCREEN_HEIGHT]))
intro_animation.append(pygame.transform.scale(pygame.image.load('images/intro_2.png'), [SCREEN_WIDTH, SCREEN_HEIGHT]))
intro_animation.append(pygame.transform.scale(pygame.image.load('images/intro_3.png'), [SCREEN_WIDTH, SCREEN_HEIGHT]))
intro_animation.append(pygame.transform.scale(pygame.image.load('images/intro_4.png'), [SCREEN_WIDTH, SCREEN_HEIGHT]))
intro_animation.append(pygame.transform.scale(pygame.image.load('images/intro_5.png'), [SCREEN_WIDTH, SCREEN_HEIGHT]))

intro_font = pygame.font.SysFont(None, 35)
current_intro = 0
intro_comment_var = 0
intro = True

sfx_intro_bgm = pygame.mixer.Sound('sounds/teemo_song.wav')
sfx_intro_bgm.set_volume(0.2)
sfx_intro_bgm.play()

#종료 관련
result_img = pygame.transform.scale(pygame.image.load('images/result.png'), (600, 450))
result_font_info = pygame.font.SysFont(None, 35)
result_font_button = pygame.font.SysFont(None, 50)
result_clear_or_not = pygame.font.SysFont(None, 70)
hp = pygame.transform.scale(pygame.image.load('images/HP_no.png'), (32, 32))

replay_button = pygame.Surface((230, 78))
replay_button.set_alpha(0)
replay_button.fill((255, 255, 255))
exit_button = pygame.Surface((230, 78))
exit_button.set_alpha(0)
exit_button.fill((255, 255, 255))

sfx_clear = pygame.mixer.Sound('sounds/game_clear.wav')
sfx_clear.set_volume(0.075)
clear_sound_var = True

#게임 조작법
info_img = pygame.transform.scale(pygame.image.load('images/info.png'), [SCREEN_WIDTH, SCREEN_HEIGHT])
info = True
info_comment_var = 0

#메인 루프
playing = True
while playing:
    dt = clock.tick(FPS)
    #인트로
    while intro:
        current_intro += 0.1
        current_intro %= 5
        intro_comment_var += 1
        if int(intro_comment_var) % 120 < 90:
            intro_comment = "Please press any key"
        else:
            intro_comment = None
        intro_text = intro_font.render(intro_comment, True, (255, 255, 255))
        for event in pygame.event.get():#이벤트리스트(큐)를 얻는 코드
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()   
            if event.type == pygame.KEYDOWN:
                intro = False
        screen.blit(intro_animation[int(current_intro)], (0, 0))
        screen.blit(intro_text, (370, 600))
        pygame.display.update()
    #조작법
    while info:
        info_comment_var += 1
        if int(info_comment_var) % 120 < 90:
            info_comment = "If you ready, please press key to start!!"
        else:
            info_comment = None
        info_text = intro_font.render(info_comment, True, (255, 255, 255))
        for event in pygame.event.get():#이벤트리스트(큐)를 얻는 코드
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()   
            if event.type == pygame.KEYDOWN:
                info = False
                sfx_intro_bgm.stop()
        screen.blit(info_img, (0, 0))
        screen.blit(info_text, (280, 600))
        pygame.display.update()
            
    # 게임 실행
    result, result_time, result_hp, clear = game.game()
    #종료 화면
    total_result_text = ''
    total_result_color = [0, 0 ,0]
    while result:
        replay_rect = screen.blit(replay_button, (260,380))
        exit_rect = screen.blit(exit_button, (506,380))
        for event in pygame.event.get():#이벤트리스트(큐)를 얻는 코드
            if event.type == pygame.QUIT:
                pygame.quit()   
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if replay_rect.collidepoint(pos):
                    playing = True
                elif exit_rect.collidepoint(pos):
                    playing = False
                    pygame.quit()
                result = False
        if clear is True:
            if clear_sound_var is True:
                sfx_clear.play(0)
                clear_sound_var = False
            total_result_text = 'C L E A R'
            total_result_color = [0, 200, 0]
        elif clear is False:
            total_result_text = 'F A L S E'
            total_result_color = [200, 0, 0]
        result_info_time_text = 'Play Time :           ' + str(int(result_time)) + ' sec'
        result_info_time = result_font_info.render(result_info_time_text, True, (0, 0, 0))
        result_info_hp = result_font_info.render('Spended HP : ', True, (0, 0, 0))
        result_button_replay = result_font_button.render('replay()', True, (255, 255, 255))
        result_button_exit = result_font_button.render('exit()', True, (255, 255, 255))
        total_result = result_clear_or_not.render(total_result_text, True, total_result_color)
        
        screen.fill((0,0,0))
        screen.blit(result_img, (200, 50))
        screen.blit(result_info_time, (280, 190))
        screen.blit(result_info_hp, (280, 250))
        for i in range(0, result_hp):
            screen.blit(hp, (485+(40*i), 250))
        screen.blit(total_result,(400, 310))
        screen.blit(result_button_replay,(315, 400))
        screen.blit(result_button_exit,(580, 400))
        
        pygame.display.update()
        
pygame.quit()