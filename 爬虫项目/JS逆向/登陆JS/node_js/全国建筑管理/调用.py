import re
from subprocess import check_output
from parsel import Selector
#网站：http://jzsc.mohurd.gov.cn/data/company
def GetXml():
    r""" 将 mathjax 公式转为 xml """
    bytesTxt = check_output(['node', 'test.js'], timeout=100)
    xmlText = bytesTxt.decode('utf8').strip()
    print('xmlText: %s' % xmlText)
    return xmlText

GetXml()