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
"""

import urllib2
response = urllib2.urlopen('http://www.offene-bibel.de/wiki/api.php?format=txt&action=query&titles=Markus_1&prop=revisions&rvprop=content')
html = response.read()
