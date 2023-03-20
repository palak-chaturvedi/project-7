import urllib2
import bs4
import os, csv
import sys
from datetime import datetime
import workdays
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re

# Path for spark source folder
os.environ['SPARK_HOME'] = "/home/sparkCluster/work/spark-1.4.1-bin-hadoop2.4"

# Append pyspark  to Python Path
sys.path.append("/home/sparkCluster/work/spark-1.4.1-bin-hadoop2.4/python/")

try:
    from pyspark import SparkContext
    from pyspark import SparkConf
    from pyspark import SparkContext
    from pyspark.mllib.feature import HashingTF
    from pyspark.mllib.regression import LabeledPoint
    from pyspark.mllib.classification import NaiveBayes
    from pyspark import SparkConf
    from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
    from pyspark.mllib.linalg import Vectors

    print ("Successfully imported Spark Modules")

except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)

sc = SparkContext(appName="Test")
sameModel = NaiveBayesModel.load(sc, "/home/sparkCluster/work/PycharmProjects/StockAnalysis/myModel")
htf = HashingTF(50000)

pg_no = 1
company_name = []
company_list = []
companies = []
codes_list = []
comp = []
experts = []
stopwords = []
exclude = []


def getCompanyName():
    global comp
    # NSE Companies list
    reader = csv.DictReader(open('/home/sparkCluster/work/PycharmProjects/nse_mapping.csv', 'rb'), delimiter=',')
    for row in reader:
        company_name = row.get('Company')
        words = company_name.lower().split(" ")
        for word in words:
            if word not in comp:
                comp.append(word)
        nse_code = row.get('NSE_Symbol')
        comp.append(nse_code.lower())


def process(line, stopwords):
    newline = []
    neg = ["dont", "not","no"]
    words = line.split(" ")
    #words = [w for w in words if not w in stopwords]
    #print words
    for word in words:
        if word not in stopwords:
            newline.append(word + " ")
    line = ''.join(newline)

    f = []
    words = line.split(" ")
    for word in words:
        if word in neg:
            pos = words.index(word)
            if pos>0 and pos<(len(words)-1):
                words[pos-1] = "!"+words[pos-1]
                words[pos+1] = "!"+words[pos+1]
            else:
                if pos==0:
                    words[pos+1] = "!"+words[pos+1]
                else:
                    if pos==len(words):
                        words[pos-1] = "!"+words[pos-1]
    new_words = []
    for word in words:
        new_words.append(word+" ")
    return ''.join(new_words)

def process_punct(line):
    line= line.lower()
    re.sub('^[0-9 ]+', '',line)
    line = re.sub(' - ', ' ', line)
    line = re.sub(',', ' ', line)
    line = re.sub('\.', ' ', line)
    line = re.sub(" rs ", '  ', line)
    line = re.sub("says", '  ', line)
    line = re.sub("Says", '  ', line)
    line = re.sub("advices", ' ', line)
    line = re.sub("advises", ' ', line)
    line = re.sub(" q ", ' ', line)
    line = re.sub('%', ' ', line)
    line = re.sub('\?', ' ', line)
    line = re.sub('\'', '', line)
    line = re.sub(';', ' ', line)
    line = re.sub(':', ' ', line)
    line = re.sub('!', ' ', line)
    line = re.sub('@', ' ', line)
    line = re.sub('/', ' ', line)
    line = re.sub('"', ' ', line)
    line = re.sub('\$', ' ', line)
    line = re.sub('[\s]+', ' ', line)
    return line

def getStopwords():
    global stopwords
    f = open('/home/sparkCluster/work/PycharmProjects/StockAnalysis/stopwords.txt', 'r')
    ys = f.readlines()
    for y in ys:
        stopwords.append(y[:-1])

def get_nse():
    global company_name
    global company_list
    global companies
    global codes_list
    reader = csv.DictReader(open('/home/sparkCluster/work/PycharmProjects/nse_mapping.csv', 'rb'), delimiter=',')
    for row in reader:
        company_name = row.get('Company')
        company_list.append(company_name)
        nse_code = row.get('NSE_Symbol')
        codes_list.append(nse_code)
        companies.append(nse_code)
        #name = name.lstrip().rstrip()
        companies.append(company_name)

        words = company_name.lower().split(" ")
        for word in words:
            if word not in comp:
                comp.append(word)
        comp.append(nse_code.lower())


def getExpertsname():
    global experts
    # NSE Companies list
    reader = csv.DictReader(open('/home/sparkCluster/work/PycharmProjects/StockAnalysis/datasets/experts1.tsv', 'rb'), delimiter='\t')
    for row in reader:
        name = row.get('expert_name')
        words = name.lower().split(" ")
        for word in words:
            if word not in experts:
                experts.append(word)

