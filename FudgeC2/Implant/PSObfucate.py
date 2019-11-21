from random import randint


class PSObfucate():
    ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    def __varString__(self):

        a = self.ascii_letters[randint(0, 51)]
        b = self.ascii_letters[randint(0, 51)]
        c = self.ascii_letters[randint(0, 51)]
        d = a + b + c
        return d


    def variableObs(self, variableStr):
        go=[]
        op=""
        for i in range(len(variableStr)):
            d=self.__varString__()
            go.append('$'+d+'="'+variableStr[i]+'"')
            op=op+"$"+d.strip()

        finalStr=""
        for gg in range(0,10):
            fakechar=self.ascii_letters[randint(0, 51)]
            go.append('$' + self.__varString__() + '="' + fakechar + '"')
        AssignVariableString=""
        while True:
            if len(go) == 0:
                break
            AssignVariableString=AssignVariableString+go.pop(randint(0,len(go)-1))+";"

        return AssignVariableString, op






if __name__ == "__main__":
    pso=PSObfucate()
    pso.variableObs("NetshPersistenceToken")