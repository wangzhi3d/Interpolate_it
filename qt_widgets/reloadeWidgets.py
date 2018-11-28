import button , checkbox , label , slider ,line_edit


def reloadIt():
	
	reload(button)
	reload(checkbox)
	reload(label)
	reload(slider)
	reload(line_edit)
	
	print '-------------> WIDGETS RELOAD : OK'