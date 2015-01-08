#!/usr/bin/env python
#-*- coding:utf-8 -*-


"""
    pyBibel - a bible webviewer
    (gpl v3) by Tobias Sauer
    http://tobi.leichtdio.de
    part of
        - Dreifach Glauben : http://dreifachglauben.de
        - Offene Bibel : http://offene-bibel.de/
        - Leichtdio.de : http://leichtdio.de
    tobias [at] leichtdio . de   
    
    Import WikiMedia Data -> convert to BibleJSON


    ToDo:
        - später soll er sich automatisch ein Update ziehen.
          das Feature fehlt jedoch noch, damit nicht jmd den Wikitext manipulieren
          kann um einen Schadcode zu verstecken. Schauen wir mal wie das klappt ;)


"""

import urllib2
import re
import json
import os.path

_long_book = { "mk" : "Markus" }

class Importor:
    def __init__(self):
        self.baseurl = 'http://www.offene-bibel.de/wiki/api.php?format=txt&action=query&titles=%s_%s&prop=revisions&rvprop=content'
    
    def import_chapter (self, book, chapter):
        file_url = os.path.join("JSON", book, chapter+".json")
        response = urllib2.urlopen(self.baseurl %(_long_book[book], chapter))
        html = response.read()
        html = html.decode('utf-8')
        import_dic = {
            u"book" : book,
            u"copyright" : u"http://creativecommons.org/licenses/by-sa/3.0/",
            u"generator" : u"pyBible - WikiMedia Auto Importer",
            u"sections" : {},
            u"text" : {}
            }
        html = unicode(html)
        html = html.replace(u"{{L", u"\n{{L")
        html = html.replace(u"<br/>", u"")
        html = html.replace(u"}}" , u"}} ")
        #print html[:1000]
        for x in re.findall(u"{{L\|[0-9]*}}.*", html):
            x = x[4:]
            #print x
            #### seeehr übler quickhack um {{sekundär}} und {{sekundär ende}} zu filtern
            x = x.replace(u"r}}", u"")
            x = x.replace(u"e}}", u"")
            
            versnr, x = x.split(u"}} ")
            #versnr = x.split(" ")[0][:-2]
            import_dic[u"text"][versnr] = x.lstrip()

        json.dump(import_dic, file(file_url, "w"), sort_keys=True, indent=4, separators=(u',', u': '))

if __name__ == "__main__":
    debug = Importor()
    #debug.import_chapter(u"mk", u"9")
    for x in xrange(2, 17):
        debug.import_chapter(u"mk", unicode(x))


