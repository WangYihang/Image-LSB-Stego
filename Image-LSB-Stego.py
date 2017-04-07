#!/usr/bin/env python
# coding:utf-8

from optparse import OptionParser
from PIL import Image

RED = 0
GREEN = 1
BLUE = 2


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


def handleBit(char, bit, value):
    num = 1
    num <<= bit
    num ^= 0xFF
    char &= num
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


def encrypt(srcIm, message, CHANNEL, BIT):
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
            pixel[CHANNEL] = handleBit(
                pixel[CHANNEL], BIT, getBit(char, 7 - j))
            pixel = tuple(pixel)
            srcIm.putpixel((x, y), pixel)


def decrypt(srcIm, CHANNEL, BIT):
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
            bit = getBit(pixel[CHANNEL], BIT)
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
    parser = OptionParser()
    parser.add_option("-m", "--model", dest="model",
                      help="Encrypt model or Decrypt model, [e|d]")
    parser.add_option("-i", "--input", dest="input",
                      help="Filename to encrypt", metavar="FILE")
    parser.add_option("-o", "--output", dest="output",
                      help="Filename to output", metavar="FILE")
    parser.add_option("-c", "--channel", dest="channel",
                      help="Channel of image, use number : \
                        [0|1|2] to indicate [R|G|B]",
                      default=0)
    parser.add_option("-b", "--bit", dest="bit",
                      help="bit of the pixel's channel",
                      default=0)
    parser.add_option("-s", "--secret", dest="secret",
                      help="Your secret")
    (options, args) = parser.parse_args()

    channel = int(options.channel)
    bit = int(options.bit)
    model = options.model
    secret = options.secret
    inputFileName = options.input
    outputFileName = options.output

    if model == "e":
        print "Input : [%s]" % (inputFileName)
        print "Output : [%s]" % (outputFileName)
        im = Image.open(inputFileName)
        encrypt(im, secret, channel, bit)
        im.save(outputFileName)
    elif model == "d":
        print "Input : [%s]" % (inputFileName)
        print "Channel : [%d]" % (channel)
        print "Bit : [%d]" % (bit)
        im = Image.open(inputFileName)
        decrypt(im, channel, bit)
    else:
        print "Invalid parameter, use -h to show help"


if __name__ == "__main__":
    main()
