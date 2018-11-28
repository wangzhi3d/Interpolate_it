from PySide import QtGui , QtCore

import maya.utils as utils

from PySide.QtGui import QPen , QColor , QBrush , QLinearGradient

import base

class DT_Slider(QtGui.QSlider , base.Base):
	_glow_brushes = {}
	for index in range(1 , 11):
		_glow_brushes[index] = [QBrush(QColor(0 , 255 , 0 , 1 * index)),
								QBrush(QColor(0 , 255 , 0 , 3 * index)),
								QBrush(QColor(0 , 255 , 0 ,8 * index)),
								QBrush(QColor(0 , 255 , 0 ,25.5 * index)),
								QBrush(QColor(0 , 255 , 0 , 15 * index)),]
	
	_pens_dark = QPen(QColor(0 , 5 , 9) , 1 , QtCore.Qt.SolidLine)
	_pens_light = QPen(QColor(16 , 17 , 19) , 1 , QtCore.Qt.SolidLine)
	
	_gradient_inner = QLinearGradient(0 , 9 , 0 , 15)
	_gradient_inner.setColorAt(0 , QColor(69 , 73 , 76))
	_gradient_inner.setColorAt(1 , QColor(17 , 18 , 20))
	
	_gradient_outer = QLinearGradient(0 , 9 , 0 , 15)
	_gradient_outer.setColorAt(0 , QColor(53 , 57 , 60))
	_gradient_outer.setColorAt(1 , QColor(33 , 34 , 36))
	
	def __init__(self , *args , **kwargs):
		QtGui.QSlider.__init__(self , *args , **kwargs)

		self._hover = False 
		self._glow_index = 0
		self._anim_timer = QtCore.QTimer()
		self._anim_timer.timeout.connect(self._animateGlow)
		
		self.setOrientation(QtCore.Qt.Horizontal)
		self.setFixedHeight(22)
		self.setMinimumWidth(50)
		
		self._track = False
		self._tracking_point = {}
		
		self._anim_follow_timer = QtCore.QTimer()
		self._anim_follow_timer.timeout.connect(self._removeTrackingPoints)
		
		self.valueChanged.connect(self._trackChanges)
		self._updateTracking()
		
	def setRange(self , *args , **kwargs):
		QtGui.QSlider.setRange(self , *args , **kwargs)
		self._updateTracking()
		
	def setMinimum(self , *args , **kwargs):
		QtGui.QSlider.setMinimum(self , *args , **kwargs)
		self._updateTracking()

	def setMaximum(self , *args , **kwargs):
		QtGui.QSlider.setMaximum(self , *args , **kwargs)
		self._updateTracking()
		
	def _updateTracking(self):
		self._tracking_points = [0] *(abs(self.maximum() - self.minimum()) + 1)

	def setValue(self , *args , **kwargs):
		QtGui.QSlider.setValue(self , *args , **kwargs)
		for index in range(len(self._tracking_points)):
			self._tracking_points[index] = 0
	
	def mouseMoveEvent(self , event):
		QtGui.QSlider.mouseMoveEvent(self , event)
		
		if self._anim_follow_timer.isActive():
			return
		
		self._anim_follow_timer.start(30)
	
	def _trackChanges(self , value):
		value = value - self.minimum()
		self._tracking_points[value] = 10
		
	def _removeTrackingPoints(self):
		self._track = False
		for index , value in enumerate(self._tracking_points):
			if value > 0:
				self._tracking_points[index] -= 1
				self._track = True
			
		if self._track is False:
			self._anim_follow_timer.stop()
				
		utils.executeDeferred(self.update)
	
	def paintEvent(self , event):
		painter = QtGui.QStylePainter(self)
		option = QtGui.QStyleOption()
		option.initFrom(self)
		
		x = option.rect.x()
		y = option.rect.y()
		width = option.rect.width() - 1
		height = option.rect.height() - 1
		
		orientation = self.orientation()
		
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		
		painter.setPen(self._pens_shadow)
		painter.setBrush(self._brush_border)
		painter.drawRoundedRect(QtCore.QRect(x+1 , y+1 , width-1 , height-1) , 10 , 10)
		
		
		mid_height = (height / 2) + 1
		painter.setPen(self._pens_dark)
		painter.drawLine(10 , mid_height , width - 8 , mid_height)
		painter.setRenderHint(QtGui.QPainter.Antialiasing , False)
		painter.setPen(self._pens_light)
		painter.drawLine(10 , mid_height , width - 10 , mid_height)
		painter.setRenderHint(QtGui.QPainter.Antialiasing , True)
		
		minimum = self.minimum()
		maximum = self.maximum()
		value_range = maximum - minimum
		value = self.value() - minimum
		
		increment = ((width - 20) / float(value_range))
		center = 10 + (increment * value)
		center_point = QtCore.QPoint(x + center , y + mid_height)
		
		painter.setPen(self._pens_clear)
		
		glow_index = self._glow_index
		glow_brushes = self._glow_brushes
		
		if self._track is True:
			for index , track_value in enumerate(self._tracking_points):
				if track_value == 0: continue
				track_center = 10 + (increment * index)
				painter.setBrush(glow_brushes[track_value][4])
				painter.drawEllipse(QtCore.QPoint(track_center , mid_height) , 7 , 7)
		
		if glow_index > 0:
			for index , size in zip(range(4) , range(10,6,-1)):
				painter.setBrush(glow_brushes[glow_index][index])
				painter.drawEllipse(center_point , size , size)
		
		painter.setBrush(QtGui.QBrush(self._gradient_outer))
		painter.drawEllipse(center_point , 6 , 6)
		
		painter.setBrush(QtGui.QBrush(self._gradient_inner))
		painter.drawEllipse(center_point , 5 , 5)			
		

	def enterEvent(self , event):
		
		if not self.isEnabled(): return
		
		self._hover = True
		self._startAnim()
	
	def leaveEvent(self , event):
		
		if not self.isEnabled(): return
		
		self._hover = False
		self._startAnim()