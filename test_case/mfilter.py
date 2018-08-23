# coding=utf-8
import json
import re

class Mfilter:

    def __init__(self,assertEqual):
        self.assertEqual = assertEqual

    def run(self,item,array):
        for a in array:
            param = a.split('|')
            name = param[0]

            if "require" in param:

                if name not in item:
                    self.__validRequire(name)


            if name not in item:
                continue

            if "int" in param:

                self.__validInt(name, item[name])

            if "float" in param:
                self.__validFloat(name, item[name])

            if  "varchar" in param:
                self.__validVarchar(name, item[name])

            if  "array" in param:
                self.__validArray(name, item[name])

            if "Bool" in param:
                self.__validBool(name, item[name])

            if "object" in param:
                self.__validObject(name, item[name])

            if "inArray" in json.dumps(param):
                array = re.compile("inArray:(.*?)]").findall(''.join(param))[0]+"]"
                self.__validIn(name, item[name],json.loads(array))


    def __validObject(self,name,value):
        if type(value)!=type({}):
                self.assertEqual.assertEqual(name, -1, name + ' require object')


    def __validRequire(self,name):
        self.assertEqual.assertEqual(name, -1, name + ' require')


    def __validBool(self, name, value):
        if type(value) != type(True) or type(value) !=type(False):
            self.assertEqual.assertEqual(name, -1, name + ' require Bool')


    def __validInt(self,name,value):
        if type(value) != type(1):
            self.assertEqual.assertEqual(name, -1, name+' require int')

    def __validFloat(self,name,value):
        if type(value) != type(1.23) and type(value)!=type(2):
            self.assertEqual.assertEqual(name, -1, name + ' require float')

    def __validArray(self, name, value):
        if type(value) != type([]):
            self.assertEqual.assertEqual(name, -1, name + ' require array')

    def __validVarchar(self,name,value):
        if type(value)==type(u"unicode"):
            value = value.encode('utf-8')

        if type(value) != type("1"):
            self.assertEqual.assertEqual(name, -1, name+' require string')

    def __valid(self,value):
        if type(value)==type(u"unicode"):
            value = value.encode('utf-8')
        return value

    def __validIn(self,name,value,in_array):

        if value not in in_array:
            self.assertEqual.assertEqual(name, -1, name+' not in '+json.dumps(in_array))
