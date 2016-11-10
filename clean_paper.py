import os
import re

retval = os.getcwd()

print ("Current Path: %s" % retval)

body_output_dir = retval + '/../corpus4/'
abstract_output_dir = retval + '/../corpus5/'
process_path = retval + '/../paper'



for foldername in os.listdir(process_path):
    file_path = process_path + '/' + foldername
    paper_idx = 0

    for filename in os.listdir(file_path):
        paper_idx += 1
        file = open(file_path + '/' + filename, 'r')
        paper = file.read()

        # regular expression
        abstract_ = re.search('Abstract|ABSTRACT', paper).span()
        intro_ = re.search('Introduction|INTRODUCTION', paper).span()
        reference_ = re.search('References|REFERENCES', paper).span()

        # extract abstract section and body part of paper
        ABSTRACT = paper[abstract_[1]:(intro_[0] - 2)]
        BODY = paper[intro_[0]:reference_[0]]

        # write into output files for abstract
        write_body_path = body_output_dir + foldername + '-body-' + str(paper_idx) + '.txt'
        write_file = open(write_body_path, 'w')
        for line in BODY:
            write_file.write(line)
        write_file.close()

        # write into output file for body
        write_abstract_path = abstract_output_dir + foldername + '-abstract-' + str(paper_idx) + '.txt'
        write_file = open(write_abstract_path, 'w')
        for line in ABSTRACT:
            write_file.write(line)
        write_file.close()

        print('Finish the %s of %s' % (filename, foldername))
    print('--------------------- %s finished ---------------------' % foldername)