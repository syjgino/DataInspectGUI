# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 10:55:46 2021

@author: BaolongSu
"""

tcode = b"eJxjYIAAkQsuNz58uWEPoV/Y888xXrRl+yco/4e9JEsYn67Rf6g4k4Ogmc3eoGusDhB5DgexLN/PfcI8DhB1/A731E3MEjUEHe6X7HDesF3I4eFBm8D/biIOj/gOxvldE3V4HO2aMzdV3OHJipOVb75IOGw7d0nDvEXKYbt0uFmbsIzDzozbzlcXyToAAOHxQyY="
tcode2 = b'eJwlU39IU1EUvlGURuGQGkYGg5pElKn9QEe1N0ZhKGs9YRVtq1XaKtPpss1UeumMmrkJ1TSWtdoCiX4IIyoheJHRJJSnuNSG5CJQjJwZloJR3O/+9XG+c75z7vlxCSGKxOADDSFkzP24niJR9Kyl6LwfA09yuusoCivSjlPkDk7VUBTbdXfh1//ZBX5ThwA72qenqHhe2UwxYGq7BT518W7k4ZMM0L/TXgbvupMJO2PpTejSPrYg7ne4BHmDX6oRl29eRzHydcEPXu6GXvxcW4460fIqxE3z6cijClZQHA7JW1l/HryPsyTZoJOSWfzEMPoNjBgvwW9s88Hf8xM2uSCpgYl55BMSe6An/IdcxH07fYXihCflNviMRifijvqOwe6aPwP7/YbzsJ/lcMDZvgaKrw7rMJ+xBqWD6Uwn4M/cfg7vGXdCT6q00MmaTmI+kkV5A32GOtAHV+eFTvGpzI53DQ5hX0TsQn9c7AfyWJdHoNe7HrrBFxSfQnx+GPWI918F22sQe+IWZi4C7b1e5F/deA3xv6zsHnJ3svl/f8l0r2PYv+jyYT/TytEm9Le5FfXIqvh+tqcDOxC3fo7NZ+++SvBqqQj53voxV1J9DzrZUz/Tp/fj3khhRAv9tuRS6NdYyoDt/CG8yytdp9jS60CezmXdTN/Mob4gHzcBC1OK2X3x6IO8cOgo2iZlmK8QmcOeAgVTV+F/kpUHvt4AnWgqxZ2K6pVsftJGDfyzMx7oUg2oqxgpqoV/IM72aYieZXf0iO3bd0QFDJWg/86BLfg/NqsacxeX/GV3q65BnQCfB1uIG83gh95YwcdG0XdgUT/qi6ow4rjsbMyJ2CdZn1lbzZr/QoUKFw=='
tcode3 = b'eJxjYAABEwcwxRACpV3QaHRxGN8ETRzGhwE/HOrR9aHTfnB1AP1uCcE='

import base64, struct
raw1 = base64.decodebytes(tcode)
raw2 = base64.decodebytes(tcode2)
raw3 = base64.decodebytes(tcode3)
#struct.unpack('<%sd' % (len(raw1) // 8), raw1)
zlibraw1 = zlib.decompress(raw1)
zlibraw2 = zlib.decompress(raw2)
zlibraw3 = zlib.decompress(raw3)
aa = struct.unpack('<%sd' % (len(zlibraw1) // 8), zlibraw1)
tic = struct.unpack('<%sd' % (len(zlibraw2) // 8), zlibraw2)
bb = struct.unpack('<%sd' % (len(zlibraw3) // 8), zlibraw3)