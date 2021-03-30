# summary: 调用 nodejs 处理 mathjax 公式
#网站：https://www.aimsciences.org/article/doi/10.3934/cpaa.2009.8.1725
import re
from subprocess import check_output
from parsel import Selector

def GetXml(mathjaxFormula):
    r""" 将 mathjax 公式转为 xml """
    bytesTxt = check_output(['node', 'test.js', mathjaxFormula], timeout=100)
    xmlText = bytesTxt.decode('utf8').strip()
    print('xmlText: %s' % xmlText)
    return xmlText

def Xml2PlainText(xmlText):
    r""" 将 xml 转换为普通文本 """
    sel = Selector(text=xmlText, type='xml')
    plainText = sel.xpath('string(.)').get().strip()
    plainText = re.sub(r'\s+', '', plainText)    # 去掉空白
    print('plainText: %s' % plainText)
    return plainText

def FnRepl(matched):
    r""" re.sub 的回调函数 """
    mathjaxFormula = matched.group(0)
    mathjaxFormula = mathjaxFormula[1:-1]  # 去掉前后的 $ 符号
    return Xml2PlainText(GetXml(mathjaxFormula))

def Convert(mathjaxText):
    plainText = re.sub('\$[\s\S]+?\$', FnRepl, mathjaxText)
    plainText = re.sub(r'\s+', ' ', plainText)    # 将多余空白替换成单个空格
    return plainText

if __name__ == '__main__':
    mathjaxText = 'Global well-posedness for the $L^2$-critical Hartree  equation on $\mathbb{R}^n$, $n\ge 3$'
    plainText = Convert(mathjaxText)
    print('mathjaxText: %s' % mathjaxText)
    print('plainText: %s' % plainText)