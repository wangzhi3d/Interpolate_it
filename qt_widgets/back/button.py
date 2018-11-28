import PySide.QtGui as QtGui
import PySide.QtCore as QtCore 

class DT_Button(QtGui.QPushButton):
	def __init__(self,*args , **kwargs):
		QtGui.QPushButton.__init__(self , *args , **kwargs)

	def paintEvent(self , event):
		painter = QtGui.QStylePainter(self)
		option = QtGui.QStyleOption()
		
		option.initFrom(self)
		option.direction
		
		x = option.rect.x()
		y = option.rect.y()
		height = option.rect.height() - 1
		width = option.rect.width() - 1 
		
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		painter.setPen(QtGui.QPen(QtGui.QColor(0,255,0),3,QtCore.Qt.SolidLine))
		painter.setBrush(QtGui.QBrush(QtGui.QColor(255,0,0)))
		painter.drawRoundedRect(QtCore.QRect(x+1 ,y+1 ,width-1 , height-1) ,5 ,5)
		
		text = self.text()
		painter.setPen(QtGui.QPen(QtGui.QColor(0,0,255)))
		painter.drawText(x,y,width , height , (QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter) , text)