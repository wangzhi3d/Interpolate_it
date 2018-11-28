from PySide import QtGui, QtCore

import pymel.core as pm 
from utils.generic import undo_pm

import maya.OpenMayaUI as OpenMayaUI
from shiboken import wrapInstance
import functools , os


from qt_widgets.button import DT_Button , DT_ButtonThin , DT_CloseButton
from qt_widgets.checkbox import DT_Checkbox
from qt_widgets.label import DT_Label
from qt_widgets.slider import DT_Slider
from qt_widgets.line_edit import DT_lineEdit
START = 'start'
END   = 'end'
CACHE = 'cache'
NODE  = 'node'

style_sheet_file = file(os.path.join(os.path.dirname(__file__) , 'stylesheets' , 'scheme.qss' ))
#style_sheet_file = file('F:\python\stylesheets\scheme.qss')
style_sheet_read = style_sheet_file.read()
style_sheet_file.close()

def getMayaWindow():
	
	ptr = OpenMayaUI.MQtUtil.mainWindow()
	if ptr:
		return wrapInstance(long(ptr) , QtGui.QWidget)



class InterpolateIt(QtGui.QDialog):
	def __init__(self , parent = getMayaWindow()):
		self.title = 'InterpolateIt'
		
		QtGui.QDialog.__init__(self , parent)
		self.setWindowFlags(QtCore.Qt.Window)
		self.setObjectName(self.title)
		self.setWindowTitle('Interpolate It')
		self.setFixedWidth(314)
		self.setStyleSheet('color: rgb(202, 207, 210);\nbackground-color: rgb(12, 13, 15);')
		

		
		self.setLayout(QtGui.QVBoxLayout())
		self.layout().setContentsMargins(0,0,0,0)
		self.layout().setSpacing(0)
		
		scroll_area = QtGui.QScrollArea()
		scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
		scroll_area.setWidgetResizable(True)
		scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.layout().addWidget(scroll_area)
		
		main_widget = QtGui.QWidget()
		main_widget.setObjectName('InterpolateIt')
		main_widget.setStyleSheet('color: rgb(202, 207, 210);\nbackground-color: rgb(12, 13, 15);')
		main_layout = QtGui.QVBoxLayout()
		main_layout.setContentsMargins(5,5,5,5)
		main_layout.setAlignment(QtCore.Qt.AlignTop)
		main_widget.setLayout(main_layout)
		scroll_area.setWidget(main_widget)
		
		self.interp_layout = QtGui.QVBoxLayout()
		self.interp_layout.setContentsMargins(0,0,0,0)
		self.interp_layout.setSpacing(0)
		self.interp_layout.setAlignment(QtCore.Qt.AlignTop)
		main_layout.addLayout(self.interp_layout)
		
		self.button_layout = QtGui.QHBoxLayout()
		self.button_layout.setContentsMargins(0,0,0,0)
		self.button_layout.setAlignment(QtCore.Qt.AlignRight)
		main_layout.addLayout(self.button_layout)
		
		add_button = DT_ButtonThin('New..')
		add_button.setStyleSheet(style_sheet_read)
		self.button_layout.addWidget(add_button)
		
		new_widget = InterpolateWidget()
		new_widget.hideCloseButton()
		self.interp_layout.addWidget(new_widget)

		
		self._interp_widget = []
		self._interp_widget.append(new_widget)
		
		self._dock_widget = self._dock_name = None
		
		add_button.clicked.connect(self.add)
		
		
	def add(self):
		new_widget = InterpolateWidget()
		self.interp_layout.addWidget(new_widget)
		self._interp_widget.append(new_widget)
		new_widget.close_bttn.clicked.connect(functools.partial(self.remove , new_widget))
		new_widget._animateExpand(True)
		
	def remove(self , interp_widget):
		interp_widget.close_bttn.clicked.connect(functools.partial(self._delete , interp_widget))
		self._interp_widget.remove(interp_widget)
		interp_widget._animateExpand(False)
		
		
		
	def _delete(self, interp_widget):
		self.interp_layout.removeWidget(interp_widget)
		interp_widget._animation = None
		interp_widget.deleteLater()
		
		
	def connectDockWidget(self , dock_name ,dock_widget):
		self._dock_widget = dock_widget
		self._dock_name = dock_name
		
	
	def close(self):
		if self._dock_widget:
			pm.deleteUI(self._dock_name)
		else:
			QtGui.QDialog.close(self)
		self._dock_widget = self._dock_name = None
		
	

