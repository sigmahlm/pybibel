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
"""

__author__ = "Tobias Sauer, tobi.leichtdio.de"

import os, json

class Book:
    def __init__(self):
        #jedes Buch hat eine eigene Klasse; Sie enthält auch verschiedene
        #Versionen in sich und den Suchindex
        pass

class BibleHandler:
    def __init__ (self):
        """
          Read JSONBib
               MediaWiki Markup
          Generate HTML
                   Zerfania XML
                   OSIS
                   SearchIndex
        """
        lex = json.loads(file("JSON/lexi/tobi.json", "r").read())
        self.lex_keywords = lex.keys()
    
    def load_json(self, book, chapter=None):
        file_name = os.path.join("JSON",book,"header.json")
        self.json_header = json.loads(file(file_name, "r").read())
        if chapter:
            file_name = os.path.join("JSON",book,chapter+".json")
            self.json_content = json.loads(file(file_name, "r").read())

    def check_book(self, buch):
        return os.path.exists(os.path.join("JSON", buch))
    
    def check_chapter(self, buch, kapitel):
        return os.path.exists(os.path.join("JSON", buch, kapitel+".json"))
    
    def get_book_info(self):
        return self.json_header["info"]

    def get_chapters(self):
        return self.json_header["chapters"]
    
    def get_bottle_tmpl (self):
        sections = []
        count = 1
        absatz_text = u""
        tmp_section = {}
        json_content = self.json_content
        sec_headlines = json_content["sections"]
        text = json_content["text"]
        tmp_section["verse"] = []
        while count != -1:
            if sec_headlines.has_key(str(count)):
                if tmp_section:
                    # also nur wenn im tmp_section überhaupt was drinne ist.
                    tmp_section["lexikon_entrys"] = []
                    absatz_text = absatz_text.replace(" ","").lower()
                    #lexi
                    for entry in self.lex_keywords:
                        if entry.replace(" ","").lower() in absatz_text:
                            tmp_section["lexikon_entrys"].append(entry)
                    #/lexi
                    sections.append(tmp_section)
                    tmp_section = {}
                tmp_section["headline"] = unicode(sec_headlines[unicode(count)])
                #reset
                tmp_section["verse"] = []
                absatz_text = u""
            vers = unicode(text[unicode(count)])
            absatz_text += vers
            tmp_section["verse"].append((unicode(count), vers))
            count += 1
            if not text.has_key(unicode(count)):
                count = -1
                # letzte Section hinzufügen
                tmp_section["lexikon_entrys"] = []
                absatz_text = absatz_text.replace(" ","").lower()
                #lexi
                for entry in self.lex_keywords:
                    if entry.replace(" ","").lower() in absatz_text:
                        tmp_section["lexikon_entrys"].append(entry)
                #/lexi
                sections.append(tmp_section)
        return sections
        
if __name__ == "__main__":
    debug = BibleHandler()
    print debug.check_chapter("mk","1")
    debug.load_json("mk","1")
    debug.get_bottle_tmpl()

