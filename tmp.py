from firefly_test import Color


def trip(v: int):
    c = Color.from_rgb24(v)
    print(f'{v:06X} {c}')


trip(0x1A1C2C)
trip(0x5D275D)
trip(0xB13E53)
trip(0xEF7D57)
trip(0xFFCD75)
trip(0xA7F070)
trip(0x38B764)
trip(0x257179)
trip(0x29366F)
trip(0x3B5DC9)
trip(0x41A6F6)
trip(0x73EFF7)
trip(0xF4F4F4)
trip(0x94B0C2)
trip(0x566C86)
trip(0x333C57)
trip(0x000000)
trip(0xFFFFFF)
trip(0xFF0000)
trip(0x00FF00)
trip(0x0000FF)
