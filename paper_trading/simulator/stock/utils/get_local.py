import csv
def get_companies():
    num = 1
    companies = []
    company_list = []
    codes_list = []
    # NSE Companies list
    reader = csv.DictReader(open('/home/varshav/work/PycharmProjects/nse_mapping.csv', 'rb'), delimiter=',')
    for row in reader:
        company_name = row.get('Company')
        nse_code = row.get('NSE_Symbol')
        companies.append(nse_code + ' : ' + company_name)
    return companies

if __name__ == '__main__':
    get_companies()
