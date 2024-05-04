class CustomString(str):
    def __init__(self, value):
        self.value=value
        super().__init__()
    def get(self):
        return self.value