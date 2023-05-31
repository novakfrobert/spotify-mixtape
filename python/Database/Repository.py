

class Repository:


    def __init__(self, session, model):
        self.Session = session
        self.Model = model

    def get(self):
        return self.Session.query(self.Model)

    def add(self, obj):
        self.Session.add(obj)

        
