import requests
import matplotlib.pyplot as plt

api_key = ''  # your api_key
api_url_rankings = 'https://www.fflogs.com:443/v1/rankings/encounter/'


def json_by_encounter_spec(encounter, spec):  # reginon:cn metric:dps
    req = requests.get(api_url_rankings+encounter, params={'api_key': api_key,
                                                           'metric': 'dps',
                                                           'class': 1,
                                                           'spec': spec,
                                                           'region': 'cn'})
    ranking_json = req.json()
    page = 1
    while 1:
        if(req.json()['hasMorePages']):
            page += 1
            print('req:page',req.json()['page'])
            print(req.json()['rankings'][0]['name'],req.json()['rankings'][0]['total'])
            req = requests.get(api_url_rankings+encounter, params={'api_key': api_key,
                                                                   'metric': 'dps',
                                                                   'class': 1,
                                                                   'spec': spec,
                                                                   'region': 'cn',
                                                                   'page': page})
            ranking_json['rankings'].extend(req.json()['rankings'])
        else:
            break
    return ranking_json


def plot_by_json(results):
    total_list = []
    for i in range(len(results['rankings'])):
        total_list.append(results['rankings'][i]['total'])

    plt.xlabel('count')
    plt.ylabel('total')

    count_per = [0.1, 0.25, 0.5, 0.75, 0.95, 0.99, 1]
    total_plot = []
    for c in count_per:
        total_plot.append(total_list[::-1][int(len(total_list)*c)-1])

    total_bar = plt.bar(range(len(total_plot)), total_plot, tick_label=count_per, color=['gray',
                                                                                         'g',
                                                                                         'b',
                                                                                         'm',
                                                                                         'orange',
                                                                                         'r',
                                                                                         'gold'])
    for b in total_bar:
        plt.text(b.get_x()+b.get_width()/2, b.get_height(), '%.1f' % b.get_height(), ha='center', va='bottom')
    plt.show()


if __name__ == '__main__':
    plot_by_json(json_by_encounter_spec('1044', '3'))
