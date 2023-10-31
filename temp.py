import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(
            'graphics/player/sprite_cuteknight1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            'graphics/player/sprite_cuteknight2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(
            'graphics/player/sprite_knight_jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

    # self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
    # self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
        # self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'storm':
            storm_1 = pygame.image.load(
                'graphics/storm/sprite_storm1.png').convert_alpha()
            storm_2 = pygame.image.load(
                'graphics/storm/sprite_storm2.png').convert_alpha()
            storm_3 = pygame.image.load(
                'graphics/storm/sprite_storm3.png').convert_alpha()
            storm_4 = pygame.image.load(
                'graphics/storm/sprite_storm4.png').convert_alpha()
            storm_5 = pygame.image.load(
                'graphics/storm/sprite_storm5.png').convert_alpha()
            storm_6 = pygame.image.load(
                'graphics/storm/sprite_storm6.png').convert_alpha()
            storm_7 = pygame.image.load(
                'graphics/storm/sprite_storm7.png').convert_alpha()
            storm_8 = pygame.image.load(
                'graphics/storm/sprite_storm8.png').convert_alpha()
            self.frames = [storm_1, storm_2, storm_3, storm_4, storm_5, storm_6,
                           storm_7, storm_8]
            y_pos = 190
        else:
            snail_1 = pygame.image.load(
                'graphics/snail/sprite_snail1.png').convert_alpha()
            snail_2 = pygame.image.load(
                'graphics/snail/sprite_snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.scored = False
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

        if self.rect.right < 80 and not self.scored:  # if the object is behind the player's character
            global score

            score += 1
            self.scored = True

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    score_surf = test_font.render(f'Score: {score}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(storm_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if
                         obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
high_score = 0
# bg_music = pygame.mixer.Sound('audio/music.wav')
# bg_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/morninghill.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# score_surf = test_font.render('My game', False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400,50))

# Snail
snail_frame1 = pygame.image.load(
    'graphics/snail/sprite_snail1.png').convert_alpha()
snail_frame2 = pygame.image.load(
    'graphics/snail/sprite_snail2.png').convert_alpha()
snail_frames = [snail_frame1, snail_frame2, snail_frame2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Storm
storm_frame1 = pygame.image.load(
    'graphics/storm/sprite_storm1.png').convert_alpha()
storm_frame2 = pygame.image.load(
    'graphics/storm/sprite_storm2.png').convert_alpha()
storm_frame3 = pygame.image.load(
    'graphics/storm/sprite_storm3.png').convert_alpha()
storm_frame4 = pygame.image.load(
    'graphics/storm/sprite_storm4.png').convert_alpha()
storm_frame5 = pygame.image.load(
    'graphics/storm/sprite_storm5.png').convert_alpha()
storm_frame6 = pygame.image.load(
    'graphics/storm/sprite_storm6.png').convert_alpha()
storm_frame7 = pygame.image.load(
    'graphics/storm/sprite_storm7.png').convert_alpha()
storm_frame8 = pygame.image.load(
    'graphics/storm/sprite_storm8.png').convert_alpha()
storm_frames = [storm_frame1, storm_frame2, storm_frame3, storm_frame4,
                storm_frame5, storm_frame6, storm_frame7, storm_frame8]
storm_frame_index = 0
storm_surf = storm_frames[storm_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load(
    'graphics/player/sprite_cuteknight1.png').convert_alpha()
player_walk_2 = pygame.image.load(
    'graphics/player/sprite_cuteknight2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load(
    'graphics/player/sprite_knight_jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load(
    'graphics/player/sprite_knight_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Pawel Jumper', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 360))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

storm_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(storm_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(
                        event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(
                    Obstacle(choice(['storm', 'snail', 'snail', 'snail'])))
            # if randint(0,2):
            # 	obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
            # else:
            # 	obstacle_rect_list.append(storm_surf.get_rect(bottomright = (randint(900,1100),210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == storm_animation_timer:
                if storm_frame_index == 0:
                    storm_frame_index = 1
                else:
                    storm_frame_index = 0
                storm_surf = storm_frames[storm_frame_index]

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # pygame.draw.rect(screen,'#c0e8ec',score_rect)
        # pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
        # screen.blit(score_surf,score_rect)
        display_score()

        # snail_rect.x -= 4
        # if snail_rect.right <= 0: snail_rect.left = 800
        # screen.blit(snail_surf,snail_rect)

        # Player
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300: player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf,player_rect)
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collision_sprite()
    # game_active = collisions(player_rect,obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0
        if score > high_score:
            high_score = score
        score = 0

        score_message = test_font.render(f'Your score: {score}', False,
                                         (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        high_score_message = test_font.render(f'High Score: {high_score}',
                                              False, (111, 196, 169))
        high_score_message_rect = high_score_message.get_rect(center=(400, 320))
        screen.blit(high_score_message, high_score_message_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)