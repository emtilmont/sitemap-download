import requests
import os

#https://www.sec.gov/Archives/edgar/full-index/1993/QTR1/sitemap.quarterlyindex1.xml
baseurl = 'https://www.sec.gov/Archives/edgar/full-index/'
year = 1993
qtr = 1
i = 0

cwd = os.getcwd()
outputdir = os.path.join(cwd, 'output')
if not os.path.exists(outputdir) :
    os.makedirs(outputdir)

logfile = os.path.join(outputdir, 'log.txt')

while (year < 2021) :
    if i == 0 :
        url = ('%s%s/QTR%s/sitemap.quarterlyindex.xml' % (baseurl, year, qtr))
    else :
        url = ('%s%s/QTR%s/sitemap.quarterlyindex%s.xml' % (baseurl, year, qtr, i))
    with open(logfile, 'a') as file :
        file.write('Fetching URL: ' + url + '\n')
    print('Fetching URL: ' + url)
    response = requests.get(url)

    yeardir = os.path.join(outputdir, str(year))
    if not os.path.exists(yeardir) :
        os.makedirs(yeardir)

    qtrdir = os.path.join(yeardir, ('QTR%s' % qtr))
    if not os.path.exists(qtrdir) :
        os.makedirs(qtrdir)

    if response.status_code == 200 :
        with open(logfile, 'a') as file :
            file.write('Request Successful' + '\n')
        print('Request Successful')
        filename = os.path.join(qtrdir, ('sitemap.quartlerlyindex%s.xml' % i))
        with open(filename, 'wb') as file:
            print('Writing file ', filename)
            file.write(response.content)

        with open(logfile, 'a') as file :
            file.write('Writing file ' + filename + '\n')
        i = i + 1
    elif response.status_code != 200 and i == 0 :
        i = i + 1
    else :
        with open(logfile, 'a') as file :
            file.write('Request Failed for URL ' + url + 'with status code ' + str(response.status_code) + '\n')
        print('Request Failed for URL ' + url + 'with status code ' + str(response.status_code))
        qtr = 1 if qtr == 4 else qtr+1
        year = year + 1 if qtr == 1 else year
        i = 0