class InterpolateWidget(QtGui.QFrame):
	def __init__(self, *args , **kwargs):
		QtGui.QFrame.__init__(self, *args , **kwargs)
		
		
		self.setStyleSheet(style_sheet_read)
		
		
		self.setLayout(QtGui.QVBoxLayout())
		self.layout().setContentsMargins(3,1,3,3)
		self.layout().setSpacing(0)
		self.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
		self.setFixedHeight(150)
		
		main_widget = QtGui.QWidget()
		main_widget.setLayout(QtGui.QVBoxLayout())
		main_widget.layout().setContentsMargins(2,2,2,2)
		main_widget.layout().setSpacing(5)
		main_widget.setFixedHeight(140)
		main_widget.setFixedWidth(290)

		
		graphics_scene = QtGui.QGraphicsScene()
		graphics_view = QtGui.QGraphicsView()
		graphics_view.setScene(graphics_scene)
		graphics_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		graphics_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		graphics_view.setFocusPolicy(QtCore.Qt.NoFocus)
		graphics_view.setStyleSheet("QGraphicsView {border-style: none;}")
		graphics_view.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		self.layout().addWidget(graphics_view)
		self.main_widget_proxy = graphics_scene.addWidget(main_widget)
		main_widget.setParent(graphics_view)
		
		
		title_layout = QtGui.QHBoxLayout()
		select_layout = QtGui.QHBoxLayout()
		button_layout = QtGui.QHBoxLayout()
		slider_layout = QtGui.QHBoxLayout()
		check_layout = QtGui.QHBoxLayout()
		main_widget.layout().addLayout(title_layout)
		main_widget.layout().addLayout(select_layout)
		main_widget.layout().addLayout(button_layout)
		main_widget.layout().addLayout(slider_layout)
		main_widget.layout().addLayout(check_layout)
		
		title_line = DT_lineEdit('Untitled')
		title_layout.addWidget(title_line)
		
		self.close_bttn = DT_CloseButton('X')
		self.close_bttn.setObjectName('roundedButton')
		title_layout.addWidget(self.close_bttn)
		
		store_items = DT_Button('Stoer Items')
		clear_items = DT_Button('Clear Items')
		
		select_layout.addSpacerItem(QtGui.QSpacerItem(5,5 , QtGui.QSizePolicy.Expanding))
		select_layout.addWidget(store_items)
		select_layout.addWidget(clear_items)
		select_layout.addSpacerItem(QtGui.QSpacerItem(5,5 , QtGui.QSizePolicy.Expanding))
		
		self.store_start_bttn = DT_ButtonThin('Stoer Start')
		self.reset_item_bttn = DT_ButtonThin('Reset')
		self.store_end_bttn = DT_ButtonThin('Store End')
		
		button_layout.addWidget(self.store_start_bttn)
		button_layout.addWidget(self.reset_item_bttn)
		button_layout.addWidget(self.store_end_bttn)
		
		self.start_lb = DT_Label('Start')
		self.slider = DT_Slider()
		self.slider.setRange(0,49)
		self.slider.setOrientation(QtCore.Qt.Horizontal)
		self.end_lb = DT_Label('End')
		
		slider_layout.addWidget(self.start_lb)
		slider_layout.addWidget(self.slider)
		slider_layout.addWidget(self.end_lb)
		
		self.transforms_chbx = DT_Checkbox('Transform')
		self.attributes_chbx = DT_Checkbox('UD Attributes')
		self.transforms_chbx.setCheckState(QtCore.Qt.Checked)
		check_layout.addWidget(self.transforms_chbx)
		check_layout.addWidget(self.attributes_chbx)
		
		self.items = {}
		self.slider_down = False
		
		#self.close_bttn.clicked.connect(self.closeWidget)
		
		store_items.clicked.connect(self.storeItems)
		clear_items.clicked.connect(self.clearItems)
		
		self.store_start_bttn.clicked.connect(self.storeStart)
		self.reset_item_bttn.clicked.connect(self.resetAttributes)
		self.store_end_bttn.clicked.connect(self.storeEnd)
		
		self.slider.valueChanged.connect(self.setLinearInterpolation)
		self.slider.sliderReleased.connect(self._endSliderUndo)
		self.slider.valueChanged.connect(self.changeLabelGlow)
		
		self.enableButtons(False)
		
	def changeLabelGlow(self , value):
		glow_value = int(float(value)/self.slider.maximum() * 100)
		self.start_lb.setGlowValue(100 - glow_value)
		self.end_lb.setGlowValue(glow_value)
		
	def _animateExpand(self, value):
		opacity_anim = QtCore.QPropertyAnimation(self.main_widget_proxy, "opacity")
		
		opacity_anim.setStartValue(not(value))
		opacity_anim.setEndValue(value)
		opacity_anim.setDuration(200)
		
		opacity_anim_curve = QtCore.QEasingCurve()
		if value:
			opacity_anim_curve.setType(QtCore.QEasingCurve.InQuad)
		else:
			opacity_anim_curve.setType(QtCore.QEasingCurve.OutQuad)
		opacity_anim.setEasingCurve(opacity_anim_curve)
			
		size_anim = QtCore.QPropertyAnimation(self , 'geometry')
		
		geometry = self.geometry()
		width = geometry.width()
		x,y,_,_ = geometry.getCoords()
		
		size_start = QtCore.QRect(x , y , width , int(not(value)) * 150)
		size_end   = QtCore.QRect(x , y , width , value*150)
		
		size_anim.setStartValue(size_start)
		size_anim.setEndValue(size_end)
		size_anim.setDuration(300)
		
		size_anim_curve = QtCore.QEasingCurve()
		if value:
			size_anim_curve.setType(QtCore.QEasingCurve.InQuad)
		else:
			size_anim_curve.setType(QtCore.QEasingCurve.OutQuad)
		size_anim.setEasingCurve(size_anim_curve)
		
		self._animation = QtCore.QSequentialAnimationGroup()
		if value:
			self.main_widget_proxy.setOpacity(1)
			self._animation.addAnimation(size_anim)
			self._animation.addAnimation(opacity_anim)
		else:
			self.main_widget_proxy.setOpacity(0)
			self._animation.addAnimation(opacity_anim)
			self._animation.addAnimation(size_anim)
		
		size_anim.valueChanged.connect(self._forceResize)
		self._animation.finished.connect(self._animation.clear)
		
		if not value:
			size_anim.finished.connect(self.deleteWidget)
		size_anim.start(QtCore.QAbstractAnimation.DeleteWhenStopped)
		
	def _forceResize(self, new_height):
		self.setFixedHeight(new_height.height())
		
	def _startSliderUndo(self):
		pm.undoInfo(openChunk=True)
	
	def _endSliderUndo(self):
		pm.undoInfo(closeChunk = True)
		self.slider_down = False
	
	def storeItems(self):
		selection = pm.ls(sl = True , fl = True)
		if not selection:
			return 
		
		self.items = {}
		for node in selection:
			self.items[node.name()] = {NODE:node , START:{} , END:{} , CACHE:{}}
		
		self.enableButtons(True)
	
	def clearItems(self):
		self.items = {}
		self.enableButtons(False)
		
	def enableButtons(self , value):
		self.store_start_bttn.setEnabled(value)
		self.reset_item_bttn.setEnabled(value)
		self.store_end_bttn.setEnabled(value)
		self.transforms_chbx.setEnabled(value)
		self.attributes_chbx.setEnabled(value)
		self.slider.setEnabled(value)
		self.start_lb.setEnabled(value)
		self.end_lb.setEnabled(value)
		
	def hideCloseButton(self, value = True):
		self.close_bttn.setVisible(not(value))
	
	def storeStart(self):
		if not self.items: return 
		self._store(START , 0)
		self._cache()
		
	def storeEnd(self):
		if not self.items: return
		self._store(END , 50)
		self._cache()
		
	def _store(self, key , value):
		for item_dict in self.items.values():
			node = item_dict[NODE]
			attrs = self.getAttributes(node)
			data = item_dict[key]
			for attr in attrs:
				data[attr] = node.attr(attr).get()
			
		self.slider.blockSignals(True)
		self.slider.setValue(value)
		self.slider.blockSignals(False)
	
	def _cache(self):
		for item_dict in self.items.values():
			node = item_dict[NODE]
			
			start = item_dict[START]
			end = item_dict[END]
			if not start or not end:
				item_dict[CACHE] = None
				continue
			
			attrs = list(set(start.keys()) and set(end.keys()))
			
			cache = item_dict[CACHE] = {}
			for attr in attrs:
				start_attr = start[attr]
				end_attr   = end[attr]
				if start_attr == end_attr:
					cache[attr] = None
				else:
					cache_values = cache[attr] = []
					interval = float(end_attr - start_attr)/49.0
					for index in range(50):
						cache_values.append(interval*index + start_attr)
			
	
	def getAttributes(self, node):
		attrs = []
		if self.transforms_chbx.isChecked():
			for transform in 'trs':
				for axis in 'xyz':
					channel = '%s%s'%(transform,axis)
					if node.attr(channel).isLocked(): continue
					attrs.append(channel)
		
		if self.attributes_chbx.isChecked():
			for attr in node.liatAttr(ud = True):
				if attr.isLocked(): continue
				if attr.type() not in ('double' , 'int'): continue
				
				attrs.append(attr.attrName())
			
		return attrs
	
	@undo_pm
	def resetAttributes(self , *args):
		if not self.items:
			return
		for item_dict in self.items.values():
			node = item_dict[NODE]
			attrs = self.getAttributes(node)
		
			for attr in attrs:
				default_value = pm.attributeQuery(attr, node=node, ld=True)[0]
				node.attr(attr).set(default_value)
	
	def setLinearInterpolation(self , value):
		if not self.items:
			return
		
		if not self.slider_down:
			self._startSliderUndo()
			self.slider_down = True
			
		for item_dict in self.items.values():
			node = item_dict[NODE]
			start = item_dict[START]
			
			if not start or not item_dict[END]: continue
			
			cache = item_dict[CACHE]
			
			for attr in cache.keys():
				if cache[attr] == None: continue
				node.attr(attr).set(cache[attr][value])
				
	#def closeWidget(self):
		#self.close()
		
	def deleteWidget(self):
		self.deleteLater()
		
dialog = None 

def create(docked = True):
	global dialog
	if dialog is None:
		dialog = InterpolateIt()
		
	if docked is True:
	
		size = dialog.size()

		name = 'MayaWindow|InterpolateIt'
		dock = pm.dockControl(
				allowedArea =['right', 'left'],
				area        = 'right',
				floating    = False,
				content     = name,
				width       = size.width(),
				height      = size.height(),
				label       = 'Interpolate It')
		
		widget      = OpenMayaUI.MQtUtil.findControl(dock)
		dock_widget = wrapInstance(long(widget), QtCore.QObject)
		
	dialog.show()

def delete():
    global dialog
    if dialog:
        dialog.close()
        dialog = None