def scrape():
    x = 0
    global pg_no
    # Page

    URL = "http://www.moneycontrol.com/elite/section/technical-experts/2-9-"+str(pg_no)+".html"
    # Download the page data and create a BeautitulSoup object
    Page = urllib2.urlopen(URL)
    Text = Page.read()
    soup = bs4.BeautifulSoup(Text, "html.parser")

    letters = soup.find_all("div", "expcontent")


    # expert1 = soup.find("a", "bl16")
    # expert = expert1.get_text()
    for element in letters:
        tgt = -1
        # ---- date -----
        date = element.find("p", "gry_11")
        dt_str = date.get_text()
        dt_obj = datetime.strptime(dt_str, '%I:%M %p | %d %b %Y |').date()
        date1 = dt_obj.__str__()
        td = datetime.now().date()
        prev_day = workdays.workday(td,-2)
        if dt_obj >= prev_day:
            x = 1
            comment1 = element.a.get_text()
            comment2 = comment1.encode('utf-8')
            formattedComment = comment2.__str__()
            if ":" in formattedComment:
                formattedComment2, rest1 = formattedComment.split(":", 1)
            else:
                formattedComment2 = formattedComment

            final_comment = formattedComment2

            formattedComment2 = re.sub('-', ' ', formattedComment2)

            words = formattedComment2.lower().split(" ")

            for i,word in enumerate(words):
                    if word == "rs":
                        try:
                            num = float(words[i+1])
                            tgt = float(words[i+1])
                            break
                        except:
                            continue
                    try:
                        num=float(word)
                        tgt = float(word)
                        break
                    except:
                        continue

            re.sub('^[0-9 ]+', '', formattedComment2.lower())
            c = process_punct(formattedComment2)

            new_comm = process(c,str(comp))

            sent = sameModel.predict(htf.transform(new_comm.lower()))
            if sent==1.0:
                sentiment = "buy"
            else:
                if sent == 2.0:
                    sentiment = "sell"
                else:
                    sentiment = "hold"

            if re.search(r'sell',c):
                sentiment = "sell"
            else:
                if re.search(r'buy',c):
                    sentiment = "buy"

            m = 0
            for company in companies:
                value=fuzz.token_set_ratio(formattedComment2, company)
                # print company+ "-- "+str(value)
                if(value>=m):
                    m=value
                    match=company
            # print "--------------------------------------------"

            nse=""

            #match = process.extractOne(formattedComment2,companies)
            #print match
            if company_list.__contains__(match):
                with open("/home/sparkCluster/work/PycharmProjects/nse_mapping.csv", 'r') as file:
                    reader = csv.reader(file)
                    nse = [line[2] for line in reader if line[0] == match]
                    final_nse = nse[0]
            else:
                if codes_list.__contains__(match):
                    nse = match
                    final_nse = nse

            print final_nse

            expert = element.find("p", "gry_13")
            expertName1 = expert.get_text()
            expertName2 = expertName1.encode('utf-8')
            expertName = expertName2.__str__()
            if "," in expertName:
                formattedName, rest2 = expertName.split(",", 1)
            else:
                formattedName = expertName

            a = formattedName.lower().lstrip().rstrip()
            g=0
            reader1 = csv.DictReader(open('/home/sparkCluster/work/PycharmProjects/StockAnalysis/datasets/experts1.tsv', 'rb'), delimiter='\t')
            for row in reader1:
                exp_name1 = row.get('expert_name')
                b = exp_name1.lower().lstrip().rstrip()
                if a == b:
                    g = 1
                    exp_id = row.get('Expert_id')
            if g!=1:
                exp_id = 1
            #print formattedName
            # f = open("/home/admin/work/newtrain.txt", 'a')
            csvFile = open('/home/sparkCluster/django-projects/stock_website/static/stock/csvs/dummy_comments.csv', 'a')
            csvWriter = csv.writer(csvFile, delimiter='\t', lineterminator='\n')
            print str(exp_id)+"     "+formattedComment2+" -- "+new_comm+" --> "+process_punct(formattedComment2)+": "+final_nse+" "+sentiment+" "+str(tgt)
            csvWriter.writerow([str(exp_id),final_comment,final_nse,sentiment,tgt])
            # s = formattedName + "\t" + formattedComment + "\t" + date1 + "\n"
            # f.write(s)

        else:
            x = 0
            break

    if x == 1:
        pg_no += 1
    return x


