# -*- coding: utf-8 -*-
'''
Copyright 2018, University of Freiburg.
Chair of Algorithms and Data Structures.
Markus Näther <naetherm@informatik.uni-freiburg.de>
'''

import urllib
import codecs
import os
import glob
import http

from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from six.moves import cPickle

drop_out_lines = [
  "Subscribe to receive email notifications whenever new talks are published.",
  "Thanks! Please check your inbox for a confirmation email. ",
  "If you want to get even more from TED, like the ability to save talks to watch later, sign up for a TED account now. ",
  "TED.com translations are made possible by volunteer translators. Learn more about the Open Translation Project."
]

class TEDExtract(object):
  '''
  Simple ted extraction tool. Returns csv files for all transcripts of 
  all ted talks (defined by the number of pages)
  '''

  def __init__(self, args):
    '''
    Constructor.
    '''
    self.args = args

    # Dictionary containing all talks
    self.all_talks = {}

  def run(self):
    '''
    Receive all information from the ted page. 
    Parse all pages and save their transcripts in own csv files.
    '''

    if os.path.isfile(os.path.join(self.args.output, 'talk_list.pkl')):
      with open(os.path.join(self.args.output, 'talk_list.pkl'), 'rb') as fin:
        self.all_talks = cPickle.load(fin)
    else:
      # Collect all talks from all pages
      for p in range(1, self.args.max_pages + 1):
        path = 'https://www.ted.com/talks?page={}'.format(p)

        self._fetch_talk_list(path)

      with open(os.path.join(self.args.output, 'talk_list.pkl'), 'wb') as fout:
        cPickle.dump(self.all_talks, fout)

    # DEBUG
    
    hdr= { 'User-Agent' : 'TEDExtract - some academic stuff' }
    conn = http.client.HTTPConnection('www.ted.com')
    # Loop through all talks and download the content for all available languages
    for i in self.all_talks:
      self._fetch_talk_content(conn, hdr, i)
    conn.close()

  def _fetch_talk_list(self, path):
    '''
    This method is used to receive all 
    '''
    print("Reading talks of \'{}\'".format(path))
    content = urllib.request.urlopen(path).read()
    soup = BeautifulSoup(content)
    talks = soup.find_all("a", class_='ga-link')
    for i in talks:
      if i.attrs['href'].find('/talks/') == 0 and self.all_talks.get(i.attrs['href']) != 1:
        self.all_talks[i.attrs['href']] = 1

    sleep(self.args.delay)
    
  def _fetch_talk_content(self, conn, hdr, talk):
    '''
    '''
    # Extract the talk name
    talkname = talk[7:]

    if os.path.isfile(os.path.join(self.args.output, talkname + '.csv')):
      print("Already there, skip {}".format(talk))
    else:
      # The data frame object for saving all languages
      req = urllib.request.urlopen('https://ted.com' + talk + '/transcript').read()
      #conn.request('GET', talk + '/transcript', headers=hdr)
      #req = conn.getresponse().read()
      print("Search URL: {}".format(talk + '/transcript'))
      soup = BeautifulSoup(req)

      df = pd.DataFrame()

      for i in soup.findAll('link'):
        if i.get('href') != None and i.attrs['href'].find('?language=') != -1:
          lang = i.attrs['hreflang']
          path = i.attrs['href']
          print("Path: {}".format(path))
          #conn.request('GET', path, headers=hdr)
          #r1 = conn.getresponse().read()
          r1 = urllib.request.urlopen(path).read()
          soup1 = BeautifulSoup(r1)
          text_talk = []
          for i in soup1.findAll('p',class_=''):
            temo = i.text.replace('\n',' ')
            temo = temo.replace('\t','')
            temo = temo.replace('\r','')
            temo = temo.replace('  ',' ')

            if temo[0] == ' ':
              temo = temo[1:]

            if temo in drop_out_lines:
              pass
            else:
              text_talk.append(temo)
          df1 = pd.DataFrame()
          df1[lang] = text_talk
          df = pd.concat([df,df1],axis=1)

          # This break is necessary, otherwise we'll receive a 429. THere would be
          # a potential wordaround as noted by the commented out code snippets, but
          # unfortunately this is not working
          sleep(self.args.delay)

      df.to_csv(os.path.join(self.args.output, talkname + '.csv'), sep='\t', encoding='utf-8')