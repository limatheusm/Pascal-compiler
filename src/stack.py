class Stack(object):		
    def __init__(self):		
        self.data = []		
 		
    def push(self, value):		
        self.data.append(value)		
  		
    def pop(self):		
        if not self.isempty():		
            return self.data.pop(-1)		
  		
    def isempty(self):		
        return len(self.data) == 0 