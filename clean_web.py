import os
from bs4 import BeautifulSoup


retval = os.getcwd()
print("Current Path: %s" % retval)
output_dir = '../corpus3/'

process_path = retval + '/../' + 'web'

for foldername in os.listdir(process_path):
    file_path = process_path + '/' + foldername
    for filename in os.listdir(file_path):
        file = open(file_path + '/' + filename, 'r')
        soup = BeautifulSoup(file)
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        write_file_path = output_dir + foldername + '-' + filename
        write_file = open(write_file_path, 'w')
        for line in text.encode('utf-8'):
            write_file.write(line)
        write_file.close()
        print('Finish the %s of %s' % (filename, foldername))
    print('--------------------- %s finished ---------------------' % foldername)