"""
This script is used to generate 5000 levels of varying difficulty and store
them in a JSON file. This script is used to train the AI to generate similar
kinds of levels
"""
import json
import pygame
from levels.LevelGenerator import LevelGenerator

temp_easy = []
temp_medium = []
temp_hard = []

easy = []
medium = []
hard = []

generator = LevelGenerator(0)

for i in range(20):
    generator.difficulty = 0
    generator.generate_level()
    temp_easy.append(generator.current_level)
    generator.clear_level()
    generator.difficulty = 1
    generator.generate_level()
    temp_medium.append(generator.current_level)
    generator.clear_level()
    generator.difficulty = 2
    generator.generate_level()
    temp_hard.append(generator.current_level)
    generator.clear_level()

print("levels are generated")
print("formatting Data to fit JSON")
targets = [temp_easy, temp_medium, temp_hard]
for target_id in range(len(targets)):
    for level in targets[target_id]:
        level_temp = []
        for shape in level:
            temp = {
                "shape_type": shape.shape_type,
                "color": shape.color,
                "free_edges": shape.free_edges,
                "all_edges": shape.all_edges,
                "index": shape.index,
                "circles_attached": shape.circles_attached,
            }
            if shape.shape_type == "triangle":
                temp["p1"] = shape.p1
                temp["p2"] = shape.p2
                temp["p3"] = shape.p3
            elif shape.shape_type == "square" or shape.shape_type == "rhombus":
                temp["p1"] = shape.p1
                temp["p2"] = shape.p2
                temp["p3"] = shape.p3
                temp["p4"] = shape.p4
            elif shape.shape_type == "circle":
                temp["center"] = shape.center
                temp["radius"] = shape.radius
            level_temp.append(temp)
        if target_id == 0:
            easy.append(level_temp)
        elif target_id == 1:
            medium.append(level_temp)
        elif target_id == 2:
            hard.append(level_temp)

print("dumping data to JSON")
print(len(easy), len(medium), len(hard))
with open("assets/levels/easy.json", "w") as f:
    json.dump(easy, f)

with open("assets/levels/medium.json", "w") as f:
    json.dump(medium, f)

with open("assets/levels/hard.json", "w") as f:
    json.dump(hard, f)

# now we draw the surface and the shapes to it and export them as images
print("Exporting images")
count = 0
easy_count = 0
medium_count = 0
hard_count = 0
for target_id in range(3):
    for level in targets[target_id]:
        count += 1
        surface = pygame.Surface((700, 700), pygame.SRCALPHA, 32)
        surface.fill((255, 255, 255, 0))
        for shape in level:
            if shape.shape_type == "triangle":
                pygame.draw.polygon(
                    surface,
                    shape.color,
                    [shape.p1, shape.p2, shape.p3],
                    0,
                )
            elif shape.shape_type == "square":
                pygame.draw.polygon(
                    surface,
                    shape.color,
                    [shape.p1, shape.p2, shape.p3, shape.p4],
                    0,
                )
            elif shape.shape_type == "circle":
                pygame.draw.circle(
                    surface,
                    shape.color,
                    shape.center,
                    shape.radius,
                    0,
                )
            elif shape.shape_type == "rhombus":
                pygame.draw.polygon(
                    surface,
                    shape.color,
                    [shape.p1, shape.p2, shape.p3, shape.p4],
                    0,
                )
        if target_id == 0:
            easy_count += 1
            pygame.image.save(surface, "assets/levels/easy/" + str(easy_count) + ".png")
        elif target_id == 1:
            medium_count += 1
            pygame.image.save(
                surface, "assets/levels/medium/" + str(medium_count) + ".png"
            )
        elif target_id == 2:
            hard_count += 1
            pygame.image.save(surface, "assets/levels/hard/" + str(hard_count) + ".png")
