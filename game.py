import pygame
import random

def game():
    #1. 게임 초기화
    pygame.mixer.init()
    pygame.init()
    
    #2. 게임창 옵션 설정
    SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 650
    SCREEN_FLOOR = 200
        #스크린 사이즈
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        #스크린 객체 생성
    screen = pygame.display.set_mode(size)
        #타이틀 설정
    title = "Teemo Adventure"
    pygame.display.set_caption(title)
        #favicon 설정
    icon = pygame.image.load('images/title_icon.png')
    pygame.display.set_icon(icon)
    
    #3. 게임 내 필요한 설정
    clock = pygame.time.Clock()#Clock()으로 객체생성
    FPS = 60  
        #배경
    background1 = pygame.image.load('images/map_1.png')
    background1 = pygame.transform.scale(background1, [SCREEN_WIDTH, SCREEN_HEIGHT])
    background_x = 0
        #사운드
    sfx_bgm = pygame.mixer.Sound('sounds/background.mp3')
    sfx_bgm.set_volume(0.2)
    sfx_bgm.play()
    sfx_jump = pygame.mixer.Sound('sounds/jump.wav')
    sfx_jump.set_volume(0.2)
    sfx_hide = pygame.mixer.Sound('sounds/hide.wav')
    sfx_hide.set_volume(0.2)
        #상태바
    status_bar = pygame.image.load('images/status_bar.png')
    time_display = pygame.image.load('images/time_display.png')
    timer_icon = pygame.image.load('images/timer_icon.png')
    timer_icon = pygame.transform.scale(timer_icon, (24, 24))
        #캐릭터 클래스
    class champion:
        def __init__(self, img_size, img_pwd, pos_x, pos_y, speed = 150):
            self.img = pygame.transform.scale(pygame.image.load(img_pwd), [img_size, img_size])
            self.rect = self.img.get_rect()
            self.size = self.rect.size#이미지 크기
            self.width = self.size[0]#캐릭터의 가로 크기
            self.height = self.size[1]#캐릭터의 세로 크기
            self.ground = SCREEN_HEIGHT - (SCREEN_FLOOR + self.height)
            self.pos_x = pos_x
            self.pos_y = self.ground - pos_y
            self.to_x = 0
            self.to_y= 0
            self.jumping = False
            self.velocity = 10 #점프속도
            self.speed = speed#이동속도
            
        def jump(self):
            if self.jumping is True:
                self.pos_y -= self.velocity*2
                self.velocity -= 0.8
                if self.velocity < -10:
                    self.jumping = False
                    self.velocity = 10
                    self.pos_y = self.ground
                    
    class minion:
        def __init__(self, img_size_x, img_size_y, img_pwd, pos_x, pos_y, speed = 100): 
            self.img = pygame.transform.scale(pygame.image.load(img_pwd), [img_size_x, img_size_y])
            self.rect = self.img.get_rect()
            self.size = self.rect.size#이미지 크기
            self.width = self.size[0]#캐릭터의 가로 크기
            self.height = self.size[1]#캐릭터의 가로 크기
            self.ground = SCREEN_HEIGHT - (SCREEN_FLOOR + self.height)
            self.pos_x = pos_x
            self.pos_y = self.ground - pos_y
            self.to_x = 0
            self.to_y= 0
            self.speed = speed#이동속도  
         #캐릭터 생성   
    teemo = champion(64, 'images/teemo.png', 100, 0)
    enermy = champion(128, 'images/enermy.png', SCREEN_WIDTH, 0, 50)
    minion1 = minion(48, 48, 'images/minion_1.png', SCREEN_WIDTH, 0, 150)
    minion2 = minion(48, 48, 'images/minion_2.png', SCREEN_WIDTH*1.3, 0, 130)
    cannon_minion = minion(120, 60, 'images/cannon_minion.png', SCREEN_WIDTH, 0, 100)
    # 티모 모션
    teemo_L = pygame.transform.scale(pygame.image.load('images/teemo_L.png'), [64, 64])
    teemo_stay_L = pygame.transform.scale(pygame.image.load('images/teemo_stay_L.png'), [64, 64])
    teemo_R = pygame.transform.scale(pygame.image.load('images/teemo.png'), [64, 64])
    teemo_stay_R = pygame.transform.scale(pygame.image.load('images/teemo_stay.png'), [64, 64])
    teemo_hide = pygame.transform.scale(pygame.image.load('images/teemo_hide.png'), [64, 64])
    teemo_demaged = pygame.transform.scale(pygame.image.load('images/teemo_demaged.png'), [64, 64])
    # 폰트 정의
    timer_font = pygame.font.SysFont(None, 40) # 폰트 객체 생성(폰트, 크기)
    distance_font = pygame.font.SysFont(None, 30)
    # 시간 계산
    start_ticks = pygame.time.get_ticks() # 현재 tick을 받아옴  
    # 체력 이벤트
    hp = []
    for i in range(0,5):
        hp.append(pygame.image.load('images/HP.png'))
        hp[i] = pygame.transform.scale(hp[i], (32, 32))
    hp_status = 0
    #충돌 변수
    collide = False
    crush_minion1 = False
    crush_minion2 = False
    crush_cannon_minion = False
    crush_enermy = False
    sturn_time = 0#1초(60fps) 스턴 구현
    #은신 변수
    hide_time = 0
    #총 거리 변수
    distance = 0
    target_distance = 50
    # 버섯
    mushroom = pygame.image.load('images/mushroom.png')
    mushroom = pygame.transform.scale(mushroom, (64, 64))
    mushroom_rect = mushroom.get_rect()
    mushroom_size = mushroom_rect.size
    mushroom_x = 0
    mushroom_y = mushroom_size[1]
    mushroom_pos_x = SCREEN_WIDTH - mushroom_x
    mushroom_pos_y = SCREEN_HEIGHT - (SCREEN_FLOOR + mushroom_y)
    mushroom.set_alpha(0)
    clear = False
    #4. 메인 이벤트###############################################################################
    playing = True
    while playing:
        
        #4-1. FPS 설정
        dt = clock.tick(FPS)#while문이 1초에 도는 횟수 . 게임화면의 초당 프레임 수
        
        #4-2. 각종 입력 감지
        for event in pygame.event.get():#이벤트리스트(큐)를 얻는 코드
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()   
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    teemo.to_x = 0
            keys = pygame.key.get_pressed()
    
        if keys[pygame.K_LEFT]:
            teemo.to_x = -(teemo.speed / dt)
            distance -= 1
            if (distance % 30) < 15:    
                teemo.img = teemo_stay_L
            else:
                teemo.img = teemo_L
        if keys[pygame.K_RIGHT]:
            teemo.to_x = teemo.speed / dt
            distance += 1
            if (distance % 30) < 15:    
                teemo.img = teemo_stay_R
            else:
                teemo.img = teemo_R
        if keys[pygame.K_SPACE]:
            teemo.jumping = True
        if not any(keys):
            hide_time += 1
        elif any(keys):
            hide_time = 0
        total_distance = distance // 60
        if target_distance == 0:
            target_distance = 0
        distance_info = str(int(target_distance - total_distance)) + 'm left'
        distance_show = distance_font.render(distance_info, True, (0, 0, 0))
        # 티모 점프 구현
        if teemo.jumping is True:
            if teemo.velocity == 9.2:
                sfx_jump.play()
            teemo.jump()
            
        #4-3. 입력, 시간에 따른 변화
        # 타이머 집어넣기
            # 경과 시간 계산
        total_time = (pygame.time.get_ticks() - start_ticks) / 1000 
            # 경과 시간을 1000으로 나눠 초단위로 표시
        display_time = str(int(total_time)) + '\''
        timer = timer_font.render(display_time, True, (0, 0, 0))
        if total_time > 10:
            time_x = 48
        elif total_time <= 10:
            time_x = 52
       
        #이벤트에 따른 티모 포지션 변경
        teemo.pos_x += teemo.to_x
        teemo.pos_y += teemo.to_y
        
            #티모 이동에 따른 변화
        if teemo.pos_x < 0:
            teemo.pos_x = 0
        if total_distance < target_distance-1:
            if teemo.pos_x > (SCREEN_WIDTH / 2) - teemo.width:
                teemo.pos_x = (SCREEN_WIDTH / 2) - teemo.width
                background_x -= 5
                if background_x < -SCREEN_WIDTH:
                    background_x = 0
        elif total_distance >= target_distance-1:
            if mushroom_x <= mushroom_size[0]:
                mushroom_x += 10
            mushroom.set_alpha(255)  
            mushroom_rect.left = mushroom_pos_x
            mushroom_rect.bottom = mushroom_pos_y
            if teemo.rect.colliderect(mushroom_rect):
                playing = False
                clear = True
        if teemo.pos_y < 0:
            teemo.pos_y = 0
        elif teemo.pos_y > teemo.ground:
            teemo.pos_y = teemo.ground
            #y축
            
        #티모 렉트 정보 가져옴
        teemo.rect.left = teemo.pos_x
        teemo.rect.bottom = teemo.pos_y
        # 적 렉트 정보 가져옴
        enermy.rect.left = enermy.pos_x
        enermy.rect.bottom = enermy.pos_y
        #미니언 렉트 정보 가져옴
        minion1.rect.left = minion1.pos_x#위치 업데이트
        minion1.rect.bottom = minion1.pos_y
        minion2.rect.left = minion2.pos_x#위치 업데이트
        minion2.rect.bottom = minion2.pos_y
        cannon_minion.rect.left = cannon_minion.pos_x#위치 업데이트
        cannon_minion.rect.bottom = cannon_minion.pos_y
        
        
        # 미니언1 이동
        if total_time > 0:
            minion1.pos_x -= (minion1.speed / dt)
            if minion1.pos_x < -(SCREEN_WIDTH * random.randint(2, 5)):
                minion1.pos_x = SCREEN_WIDTH
        #미니언2 이동
        if total_time > 3: 
            minion2.pos_x -= (minion2.speed / dt)
            if minion2.pos_x < -(SCREEN_WIDTH * random.randint(2, 4)):  
                minion2.pos_x = SCREEN_WIDTH
        #대포 미니언 이동
        if total_time > 10: 
            cannon_minion.pos_x -= (cannon_minion.speed / dt)
            if cannon_minion.pos_x < -(SCREEN_WIDTH * random.randint(2, 4)):  
                cannon_minion.pos_x = SCREEN_WIDTH
        #적 이동
        rand_num = random.randint(0, 60)
        if total_time > 15:
            enermy.pos_x -= (enermy.speed / dt)
            if rand_num == 12:
               enermy.jumping = True
            if enermy.pos_x < -(SCREEN_WIDTH * random.randint(3, 5)):  
                enermy.pos_x = SCREEN_WIDTH
        if enermy.jumping is True:
            enermy.jump()
        # 충돌/은신 처리##############################################
        sturn_time += 1 #60프레임(1초)간 충돌 방지
        if hide_time < 90:
            if sturn_time > 60:
                if collide is False:
                     #미니언1 충돌
                    if teemo.rect.colliderect(minion1.rect):
                        if hp_status < 4:
                            hp[hp_status] = pygame.image.load('images/HP_no.png')
                            hp[hp_status] = pygame.transform.scale(hp[hp_status], (32, 32))
                            hp_status += 1
                            crush_minion1 = True
                            collide = True
                            sturn_time = 0
                            hide_time = 0
                        elif hp_status >= 4:
                            playing = False
                     #미니언2 충돌
                    if teemo.rect.colliderect(minion2.rect):
                        if hp_status < 4:
                            hp[hp_status] = pygame.image.load('images/HP_no.png')
                            hp[hp_status] = pygame.transform.scale(hp[hp_status], (32, 32))
                            hp_status += 1
                            crush_minion2 = True
                            collide = True
                            sturn_time = 0
                            hide_time = 0
                        elif hp_status >= 4:
                            playing = False
                     #대포 미니언 충돌
                    if teemo.rect.colliderect(cannon_minion.rect):
                        if hp_status < 4:
                            hp[hp_status] = pygame.image.load('images/HP_no.png')
                            hp[hp_status] = pygame.transform.scale(hp[hp_status], (32, 32))
                            hp_status += 1
                            crush_cannon_minion = True
                            collide = True
                            sturn_time = 0
                            hide_time = 0
                        elif hp_status >= 4:
                            playing = False
                     #적챔피언 충돌
                    if teemo.rect.colliderect(enermy.rect):
                        if hp_status < 4:
                            hp[hp_status] = pygame.image.load('images/HP_no.png')
                            hp[hp_status] = pygame.transform.scale(hp[hp_status], (32, 32))
                            hp_status += 1
                            crush_enermy = True
                            collide = True
                            sturn_time = 0
                            hide_time = 0
                        elif hp_status >= 4:
                            playing = False
                # 충돌 후 처리
                if collide is True:
                    if crush_minion1 is True:
                        if not teemo.rect.colliderect(minion1.rect):
                            collide = False
                            crush_minion1 = False
                    if crush_minion2 is True:
                        if not teemo.rect.colliderect(minion2.rect):
                            collide = False
                            crush_minion2 = False
                    if crush_cannon_minion is True:
                        if not teemo.rect.colliderect(cannon_minion.rect):
                            collide = False
                            crush_cannon_minion = False
                    if crush_enermy is True:
                        if not teemo.rect.colliderect(enermy.rect):
                            collide = False
                            crush_enermy = False
            elif total_time > 2 and sturn_time <= 60:
                teemo.img = teemo_demaged
        if hide_time >= 90:
            if hide_time == 90:
                sfx_hide.play()
            teemo.img = teemo_hide
        
        #4-4. 그리기
        screen.blit(background1, (background_x, 0))
        screen.blit(background1, (SCREEN_WIDTH + background_x, 0))
        screen.blit(teemo.img, (teemo.pos_x, teemo.pos_y))
        screen.blit(minion1.img, (minion1.pos_x, minion1.pos_y))
        screen.blit(minion2.img, (minion2.pos_x, minion2.pos_y))
        screen.blit(cannon_minion.img, (cannon_minion.pos_x, cannon_minion.pos_y))
        screen.blit(enermy.img, (enermy.pos_x, enermy.pos_y))
        screen.blit(time_display, (0, 0))
        screen.blit(timer, (time_x, 15))
        screen.blit(timer_icon, (20, 15))
        screen.blit(status_bar,(275,530))
        screen.blit(distance_show, (910, 15))
        screen.blit(mushroom, (SCREEN_WIDTH - mushroom_x, SCREEN_HEIGHT - (SCREEN_FLOOR + mushroom_y)))
        for i in range(0, 5):
            screen.blit(hp[i], (385+(50*i), 585))
        #4-5. 업데이트
        pygame.display.update()
    #5. 게임 종료
    if playing is False:
        sfx_bgm.stop()
        return (True, total_time, hp_status, clear)
    pygame.quit()