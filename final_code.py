#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 10:47:06 2024

@author: yoojinoh
"""

import pygame
import csv
import pandas as pd
import random

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Read aloud and picture naming experiment")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define fonts
font = pygame.font.SysFont("AppleGothic", 24)

#Read stimuli from excel file
stimuli_df = pd.read_excel("stimuli.xlsx")

# Extract sentences and picture filenames
sentences = stimuli_df["read"].tolist()
pictures = stimuli_df["picture"].tolist()

# Combine sentences and pictures into pairs
stimulus_pairs = list(zip(sentences, pictures))

# Shuffle the indices of the pairs
indices = list(range(len(stimulus_pairs)))
random.shuffle(indices)

# Shuffle sentences and pictures based on the shuffled indices
shuffled_sentences = [stimulus_pairs[i][0] for i in indices]
shuffled_pictures = [stimulus_pairs[i][1] for i in indices]

# Instructional pages
instruction_1 = "Welcome to the experiment. Today you will read some words or name some pictures in Korean and English. Press any key to read more instructions."
instruction_2 = "When you see a string of words, please read them out loud as they are written. This may either be in Korean or English. When you see a picture, please name it in ENGLISH. Press any key to continue"
instruction_3 = "Please ask any questions you may have before you begin. When you are ready, press any key to start."

# Render instructional text surfaces
instruction_surface_1 = font.render(instruction_1, True, BLACK)
instruction_surface_2 = font.render(instruction_2, True, BLACK)
instruction_surface_3 = font.render(instruction_3, True, BLACK)

# Function to render text with line breaks
def render_text_with_line_breaks(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    lines.append(current_line)
    surfaces = [font.render(line, True, BLACK) for line in lines]
    return surfaces

def display_instruction(instruction_surfaces):
    screen.fill(WHITE)
    y_offset = (screen_height - sum(surface.get_height() for surface in instruction_surfaces)) / 2
    for surface in instruction_surfaces:
        screen.blit(surface, ((screen_width - surface.get_width()) / 2, y_offset))
        y_offset += surface.get_height()  # Adjust y offset for the next line
    pygame.display.flip()
    wait_for_key()

# Function to wait for a key press
def wait_for_key():
    key_pressed = False
    while not key_pressed:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_pressed = True

# Display instructional pages with line breaks
display_instruction(render_text_with_line_breaks(instruction_1, font, screen_width))
display_instruction(render_text_with_line_breaks(instruction_2, font, screen_width))
display_instruction(render_text_with_line_breaks(instruction_3, font, screen_width))


# Experiment parameters
fixation_time = 300  # in milliseconds
sentence_time = 10000  # in milliseconds
inter_stimulus_interval = 0  # in milliseconds
picture_time = 10000  # in milliseconds
inter_trial_interval = 0  # in milliseconds

# Main experiment loop
reaction_times = []
for trial_index in range(len(shuffled_sentences)):
    print("start trial")
    # Fixation cross
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, (screen_width/2 - 20, screen_height/2), (screen_width/2 + 20, screen_height/2), 3)
    pygame.draw.line(screen, BLACK, (screen_width/2, screen_height/2 - 20), (screen_width/2, screen_height/2 + 20), 3)
    pygame.display.flip()
    pygame.time.wait(fixation_time)

    # Sentence presentation
    screen.fill(WHITE)
    sentence_text = font.render(shuffled_sentences[trial_index], True, BLACK)
    screen.blit(sentence_text, ((screen_width - sentence_text.get_width()) / 2, (screen_height - sentence_text.get_height()) / 2))
    pygame.display.flip()
    start_time = pygame.time.get_ticks()
    
    key_pressed = False
    while pygame.time.get_ticks() - start_time < sentence_time:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_pressed = True
                print("pressed key - sentence")
                break
        if key_pressed:
            break
    pygame.time.wait(inter_stimulus_interval)
    
    
    # Picture presentation
    screen.fill(WHITE)
    picture = pygame.image.load(shuffled_pictures[trial_index])
    picture = pygame.transform.scale(picture, (400, 300))
    screen.blit(picture, ((screen_width - picture.get_width()) / 2, (screen_height - picture.get_height()) / 2))
    pygame.display.flip()
    start_time = pygame.time.get_ticks()
    
    key_pressed = False
    while pygame.time.get_ticks() - start_time < picture_time:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_pressed = True
                reaction_time = pygame.time.get_ticks() - start_time
                reaction_times.append(reaction_time)
                print("Reaction time: ", reaction_time, "ms")
                print("pressed key - picture")
                break
        if key_pressed:
            break
    pygame.time.wait(inter_trial_interval)
    
# Save reaction times to CSV file
with open('reaction_times.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Trial", "Reaction Time (ms)", "Switch", "Complex"])
    for i, reaction_time in enumerate(reaction_times):
        switch_column = stimuli_df.loc[i, "switch"]
        complex_column = stimuli_df.loc[i, "complex"]
        writer.writerow([i+1, reaction_time, switch_column, complex_column])


# Quit pygame
pygame.quit()
