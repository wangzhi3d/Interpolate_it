#!/usr/bin/env python
#coding=cp936
#coding=utf-8
"""
@Amend Time: 2017.2.10

@Author: wangzhi
"""
from PySide import QtGui , QtCore

import maya.utils as utils

from PySide.QtGui import QPen , QColor , QBrush , QLinearGradient


class Base(object):
	_glow_pens = {}
	for index in range(1,11):
		_glow_pens[index] = [QPen(QColor(0 , 255 , 0 , 12 * index) , 1 , QtCore.Qt.SolidLine),
							QPen(QColor(0 , 255 , 0 , 5 * index) , 3 , QtCore.Qt.SolidLine),
							QPen(QColor(0 , 255 , 0 , 2 * index) , 5 , QtCore.Qt.SolidLine),
							QPen(QColor(0 , 255 , 0 , 25.5 * index) , 1 , QtCore.Qt.SolidLine)]
	
	_pens_text   = QPen(QColor(207 , 207 , 210) , 1 , QtCore.Qt.SolidLine)
	_pens_shadow = QPen(QColor(  9 ,  10 ,  12) , 1 , QtCore.Qt.SolidLine)
	_pens_border = QPen(QColor(  9 ,  10 ,  12) , 2 , QtCore.Qt.SolidLine)
	_pens_clear  = QPen(QColor( 0 , 0 ,  0 , 0) , 1 , QtCore.Qt.SolidLine)
	
	_pens_text_disabled   = QPen(QColor(102 , 107 , 110) , 1 , QtCore.Qt.SolidLine)
	_pens_shadow_disabled = QPen(QColor(  0 ,   0 ,   0) , 1 , QtCore.Qt.SolidLine)
	
	_brush_clear  = QBrush(QColor(0,0,0,0))
	_brush_border = QBrush(QColor(9,10,12))

	def __init__(self):
		font = QtGui.QFont()
		font.setPointSize(8)
		font.setFamily('Calibri')
		self.setFont(font)
		
		self._hover = False 
		self._glow_index = 0
		self._anim_timer = QtCore.QTimer()
		self._anim_timer.timeout.connect(self._animateGlow)
		
	def _animateGlow(self):
		if self._hover:
			if self._glow_index >= 10:
				self._glow_index = 10
				self._anim_timer.stop()
			else:
				self._glow_index += 1
				
		else:
			if self._glow_index <= 0:
				self._glow_index = 0
				self._anim_timer.stop()
			else:
				self._glow_index -= 1
	
		#.update 更新函数
		utils.executeDeferred(self.update) 
	
	def enterEvent(self , event):
		#进入事件
		#print 'enter'
		#super(self.__class__ , self).enterEvent(event)
		#Enabled: 激活
		if not self.isEnabled(): return
		
		self._hover = True
		self._startAnim()
	
	def leaveEvent(self , event):
		#离开事件
		#print 'leave'
		#super(self.__class__ , self).leaveEvent(event)
		
		if not self.isEnabled(): return
		
		self._hover = False
		self._startAnim()
		
		
	def _startAnim(self):
		if self._anim_timer.isActive():
			return
		
		self._anim_timer.start(15)