#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo, xiaomo
"""

import pygame
from sys import exit
from pygame.locals import *
import random

from gameCommon import *
from gameRole import *

def move_plane(player):
	# 监听键盘事件
	key_pressed = pygame.key.get_pressed()
	# 若玩家被击中，则无效
	if not player.is_hit:
		if key_pressed[K_w] or key_pressed[K_UP]:
			player.moveUp()
		if key_pressed[K_s] or key_pressed[K_DOWN]:
			player.moveDown()
		if key_pressed[K_a] or key_pressed[K_LEFT]:
			player.moveLeft()
		if key_pressed[K_d] or key_pressed[K_RIGHT]:
			player.moveRight()

def update_score(score):
	score_font = pygame.font.Font(None, 36)
	score_text = score_font.render(str(score), True, (128, 128, 128))
	text_rect = score_text.get_rect()
	text_rect.topleft = [10, 10]
	screen.blit(score_text, text_rect) 

def show_game_over(score):
	font = pygame.font.Font(None, 48)
	text = font.render('Score: '+ str(score), True, (255, 0, 0))
	text_rect = text.get_rect()
	text_rect.centerx = screen.get_rect().centerx
	text_rect.centery = screen.get_rect().centery + 24
	screen.blit(img_game_over, (0, 0))
	screen.blit(text, text_rect)

def wait_for_exit():
	try:
		pygame.display.update() 
		game_exit = False
		while not game_exit:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_exit = True
	finally:
		pygame.quit()        

def start_game():
	shoot_frequency = 0
	enemy_frequency = 0
	player_down_index = 16
	score = 0
	clock = pygame.time.Clock()
	running = True

	while running:
		# 控制游戏最大帧率为60
		clock.tick(60)

		# 控制发射子弹频率,并发射子弹
		if not player.is_hit:
			if shoot_frequency % 15 == 0:
				bullet_sound.play()
				player.shoot(bullet_img)
			shoot_frequency += 1
			if shoot_frequency >= 15:
				shoot_frequency = 0

		# 生成敌机
		if enemy_frequency % 50 == 0:
			enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
			enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
			enemies1.add(enemy1)
		enemy_frequency += 1
		if enemy_frequency >= 100:
			enemy_frequency = 0

		# 移动子弹，若超出窗口范围则删除
		for bullet in player.bullets:
			bullet.move()
			if bullet.rect.bottom < 0:
				player.bullets.remove(bullet)

		# 移动敌机，若超出窗口范围则删除
		for enemy in enemies1:
			enemy.move()
			# 判断玩家是否被击中
			if pygame.sprite.collide_circle(enemy, player):
				enemies_down.add(enemy)
				enemies1.remove(enemy)
				player.is_hit = True
				game_over_sound.play()
				break
			if enemy.rect.top < 0:
				enemies1.remove(enemy)

		# 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画
		enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
		for enemy_down in enemies1_down:
			enemies_down.add(enemy_down)

		# 绘制背景
		screen.fill(0)
		screen.blit(IMG_BACKGROUND, (0, 0))

		# 绘制玩家飞机
		if not player.is_hit:
			screen.blit(player.image[player.img_index], player.rect)
			# 更换图片索引使飞机有动画效果
			player.img_index = shoot_frequency / 8
		else:
			player.img_index = player_down_index / 8
			screen.blit(player.image[player.img_index], player.rect)
			player_down_index += 1
			if player_down_index > 47:
				running = False

		# 绘制击毁动画
		for enemy_down in enemies_down:
			if enemy_down.down_index == 0:
				enemy1_down_sound.play()
			if enemy_down.down_index > 7:
				enemies_down.remove(enemy_down)
				score += 1000
				continue
			screen.blit(enemy_down.down_imgs[enemy_down.down_index / 2], enemy_down.rect)
			enemy_down.down_index += 1

		# 绘制子弹和敌机
		player.bullets.draw(screen)
		enemies1.draw(screen)
		# 绘制得分
		update_score(score)
		# 更新屏幕
		pygame.display.update() 

		# 监听事件并移动飞机		
		move_plane(player)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()		

	# 显示游戏结束
	show_game_over(score)
	# 等待退出
	wait_for_exit()
		
if __name__=='__main__':
	start_game()
