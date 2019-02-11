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
        #print(op[:-1])
        finalStr=""
        # Generate 10 junk entries
        #print("TOKEN ARRAY LENGHT: ", len(go))
        for gg in range(0,10):
            fakechar=self.ascii_letters[randint(0, 51)]
            go.append('$' + self.__varString__() + '="' + fakechar + '"')
        #print("TOKEN ARRAY LENGHT: ",len(go))
        AssignVariableString=""
        while True:
            if len(go) == 0:
                break
            AssignVariableString=AssignVariableString+go.pop(randint(0,len(go)-1))+";"
        print(AssignVariableString)
        print(op)






if __name__ == "__main__":
    pso=PSObfucate()
    pso.variableObs("HyperLinkHackz")