#!/usr/bin/env python
# coding:utf-8

from PIL import Image

RED = 0
GREEN = 1
BLUE = 2
CHANNEL = RED


def showBit(char):
    bit0 = getBit(char, 0)
    bit1 = getBit(char, 1)
    bit2 = getBit(char, 2)
    bit3 = getBit(char, 3)
    bit4 = getBit(char, 4)
    bit5 = getBit(char, 5)
    bit6 = getBit(char, 6)
    bit7 = getBit(char, 7)
    return "%d%d%d%d%d%d%d%d" % \
        (bit7, bit6, bit5, bit4, bit3, bit2, bit1, bit0)


def showPixel(pixel):
    return "[%s][%s][%s]" % \
        (showBit(pixel[0]), showBit(pixel[1]), showBit(pixel[2]))


def getBit(char, index):
    return (char >> index & 1)


def handleLowBit(char, value):
    char &= 0b11111110
    char |= value
    return char


def p2i(x, y, width):
    return x * width + y


def i2p(i, width):
    return i % width, i / width


def showPixels(srcIm):
    height = srcIm.size[1]
    width = srcIm.size[0]
    number = width * height
    for i in xrange(0, number, 8):
        for j in range(8):
            x = i2p(i + j, width)[0]
            y = i2p(i + j, width)[1]
            if y >= height:
                return
            pixel = list(srcIm.getpixel((x, y)))
            print showPixel(pixel)


def encrypt(srcIm, message):
    height = srcIm.size[1]
    width = srcIm.size[0]
    number = width * height
    counter = 0
    for i in xrange(0, number, 8):
        if counter == len(message):
            break
        counter += 1
        char = ord(message[i / 8])
        for j in range(8):
            x = i2p(i + j, width)[0]
            y = i2p(i + j, width)[1]
            if y >= height:
                return
            pixel = list(srcIm.getpixel((x, y)))
            pixel[CHANNEL] = handleLowBit(pixel[CHANNEL], getBit(char, 7 - j))
            pixel = tuple(pixel)
            srcIm.putpixel((x, y), pixel)


def decrypt(srcIm):
    height = srcIm.size[1]
    width = srcIm.size[0]
    number = width * height
    line = ""
    for i in xrange(0, number, 8):
        if len(line) == 16:
            print "%s" % (unprintable(line))
            line = ""
        char = 0
        for j in range(8):
            x = i2p(i + j, width)[0]
            y = i2p(i + j, width)[1]
            if y >= height:
                return
            pixel = list(srcIm.getpixel((x, y)))
            bit = getBit(pixel[CHANNEL], 0)
            char |= (bit << 7 - j)
        line += chr(char)


def unprintable(content):
    result = ""
    for i in content:
        if ord(i) < 0x20 or ord(i) > 0x7f:
            result += "."
        else:
            result += i
    return result


def main():
    # message = "Why are you so diao?"
    srcIm = Image.open("data.bmp")
    # encrypt(srcIm, message)
    decrypt(srcIm)
    # srcIm.save("data.bmp")


if __name__ == "__main__":
    main()
