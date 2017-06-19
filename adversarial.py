#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  adversarial.py
#  
#  Copyright 2015 Robert Ringstad <robert@pcmarkone>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

#  Import statements
import numpy as np

prompt = '>'
print "This is an adversarial crime model with strategy inertia,"
print "adapted from DOI: 10.1103/PhysRevE.82.066114 by Short,"
print "Brantingham, and D'Orsogna, published in 2010."
print
print "Written by Robert Ringstad as part of a research project"
print "at NEIU, under the guidance of Dr. Joseph Hibdon, Jr."
print
print


#  Getting initial conditions from user
print "Initial Conditions:"
print "Number of Paladins"
paladins = raw_input(prompt)
print "Number of Informants"
informants = raw_input(prompt)
print "Number of Apathetics"
apathetics = raw_input(prompt)
print "Number of Villains"
villains = raw_input(prompt)
