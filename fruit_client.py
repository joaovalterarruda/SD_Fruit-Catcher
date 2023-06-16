import pygame
import random


class Fruit(pygame.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int, w_size: int, *groups):
        super().__init__(*groups)
        image_files = ["./frutas/ananas.png", "./frutas/banana.png", "./frutas/cereja.png", "./frutas/kiwi.png",
                       "./frutas/maca.png", "./frutas/uva.png"]
        selected_image = random.choice(image_files)
        self.image = pygame.image.load(selected_image)
        initial_size = self.image.get_size()
        size_rate = w_size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * w_size, pos_y * w_size), self.image.get_size())

    def get_size(self):
        return self.new_size

    def update(self):
        pass
