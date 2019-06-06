class TestClass():

    data = ''

    def __init__(self):
        self.data = 'aaa'

    def test_func(self):
        resp = {"response": self.data}
        return resp