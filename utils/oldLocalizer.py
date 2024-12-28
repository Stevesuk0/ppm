"""

    This is a localizer for ppm;
    I'll add crowdin support in the future btw

"""
import pConfig
import stringUtils
import re

def setLanguage(lang):
    if pconfig.language!=0:
        pconfig.language = lang
        return 1
    else:
        return 0

def readLang(language,isList):
    with open(f"localizing/{language}.lang",'r') as f:
        if isList:
            return [x.strip() for x in f.readlines()]
        else:
            return f.readlines()

def translate(a):
    for i in readLang(pconfig.language,True):
        if re.search(a,i):
            return i.split('$')[1]

def testing():
    exampleString = readLang(pconfig.language,True)[0]
    stringUtils.printMultiLines(exampleString)

if __name__=="__main__":
    pass