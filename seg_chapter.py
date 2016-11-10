import os
import re

def search_chapter(novel, res):
    chap = re.search('Chapter|chapter|CHAPTER', novel)
    if chap:
        chap_pos = chap.span()
        next_start_point = long(chap_pos[1])
        res.append(next_start_point)
        search_chapter(novel[next_start_point:], res)
        return True
    return False

retval = os.getcwd()
print("Current Path: %s" % retval)
folder_path = retval + '/../novel'
output_dir = retval + '/../corpus2/'

for foldername in os.listdir(folder_path):
    file_path = folder_path + '/' + foldername
    for filename in os.listdir(file_path):
        res = []
        file = open(file_path + '/' + filename, 'r')
        novel = file.read()
        # regular expression for chapter
        flag = search_chapter(novel, res)

        # check the result list
        if flag:
            # initialize cursor
            cursor = res[0]
            for idx in xrange(len(res)):
                front = cursor

                if idx == len(res)-1:
                    chap_seg = novel[front-7:]
                else:
                    # update cursor
                    end = cursor + res[idx + 1]
                    cursor = end

                    chap_seg = novel[front-7:end-7]

                # write the chapter segment into .txt file
                write_chap_seg_path = output_dir + filename.split('.')[0] + '-chapter' + str(idx+1) + '.txt'
                write_file = open(write_chap_seg_path, 'w')
                for line in chap_seg:
                    write_file.write(line)
                write_file.close()
            print("Done %s -- %s" % (foldername, filename))
        else:
            # write the whole novel since there is no chapter
            print("%s -- %s has no any chapter." % (foldername, filename))

