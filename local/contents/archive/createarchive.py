#! /Library/Frameworks/Python.framework/Versions/3.4/bin/python3

# from csv to html(slim) table.
# script for python3.

import sys
import sqlite3
import datetime

outputdir = "../slim/archive/"

def add_value(text, variable, value):
  text.append(variable + ' = ' + str(value))

def add_str(text, str):
  text.append(str)

def table_row_td(text, cls, str):
  if (cls):
    text.append('    td.' + cls + ' ' + str)
  else:
    text.append('    td ' + str)

def table_row_post(text):
  pass

def get_weekday(i_week):
  w = ['日', '月', '火', '水', '木', '金', '土']
  if (int(i_week) < 7):
    return w[int(i_week)]
  else:
    return None


def execStage(c, stageId):
  res = c.execute("select * from stage inner join hall on stage.place = hall.id where stage.id = %s" % stageId)
  if (res):
    for i in res:
      concertid = i[0]
      concertname = i[2]
      concertnameen = i[3]
      concertdate_f = i[4]
      concertpagename = i[5]
      concertplace = i[7]
      concertplaceen = i[8]
      c_datetime = datetime.datetime.fromordinal(int(concertdate_f + 12.000001 / 24.0) - 1721425)
      concertdate = c_datetime.strftime("%Y年%m月%d日（%a）")
      timh = (concertdate_f - int(concertdate_f)) * 24.0 + 12.000001
      timm = (timh - int(timh)) * 60.0
      concerttime = "{timh:02d}:{timm:02d}".format(timh=int(timh), timm=int(timm))
    
    
    print(str(concertid) + ", " + concertname + concertplace + ", " + concertdate + concerttime)
    text = []
    
    # makoは同じディレクトリに置かれたテンプレートファイルしか使用できない
    add_str(text, '-inherit archieve.baseslim')
    add_str(text, '-block titletag_name')
    add_str(text, '  過去の演奏会 {cname}'.format(cname=concertname))
    add_str(text, '-block subpage_name')
    add_str(text, '  {cname}'.format(cname=concertname))
    add_str(text, '-block concert_date')
    add_str(text, '  {cdate} {ctime}開演'.format(cdate=concertdate, ctime=concerttime))
    add_str(text, '-block concert_place')
    add_str(text, '  {cplace}'.format(cplace=concertplace))
#    add_str(text, '-block prev_link')
#    add_str(text, '  {clink}'.format(clink=concertid - 1))
#    add_str(text, '-block next_link')
#    add_str(text, '  {clink}'.format(clink=concertid + 1))
    add_str(text, '/! body content')
    add_str(text, '.pure-g.archive-list.archive-list-title')
    add_str(text, '  .title.pure-u-1.pure-u-lg-12-24 曲名')
    add_str(text, '  .composer.pure-u-8-24.pure-u-lg-4-24 作曲')
    add_str(text, '  .arranger.pure-u-8-24.pure-u-lg-4-24 編曲')
    add_str(text, '  .pure-u-4-24.pure-u-lg-2-24 編成')
    add_str(text, '  .pure-u-4-24.pure-u-lg-2-24 演奏')
    add_str(text, '  ')
    
    res = c.execute("select * from piece where concertid = {cid}".format(cid=concertid))
    for i in res:
      add_str(text, '.pure-g.archive-list.archive-list-title')
      add_str(text, '  .title.pure-u-1.pure-u-lg-12-24 {cname}'.format(cname=i[3]))
      add_str(text, '  .composer.pure-u-8-24.pure-u-lg-4-24 {ccomp}'.format(ccomp=i[4]))
      add_str(text, '  .arranger.pure-u-8-24.pure-u-lg-4-24 {carr}'.format(carr=(i[5] if i[5] != None else '')))
      add_str(text, '  .pure-u-4-24.pure-u-lg-2-24 {ctrb}Trbs.{ccomm}'.format(ctrb=i[6], ccomm=(i[7] if i[7] != None else '')))
      add_str(text, '  .pure-u-4-24.pure-u-lg-2-24 {call}'.format(call=('全員合奏' if i[8] == True else '')))
      add_str(text, '  ')
    
    
    #print(text)
    
    with open(outputdir + concertpagename + '.slim', 'w') as fp:
      fp.write('\n'.join(text))
      fp.close()


# main

argc = len(sys.argv)

if (argc < 2):
  print('usage: python %s concert.sqlite <id>' % sys.argv[0])
  quit();

conn = sqlite3.connect(sys.argv[1])
c = conn.cursor()

if (argc == 2):
  # stageIdRawはコピーしているわけではなくpointerなので？再度c.exeucuteすると移動する
  stageIdRaw = c.execute("select id from stage")
  stageIdList = []
  for stageIds in stageIdRaw:
    stageIdList.append(stageIds[0])
  for i in stageIdList:
    execStage(c, i)

else:
  execStage(c, sys.argv[2])
  
c.close()
