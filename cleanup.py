#!/usr/bin/env python
#
# cleanup.py
#
# Simple script that cleanup filename in directory
#
# Author: Florent MONTHEL (fmonthel@flox-arts.net)
#

import os
import shutil
import argparse
import ConfigParser
import re
import datetime
from terminaltables import AsciiTable

def main() :

    # Options
    parser = argparse.ArgumentParser(description='Script to clean up filename into directory')
    parser.add_argument('--directory', action='store', dest='dir', default='./torrent')
    args = parser.parse_args()

    # Parameters
    time_start = datetime.datetime.now()
    file_config = os.path.join(os.path.dirname(__file__), 'conf/config.ini')
    Config = ConfigParser.ConfigParser(allow_no_value = True)
    Config.read(file_config)
    
    # Extensions in a list
    ext_video = Config.get('EXTENSION','video').split(',')
	# Word to clean in a list
    word_toclean = [x[0] for x in Config.items('TOCLEAN')]
    
    # Ascii table
    myAsciiTable = [['Old filename','New filename','Action']]

    # Parse directory
    for root, directories, filenames in os.walk(args.dir):
        for filename in filenames :
            # Build list for output
            tmpdata = list()
            tmpdata.append(os.path.join(root,filename)) # Current path
            # Working area
            ext = os.path.splitext(filename)[1][1:].lower()
            new_filename = os.path.splitext(filename)[0]
            if ext in ext_video and not filename.startswith('.') :
                new_filename = filename_cleanup(new_filename,word_toclean)+'.'+ext
                new_filename_path = os.path.join(args.dir,new_filename)
                tmpdata.append(new_filename_path) # New path
                if new_filename != filename :
                    tmpdata.append('filename cleanup done')
                elif new_filename_path != os.path.join(root,filename) :
                    tmpdata.append('path cleanup done')
                else :
                    tmpdata.append('nothing todo')
                # Move file
                shutil.move(os.path.join(root,filename),new_filename_path)
            else : # Nothing todo as no extention managed
                tmpdata.append('')
                tmpdata.append('extension not managed - nothing todo')
            # Add tmpdata list to myAsciiTable 
            myAsciiTable.append(tmpdata)
    # Parse directory again for cleanup
    for root, directories, filenames in os.walk(args.dir) :
        for directory in directories :
            # Build list for output
            tmpdata = list()
            tmpdata.append(os.path.join(root,directory))
            tmpdata.append('')
            # Delete dir if empty
            if not os.listdir(os.path.join(root,directory)) :
                shutil.rmtree(os.path.join(root,directory))
                tmpdata.append('directory deleted as empty')
            else :
                tmpdata.append('directory not empty - nothing todo')
            # Add tmpdata list to myAsciiTable 
            myAsciiTable.append(tmpdata)
    # Create AsciiTable and total
    tmpdata = list()
    tmpdata.append("Total : " + str(len(myAsciiTable) - 1) + " row(s)")
    tmpdata.append("")
    myAsciiTable.append(tmpdata)
    myTable = AsciiTable(myAsciiTable)
    myTable.inner_footing_row_border = True
    # End script
    time_stop = datetime.datetime.now()
    time_delta = time_stop - time_start
    # Output data
    print "######### Date : %s - App : %s #########" % (time_start.strftime("%Y-%m-%d"),Config.get('GLOBAL','application'))
    print "- Start time : %s" % (time_start.strftime("%Y-%m-%d %H:%M:%S"))
    print "- Finish time : %s" % (time_stop.strftime("%Y-%m-%d %H:%M:%S"))
    print "- Delta time : %d second(s)" % (time_delta.total_seconds())
    print myTable.table

def filename_cleanup(filename,word_toclean) :
    ''' Clean the filename '''

    for word in word_toclean :
        # Clean word as is
        filename = re.sub(word, '', filename.strip(' \t\n\r\.'))
        # Clean word "cleaned"
        word = string_cleanup(word)
        filename = re.sub(word, '', filename.strip(' \t\n\r\.'))
    # Generic cleaning
    filename = string_cleanup(filename)
    return filename

def string_cleanup(string) :
    ''' Clean string '''
    
    # Generic cleaning
    string = re.sub('[^\w\s-]', '-', string.strip(' \t\n\r\.').lower())
    string = re.sub('[-\s]+', '-', string)
    return string 

if __name__ == "__main__":
    main()
