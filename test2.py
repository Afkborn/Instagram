
class test:
    __isLogin = False
    def __init__(self):
        self.__isLogin = True
        self.__changeLogin(False)
    def getIsLogin(self):
        return self.__isLogin
    def __changeLogin(self,newLoginState : bool):
        self.__isLogin == newLoginState


testObje = test()