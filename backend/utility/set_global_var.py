#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import backend.utility.globalvar as gl

gl._init()

gl.set_value('diameter_axis', [1, 2, 3, 5, 10, 15, 20])
gl.set_value('ssd_al_axis', [1.5, 3, 5, 7, 10, 20, 30, 50, 100])
gl.set_value('ssd_cu_axis', [10, 20, 30, 50, 100])
gl.set_value('hvl_al_axis', [0.04, 0.05, 0.06, 0.08, 0.1, 0.12, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1, 1.2, 1.5, 2, 3, 4, 5, 6, 8])
gl.set_value('hvl_cu_axis', [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1, 1.5, 2, 3, 4, 5])
