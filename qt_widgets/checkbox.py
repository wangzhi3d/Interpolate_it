from PySide import QtGui , QtCore

import maya.utils as utils

from PySide.QtGui import QPen , QColor , QBrush , QLinearGradient
import base


class DT_Checkbox(QtGui.QCheckBox ,base.Base):
	_glow_brushes = {}
	for index in range(1, 11):
		_glow_brushes[index] = [QBrush(QColor(0, 255, 0, 1    * index)),
								QBrush(QColor(0, 255, 0, 3    * index)),
								QBrush(QColor(0, 255, 0, 15   * index)),
								QBrush(QColor(0, 255, 0, 25.5 * index))]

	_disabled_glow_brushes = {}
	for index in range(1, 11):
		_disabled_glow_brushes[index] = [QBrush(QColor(125,125,125, 1    * index)),
										QBrush(QColor(125,125,125, 3    * index)),
										QBrush(QColor(125,125,125, 15   * index)),
										QBrush(QColor(125,125,125, 25.5 * index))]
	def __init__(self , *args , **kwargs):
		QtGui.QCheckBox.__init__(self , *args , **kwargs)
		
		font = QtGui.QFont()
		font.setPointSize(8)
		font.setFamily('Calibri')
		self.setFont(font)
		
		self._hover = False 
		self._glow_index = 0
		self._anim_timer = QtCore.QTimer()
		self._anim_timer.timeout.connect(self._animateGlow)
		
	def paintEvent(self , event):
		painter = QtGui.QStylePainter(self)
		option = QtGui.QStyleOption()
		option.initFrom(self)
		
		x = option.rect.x()
		y = option.rect.y()
		height = option.rect.height() -1 
		width = option.rect.width() -1 
		
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
		
		font = self.font()
		text = self.text()

		
		alignment = (QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
		
		painter.setPen(self._pens_border)
		painter.setBrush(self._brush_border)
		painter.drawRoundedRect(QtCore.QRect(x+2, y+2, 13, 13), 3, 3)
		
		if self.isEnabled():
			painter.setPen(self._pens_shadow)
			painter.drawText(21, y+2, width, height, alignment, text)
			
			painter.setPen(self._pens_text)
			painter.drawText(20, y+1, width, height, alignment, text)
		
		else:
			painter.setPen(self._pens_shadow_disabled)
			painter.drawText(21, y+2, width, height, alignment, text)
			
			painter.setPen(self._pens_text_disabled)
			painter.drawText(20, y+1, width, height, alignment, text)
			
		painter.setPen(self._pens_clear)
		
		if self.isEnabled():
			glow_brushes = self._glow_brushes
		else:
			glow_brushes = self._disabled_glow_brushes
			
		if self.checkState():
			for index ,pos , size , corner in zip(range(4) , (2,3,4,5) , (13,11,9,7) , (4,3,3,2)):
				painter.setBrush(glow_brushes[10][index])
				painter.drawRoundedRect(QtCore.QRect(x+pos, y+pos, size, size), corner, corner)
				
		glow_index   = self._glow_index
		if glow_index > 0:
			for index, pos, size, corner in zip(range(4), (3,4,5,6), (11,9,7,5), (3,3,2,2)):
				painter.setBrush(glow_brushes[glow_index][index])
				painter.drawRoundedRect(QtCore.QRect(x+pos, y+pos, size, size), corner, corner)

	def enterEvent(self , event):
		
		if not self.isEnabled(): return
		
		self._hover = True
		self._startAnim()
	
	def leaveEvent(self , event):
		
		if not self.isEnabled(): return
		
		self._hover = False
		self._startAnim()