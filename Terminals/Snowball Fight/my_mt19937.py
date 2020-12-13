#!/usr/bin/env python3
#
# mt19937.py - a quick and dirty implementation of the MT19937 PRNG in Python
#
#    Copyright (C) 2020  Tom Liston - email: tom.liston@bad-wolf-sec.com
#                                   - twitter: @tliston
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see [http://www.gnu.org/licenses/].

## cut and edited for holiday hack 2020 ##
import random

# this is simply a python implementation of a standard Mersenne Twister PRNG.
# the parameters used, implement the MT19937 variant of the PRNG, based on the
# Mersenne prime 2^19937−1
# see https://en.wikipedia.org/wiki/Mersenne_Twister for a very good explanation
# of the math behind this...

class mt19937():
    u, d = 11, 0xFFFFFFFF
    s, b = 7, 0x9D2C5680
    t, c = 15, 0xEFC60000
    l = 18
    n = 624

    def my_int32(self, x):
        return(x & 0xFFFFFFFF)

    def __init__(self, seed):
        w = 32
        r = 31
        f = 1812433253
        self.m = 397
        self.a = 0x9908B0DF
        self.MT = [0] * self.n
        self.index = self.n + 1
        self.lower_mask = (1 << r) - 1
        self.upper_mask = self.my_int32(~self.lower_mask)
        self.MT[0] = self.my_int32(seed)
        for i in range(1, self.n):
            self.MT[i] = self.my_int32((f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (w - 2))) + i))

    def extract_number(self):
        if self.index >= self.n:
            self.twist()
            self.index = 0
        y = self.MT[self.index]
        # this implements the so-called "tempering matrix"
        # this, functionally, should alter the output to
        # provide a better, higher-dimensional distribution
        # of the most significant bits in the numbers extracted
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        self.index += 1
        return self.my_int32(y)

    def twist(self):
        for i in range(0, self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if(x % 2) != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA


# so... guess what! while it isn't necessarily obvious, the
# functioning of the tempering matrix are mathematically
# reversible. this function impliments that...
#
# by using this, we can take the output of the MT PRNG, and turn
# it back into the actual values held within the MT[] array itself
# and therefore, we can "clone" the state of the PRNG from "n"
# generated random numbers...
#
# initially, figuring out the math to do this made my brain hurt.
# simplifying it caused even more pain.
# please don't ask me to explain it...
def untemper(y):
    y ^= y >> mt19937.l
    y ^= y << mt19937.t & mt19937.c
    for i in range(7):
        y ^= y << mt19937.s & mt19937.b
    for i in range(3):
        y ^= y >> mt19937.u & mt19937.d
    return y

## end of tom's work and start my junk##

# impossible.txt needs to contain the 624 previous seeds from the source code of the Snowball Game
# i copied the element then removed the first tab and "not random enough" string using find and replace in my editor
with open('impossible.txt') as orig_values:
  impossible = [line.rstrip('\n') for line in orig_values]

# as strings the values won't work with the mt19937 class so we convert each item into an int, probably a better way to do this from the outset but i'm a noob
count = 0
while count < len(impossible):
    impossible[count] = int(impossible[count])
    count += 1

# initializing the prng set
# the initial seed provided to mt19937 doesn't matter because we're going to replace anything present with the historical values we got from the game code
myprng = mt19937(0)

# set each MT as the impossible value
for i in range(mt19937.n):
    myprng.MT[i] = impossible[i]

# used to make sure that my set values matched what was in the document, leaving if it needs verification later
#for i in range(mt19937.n):
#    print(myprng.MT[i])

# in the original script the random output was being untempered to match the other function, we need to untemper the values we received from the snowball fight instead
for i in range(mt19937.n):
    myprng.MT[i] = untemper(myprng.MT[i])
    
# extract_number is needed to get the next seed. 
# since this is deterministic the output should never change
# for the snowball fight challenge, play this seed on easy mode to discover the board layout on impossible mode assuming this is actually the redacted seed for layout
for i in range(1):
    print(myprng.extract_number())