import sys
import board
import neopixel
pixel_number = 12
pixels = neopixel.NeoPixel(board.D21,pixel_number)
#D21 Sorunsuz calisiyor.

def parametre_kontrol(parametre):
    if parametre == "blue":
        for x in range(0,6,+1):
            pixels[x] = (0, 0, 255)

    elif parametre == "close":
        for x in range(0,6,+1):
            pixels[x] = (0, 0, 0)

    elif parametre == "green":
        for x in range(0,6,+1):
            pixels[x] = (0, 255, 0)

    elif parametre == "purple":
        for x in range(0,6,+1):
            pixels[x] = (255, 0, 255)

    elif parametre == "red":
        for x in range(0,6,+1):
            pixels[x] = (255, 0, 0)

    elif parametre == "white":
        for x in range(0,6,+1):
            pixels[x] = (255, 255, 255)

    elif parametre == "yellow":
        for x in range(0,6,+1):
            pixels[x] = (255, 255, 0)

    else:
        print("Bilinmeyen renk")


if len(sys.argv) > 1:
    parametre = sys.argv[1]
    parametre_kontrol(parametre)
else:
    print("Parametre bulunamadı.")