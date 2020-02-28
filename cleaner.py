#!/usr/bin/python

import mysql.connector

username="db_admin"
password ="password"
host = "127.0.0.1"
database="database_name"

prefix = "wp_"

tables=[
    "commentmeta",
    "comments",
    "event_hours",
    "event_hours_booking",
    "layerslider",
    "layerslider_revisions",
    "links",
    "options",
    "postmeta",
    "posts",
    "revslider_css",
    "revslider_css_bkp",
    "revslider_layer_animations",
    "revslider_layer_animations_bkp",
    "revslider_navigations",
    "revslider_navigations_bkp",
    "revslider_sliders",
    "revslider_sliders_bkp",
    "revslider_slides",
    "revslider_slides_bkp",
    "revslider_static_slides",
    "revslider_static_slides_bkp",
    "term_relationships",
    "term_taxonomy",
    "termmeta",
    "terms",
    "timetable_guests",
    "tour_bookings",
    "tour_dates",
    "tour_times",
    "usermeta",
    "users",
    "wfblockediplog",
    "wfblocks7",
    "wfconfig",
    "wfcrawlers",
    "wffilechanges",
    "wffilemods",
    "wfhits",
    "wfhoover",
    "wfissues",
    "wfknownfilelist",
    "wflivetraffichuman",
    "wflocs",
    "wflogins",
    "wfls_2fa_secrets",
    "wfls_settings",
    "wfnotifications",
    "wfpendingissues",
    "wfreversecache",
    "wfsnipcache",
    "wfstatus",
    "wftrafficrates",

]

tables = ["posts"]

fields = {}

cnx =mysql.connector.connect(user=username, password=password,
 host=host,
 database="information_schema")


cursor = cnx.cursor()

for table in tables:
    cursor.execute("select column_name from columns where table_name='"+prefix+table+"' and table_schema='"+database+"'")
    res = cursor.fetchall()
    fields[table] = []
    for x in res:
        fields[table].append(x[0])

cursor.close()
cnx.close()

cnx =mysql.connector.connect(user=username, password=password,
 host=host,
 database=database)


cursor = cnx.cursor()

y = "<script"
yy = "</script>"
print("Started!")
for table in tables:
    for cname in fields[table]:
        try:
            cursor.execute("SELECT "+cname+",ID FROM "+prefix+table)
            res = cursor.fetchall()
        except:
            continue
       

        for x in res:
            post = str(x[0])
            id = x[1]
            mods = False
            post = post.strip()

            if len(post) < len(y):
                continue

            if len(post) < len(yy):
                continue

          
            if post[:len(y)+1].lower().find(y) >-1:
                post = post[post.find(yy) + len(yy):]
                mods = True
                

            if post[-len(yy):].lower().find(yy) > -1:
                post = post[:post.rfind(y)]
                mods = True


            if mods:
                post = post.replace("\"", "'")
                post = post.replace("\\", "\\\\")
                if len(post.strip()) == 0:
                        post =" "

             
                try:
                  cursor.execute("UPDATE "+prefix+table+" set "+cname+"=\""+post+"\" where ID = "+str(id))
                except:
                  pass




cursor.close()
cnx.close()