def scrape_brok():
    x = 0
    global pg_no
    # Page
    URL = "http://www.moneycontrol.com/elite/section/-experts/2-25-"+str(pg_no)+".html"
    # Download the page data and create a BeautitulSoup object
    Page = urllib2.urlopen(URL)
    Text = Page.read()
    soup = bs4.BeautifulSoup(Text, "html.parser")

    letters = soup.find_all("div", "expcontent")


    # expert1 = soup.find("a", "bl16")
    # expert = expert1.get_text()
    for element in letters:
        tgt = -1
        # ---- date -----
        date = element.find("p", "gry_11")
        dt_str = date.get_text()
        dt_obj = datetime.strptime(dt_str, '%I:%M %p | %d %b %Y |').date()
        date1 = dt_obj.__str__()
        td = datetime.now().date()
        prev_day = workdays.workday(td,-2)
        if dt_obj >= prev_day:
            x = 1
            comment1 = element.a.get_text()
            comment2 = comment1.encode('utf-8')
            formattedComment = comment2.__str__()
            if ":" in formattedComment:
                formattedComment2, rest1 = formattedComment.split(":", 1)
            else:
                formattedComment2 = formattedComment

            final_comment = formattedComment2

            formattedComment2 = re.sub('-', ' ', formattedComment2)

            words = formattedComment2.lower().split(" ")

            for i,word in enumerate(words):
                    if word == "rs":
                        try:
                            num = float(words[i+1])
                            tgt = float(words[i+1])
                            break
                        except:
                            continue
                    try:
                        num=float(word)
                        tgt = float(word)
                        break
                    except:
                        continue

            re.sub('^[0-9 ]+', '', formattedComment2.lower())
            c = process_punct(formattedComment2)

            new_comm = process(c,str(comp))

            sent = sameModel.predict(htf.transform(new_comm.lower()))
            if sent==1.0:
                sentiment = "buy"
            else:
                if sent == 2.0:
                    sentiment = "sell"
                else:
                    sentiment = "hold"

            if re.search(r'sell',c):
                sentiment = "sell"
            else:
                if re.search(r'buy',c):
                    sentiment = "buy"

            m = 0
            for company in companies:
                value=fuzz.token_set_ratio(formattedComment2, company)
                # print company+ "-- "+str(value)
                if(value>=m):
                    m=value
                    match=company
            # print "--------------------------------------------"

            nse=""

            #match = process.extractOne(formattedComment2,companies)
            #print match
            if company_list.__contains__(match):
                with open("/home/sparkCluster/work/PycharmProjects/nse_mapping.csv", 'r') as file:
                    reader = csv.reader(file)
                    nse = [line[2] for line in reader if line[0] == match]
                    final_nse = nse[0]
            else:
                if codes_list.__contains__(match):
                    nse = match
                    final_nse = nse

            print final_nse

            expert = element.find("p", "gry_13")
            expertName1 = expert.get_text()
            expertName2 = expertName1.encode('utf-8')
            expertName = expertName2.__str__()
            if "," in expertName:
                formattedName, rest2 = expertName.split(",", 1)
            else:
                formattedName = expertName

            a = formattedName.lower().lstrip().rstrip()
            g=0
            reader1 = csv.DictReader(open('/home/sparkCluster/work/PycharmProjects/StockAnalysis/datasets/experts1.tsv', 'rb'), delimiter='\t')
            for row in reader1:
                exp_name1 = row.get('expert_name')
                b = exp_name1.lower().lstrip().rstrip()
                if a == b:
                    g = 1
                    exp_id = row.get('Expert_id')
            if g!=1:
                exp_id = 1
            #print formattedName
            # f = open("/home/admin/work/newtrain.txt", 'a')
            csvFile = open('/home/sparkCluster/django-projects/stock_website/stock/static/stock/csvs/dummy_comments.csv', 'a')
            csvWriter = csv.writer(csvFile, delimiter='\t', lineterminator='\n')
            print str(exp_id)+"    "+date1+"   "+final_comment+" -- "+new_comm+" --> "+process_punct(formattedComment2)+": "+final_nse+" "+sentiment+" "+str(tgt)
            csvWriter.writerow([str(exp_id),final_comment,final_nse,sentiment,tgt])
            # s = formattedName + "\t" + formattedComment + "\t" + date1 + "\n"
            # f.write(s)

        else:
            x = 0
            break

    if x == 1:
        pg_no += 1
    return x


def scr_call():
    if os.path.exists('/home/sparkCluster/django-projects/stock_website/stock/static/stock/csvs/dummy_comments.csv'):
        os.remove('/home/sparkCluster/django-projects/stock_website/stock/static/stock/csvs/dummy_comments.csv')
    csvFile = open('/home/sparkCluster/django-projects/stock_website/stock/static/stock/csvs/dummy_comments.csv', 'a')
    csvWriter = csv.writer(csvFile, delimiter='\t', lineterminator='\n')
    csvWriter.writerow(["expert_id","comments","company_code","sentiment","target"])
    csvFile.close()
    print "done"

    global exclude
    #getCompanyName()
    getExpertsname()
    get_nse()
    getStopwords()
    for s in stopwords:
        exclude.append(s)
    for e in experts:
        exclude.append(e)
    for e in comp:
        exclude.append(e)

    global pg_no
    #if os.path.exists('/home/varshav/django-projects/stock_website/stock/static/stock/csvs/comments.csv'):
     #   os.remove('/home/varshav/django-projects/stock_website/stock/static/stock/csvs/comments.csv')
    page = 1
    #sc = SparkContext(appName="Test")
    x = 1
    while x:
        x = scrape()
    pg_no=1

    y = 1
    while y:
        y = scrape_brok()
    pg_no=1
    sc.stop()


def main():
    scr_call()


if __name__ == "__main__":
    main()
