from bs4 import BeautifulSoup
from requests import get

url = "https://etherscan.io/tokentxns?a=0xfe9e8709d3215310075d67e3ed32a380ccf451c8&p="

def get_transactions():
    transactions = []
    for i in range(1, 201):
        response = get(url + str(i))
        html = BeautifulSoup(response.text, 'html.parser')
        table = html.find_all('table')[0].find_all('tr')
        for tran in table[1:]:
            infos = tran.find_all('td')
            _time = infos[1].find('span')['title'].encode('utf8').strip()
            _from = infos[2].get_text().encode('utf8').strip()
            _to = infos[4].get_text().encode('utf8').strip()
            _value = infos[5].get_text().encode('utf8').strip().replace(',','')
            _token = infos[6].get_text().encode('utf8').strip()
            transactions.append({   'token': _token,
                                    'from': _from,
                                    'to': _to,
                                    'time': _time,
                                    'value': _value,
                                    'token': _token})
    return transactions

def get_cycles(transactions):
    in_trans = {}
    out_trans = {}
    cycles = []
    for tran in transactions:
        if tran['token'] not in in_trans:
            in_trans[tran['token']] = []
        if tran['to'] == "Binance_5":
            if tran['token'] in in_trans and len(in_trans[tran['token']]) > 0:
                if in_trans[tran['token']][-1]['from'] == "Binance_5":
                    cycles.append(in_trans[tran['token']])
                    del in_trans[tran['token']]
                    in_trans[tran['token']] = []               

            in_trans[tran['token']].append(tran)
        if tran['from'] == "Binance_5":
            in_trans[tran['token']].append(tran)
    for cycle in in_trans:
        cycles.append(cycle)
    return cycles

def get_total(cycle):
    total_in = 0
    total_out = 0
    for tran in cycle:
        if tran['to'] == "Binance_5":
            total_in += int(tran['value'])
        if tran['from'] == "Binance_5":
            total_out += int(tran['value'])
    return total_in, total_out

def find_entry(cycles):
    for cycle in cycles:
        