import pygame

def scale_image(image, scale):
    #Escala una imagen manteniendo sus proporciones
    w, h = image.get_width(), image.get_height()
    return pygame.transform.scale(image, (int(w * scale), int(h * scale)))
