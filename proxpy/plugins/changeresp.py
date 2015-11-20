#coding:utf-8

import xml.dom.minidom as Dom


class AuthorAlias(object):

    def __init__(self):
        self.shouldTrans = False
        self.map = {
            'A1361': u'吴孟春'
        }
        print(self.map)

    def trans(self, rep):
        if self.shouldTrans:
            v = rep.getHeader("Content-Type")
            if len(v) > 0 and "text/xml" in v[0]:
                rep.body = self.transAuthor(rep.body)
                rep.setHeader('Content-Length', len(rep.body))
        return rep

    def transAuthor(self, xmlStr):
        dom = Dom.parseString(xmlStr)
        for element in dom.getElementsByTagName('author'):
            if element.firstChild.nodeType == element.TEXT_NODE:
                element.firstChild.nodeValue = self.map.get(
                    element.firstChild.nodeValue, element.firstChild.nodeValue)
        return dom.toxml('utf-8')

    def record(self, req):
        self.shouldTrans = req.getMethod() == 1 and req.getParams().get('xml')
        self.shouldTrans = True     # test only


transer = AuthorAlias()


def proxy_mangle_request(req):
    transer.record(req)
    return req


def proxy_mangle_response(rep):
    transer.trans(rep)
    return rep
