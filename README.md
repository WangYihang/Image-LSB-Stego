# Image-LSB-Stego


Usage : 
---

```
Usage: Image-LSB-Stego.py [options]

Options:
  -h, --help            show this help message and exit
  -m MODEL, --model=MODEL
                        Encrypt model or Decrypt model, [e|d]
  -i FILE, --input=FILE
                        Filename to encrypt
  -o FILE, --output=FILE
                        Filename to output
  -c CHANNEL, --channel=CHANNEL
                        Channel of image, use number :
                        [0|1|2] to indicate [R|G|B]
  -b BIT, --bit=BIT     bit of the pixel's channel
  -s SECRET, --secret=SECRET
                        Your secret
```

Example : 
---

> Encrypt : 

```
$ python Image-LSB-Stego.py -m e -i input.bmp -o output.bmp -s 'YourSecret' -c 0 -b 0
Input : [input.bmp]
Output : [output.bmp]
Message : [YourSecret]
```
> Decrypt : 

```
$ python Image-LSB-Stego.py -m d -i ./output.bmp -c 0 -b 0
Input : [./output.bmp]
Channel : [0]
Bit : [0]
YourSecretp.....
.........pip....
.. ...i.p.....p.
..y.O.y.........
..'..|.{.p.....(
p..`.....3......
...?..?.?...1..?
.......?...s..<.
```
