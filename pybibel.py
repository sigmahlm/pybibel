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

from bottle import route, run, template, error, static_file, debug

CONFIG = {
    "data" : "BibelData",
    "static" : "views",
    
    
}

import biblehandler
bh = biblehandler.BibleHandler()

@route('/css/<css>')
def server_static(css):
    return static_file(css, root="css")

@route('/js/<js_lib>')
def server_static(js_lib):
    return static_file(js_lib, root="js")

@route('/images/<filename:re:.*\.png|.*\.jpg>')
def send_image(filename):
    if ".jpg" in filename:
        return static_file(filename, root="images", mimetype="image/jpeg")
    elif ".png" in filename:
        return static_file(filename, root='images', mimetype='image/png')

@route('/lexi/<lex_entry>')
def lexi(lex_entry=None):
    return 'Lexi-Nothing here, sorry'

@route('/')
@route('/<buch>/')
@route('/<buch>')
@route('/<buch>/<kapitel>')
@route('/<buch>/<kapitel>/')
@route('/<buch>/<kapitel>/<render_type>/')
def dynamic_text(buch="mk", kapitel=None, render_type="r"):
    if bh.check_book(buch):
        if kapitel:
            if bh.check_chapter(buch, kapitel):
                bh.load_json(buch, kapitel)
                chapters = bh.get_chapters()
                sections = bh.get_bottle_tmpl()
                attrb = {"buch":buch, "kapitel":kapitel, "sections":sections, "chapters":int(chapters)}
                if render_type == "wm":
                    return template("wikimedia.tmpl", attrb)
                elif render_type == "json":
                    jsoncontent = bh.json_content
                    return template("json.tmpl", {"jsoncontent":jsoncontent})
                else:
                    return template("design.tmpl", attrb)
            else:
                bh.load_json(buch)
                chapters = bh.get_chapters()
                text = "<p>Leider haben wir das gesuchte Kapitel <em>%s</em> von <em>%s</em> noch nicht in unserer Datenbank. Versuchen Sie einfach den Link zum Offenen Bibel Projekt. Eventuell ist der gesuchte Text schon übersetzt.</p>" %(str(kapitel), buch)
                attrb = {"buch":buch, "kapitel":kapitel, "sections":text, "chapters":int(chapters)}
                return template("design.tmpl", attrb)
        else:
            bh.load_json(buch)
            chapters = bh.get_chapters()
            attrb = {"buch":buch, "kapitel":None, "sections":bh.get_book_info(), "chapters":int(chapters)}
            return template("design.tmpl", attrb)
    else:
        return "I'm sorry no book"


@error(404)
def error404(error):
    return 'Nothing here, sorry'

debug(True)
run(host='localhost', port=8000, debug=False, reloader=True)
