import sublime, sublime_plugin, re

class XorStringsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#self.view.insert(edit, 0, "Hello, World!")
		sels = self.view.sel()
		for idx, sel in enumerate(sels):
			selBegin = sel.begin()
			beginRow, beginCol = self.view.rowcol(selBegin)
			selEnd = sel.end()
			endRow, endCol = self.view.rowcol(selEnd)

			#Only allow two lines
			lineCount = endRow - beginRow + 1
			if lineCount != 2:
				self.showError("Wrong line count. ({!r})".format(lineCount))
				return
			#Validate each line and retrieve the text
			splitLines = self.view.split_by_newlines(sel)
			lineTexts = []
			for idx2, selLine in enumerate(splitLines):
				lineText = self.view.substr(selLine)
				if not self.isLineValid(lineText):
					self.showError("Line {0} is not a binary string".format(idx2))
					return
				else:
					lineTexts.append(lineText)
			result = self.xorStrings(lineTexts[0], lineTexts[1])
			self.view.insert(edit, selEnd, "\n" + result)
			print(result)
	def xorStrings(self, string1, string2):
		longer = max(len(string1), len(string2))
		print("longer is " + str(longer))
		result = ''
		for idx in range(longer):
			c1 = self.getCharOrZero(string1, idx)
			c2 = self.getCharOrZero(string2, idx)
			xored = self.xorChars(c1, c2)
			result += str(xored)
		return result

	def xorChars(self, char1, char2):
		c1parsed = int(char1)
		c2parsed = int(char2)
		result = (c1parsed + c2parsed) % 2
		return result

	def getCharOrZero(self, line, idx):
		if len(line) <= idx:
			return "0"
		else:
			return line[idx]
	#self.lineFormat = re.compile("^[01]*$")
	def isLineValid(self, lineText):
		#Would like to compile this but need to save in state
		matchObj = re.match("^[01]*$", lineText) 
		return matchObj is not None
	def showError(self, message):
		sublime.status_message(message)
		sublime.error_message(message)
#rowcol

# class ToggleCommand(sublime_plugin.TextCommand):
# 	def __init__(self, view):
# 		super().__init__(view)
# 		self.toggle = False		
# 		self.id = uuid.uuid4()
# 		print("Loaded, uuid is {!r}".format(self.id))
# 	def run(self, edit):
# 		self.toggle = not self.toggle
# 		message = "Toggled to {!r} in {!r}".format(self.toggle, self.id)
# 		sublime.status_message(message)
# 		print(message)

# 	def is_enabled(self):
# 		print("is_visible from {!r} - {!r}".format(self.id, self.toggle))
# 		return self.togglej