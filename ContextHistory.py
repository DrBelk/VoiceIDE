import copy

class ContextHistory():
    def __init__(self):
        self.history = list("")
        self.currentPosition = -1

    def addContext(self, context):
        self.currentPosition += 1
        self.history = self.history[0:self.currentPosition]
        self.history.append(copy.deepcopy(context))
        print("[ContextHistory] addContext, currentPosition is", self.currentPosition)

    def undo(self):
        if self.currentPosition - 1 >= 0:
            self.currentPosition -= 1
        return self.getCurrContext()

    def redo(self):
        if self.currentPosition + 1 < len(self.history):
            self.currentPosition += 1
        return self.getCurrContext()

    def getCurrContext(self):
        print ('[ContextHistory] return current context number', self.currentPosition)
        return copy.deepcopy(self.history[self.currentPosition])
