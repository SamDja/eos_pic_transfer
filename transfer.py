import sys
import os
from shutil import copyfile
from datetime import datetime
from os.path import join
import errno

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', end='\r'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| (%d/%d) %s%%  %s' % (prefix, bar, iteration, total, percent, suffix), end = end)
    # Print New Line on Complete
    if iteration == total:
        print()

def main():
    if len(sys.argv) != 3:
        print("Correct syntax is:")
        print("$ python transfer.py <source> <destination>")

    source_dir = sys.argv[1]
    destination_dir = sys.argv[2]

    dict = {}

    pic_list = os.listdir(source_dir)

    for pic in pic_list:
        pic_date = datetime.fromtimestamp( os.stat(join(source_dir,pic)).st_birthtime).strftime('%Y_%m_%d')
        if pic_date not in dict:
            dict[pic_date] = [pic]
        else:
            dict[pic_date].append(pic)


    for key in dict:
        dest = join(destination_dir,key)
        listLength = len(dict[key])
        prefix = 'Progress:\n' + key + ':'

        if not os.path.exists(dest):
            try:
                os.mkdir(dest)
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        printProgressBar(0, listLength, prefix = prefix, suffix = 'Complete', length = 50)
        for i, pic in enumerate(dict[key]):
            source = join(source_dir,pic)
            destination = join(dest, pic)
            res = "y"
            end = ''


            if os.path.isfile(destination):
                res = input("file '%s' is already present, do you want to overwrite it (Y, n)? " % pic).lower()
                if res == 'y' or res == 'Y':
                    copyfile(source, destination)
                end = '\n'
            else:
                copyfile(source, destination)

            if i != listLength or (i == listLength and end != '\n'):
                os.system('clear')


            if end != '':
                printProgressBar(i + 1, listLength, prefix = prefix, suffix = 'Complete', length = 50, end = end)
            else:
                printProgressBar(i + 1, listLength, prefix = prefix, suffix = 'Complete', length = 50)


if __name__ == "__main__":
    main()