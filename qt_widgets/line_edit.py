from PySide import QtGui , QtCore

import maya.utils as utils

from PySide.QtGui import QPen , QColor , QBrush , QLinearGradient

import base


class DT_lineEdit(QtGui.QLineEdit):
	
	_glow_pens = base.Base._glow_pens
	
	_pens_text = base.Base._pens_text
	_pens_shadow = base.Base._pens_shadow
	_pens_border = base.Base._pens_border
	_pens_clear = base.Base._pens_clear
	
	_brush_clear = base.Base._brush_clear
	
	_pens_placeholder = QPen(QColor(202 , 207 , 210 , 127) , 1 , QtCore.Qt.SolidLine)
	
	def __init__(self , *args , **kwargs):
		QtGui.QLineEdit.__init__(self , *args , **kwargs)
		
		
		font = QtGui.QFont()
		font.setPixelSize(16)
		self.setFont(font)
		self.font_metrics = QtGui.QFontMetrics(font)
		self.setFixedHeight(self.font_metrics.height() + 7)
		
		self._placeholder_message = ''
		
		self._text_glow = {}
		self._previous_text = ''
		
		text = self.text()
		if text : self.setText(text)
		
		self._anim_timer = QtCore.QTimer()
		self._anim_timer.timeout.connect(self._animateText)
		
	def setText(self , *args):
		
		QtGui.QLineEdit.setText(self , *args)
		self._text_glow = {}
		text = self.text()
		for index in range(len(text)):
			self._text_glow[index] = 0
		
	def setPlaceholderMessage(self , message):
		self._placeholder_message = str(message)
	
	def keyPressEvent(self , *args):
		QtGui.QLineEdit.keyPressEvent(self , *args)
		text = self.text()
		
		if text == self._previous_text : return
		
		len_text = len(text)
		if len_text > len(self._previous_text):
			self._anim_timer.start(30)
			self._text_glow[len_text - 1] = 0
			self._text_glow[self.cursorPosition() -1] = 10
			
		elif len(self._text_glow.keys()) == 0:
			self._anim_timer.stop()
		
		self._previous_text = text
	
	def _animateText(self):
		stop_animating = True
		for key , value in self._text_glow.items():
			if value > 0:
				stop_animating = False
				self._text_glow[key] = value - 1
		
		if stop_animating:
			self._anim_timer.stop()
		
		utils.executeDeferred(self.update)
		

		
	def paintEvent(self , event):
		painter = QtGui.QStylePainter(self)
		option  = QtGui.QStyleOptionFrame()
		self.initStyleOption(option)
		
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
		
		contents = self.style().subElementRect(QtGui.QStyle.SE_LineEditContents , option , self )
		contents.setLeft(contents.left() + 2)
		contents.setRight(contents.right() - 2)
		alignment = (QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
	
		text = self.text()
		font = self.font()
		font_metrics = self.font_metrics
		
		if not text:
			painter.setPen(self._pens_placeholder)
			painter.drawText(contents , alignment , self._placeholder_message)
			
		glow_pens = self._glow_pens
		
		left_edge = contents.left()
		for index , letter in enumerate(text):
			text_width = font_metrics.width(text[0:index])
			contents.setLeft(left_edge + text_width)
		
			x , y , width , height = contents.getRect()
			
			painter.setPen(self._pens_shadow)
			painter.drawText(x+1 , y+1 , width , height , alignment , letter )
			painter.setPen(self._pens_text)
			painter.drawText(contents , alignment , letter )	
			
			glow_index = self._text_glow[index]
			if glow_index > 0:
				text_path = QtGui.QPainterPath()
				text_path.addText(contents.left() , font.pixelSize() + 4 , font , letter)
				
				for index in range(3):
					painter.setPen(glow_pens[glow_index][index])
					painter.drawPath(text_path )
		
				painter.setPen(glow_pens[glow_index][3])
				painter.drawText(contents , alignment , letter )
		
		if not self.hasFocus(): return
		
		contents.setLeft(left_edge)
		x, y, width, height = contents.getRect()
		
		cursor_pos = self.cursorPosition()
		text_width = font_metrics.width(text[0:cursor_pos])
		pos = x + text_width
		top = y + 1
		bttm = y + height - 1
		painter.drawLine(pos, top,pos, bttm)
		