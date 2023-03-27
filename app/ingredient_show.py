'''Description.'''
import pandas as pd
import re

def request_names(request):
    '''
    Documentation.
    '''
    a = pd.read_pickle('instance/ingr_map.pkl')
    a['replaced'].replace('flmy','flour',inplace=True)
    all_items = ','.join(list(set(a['replaced'])))
    a.set_index('raw_ingr',inplace=True)
    all_items = ',' +all_items
    all_items = all_items + ','
    results = re.findall(f',[ \w]*{request}[A-Za-z]*[ \w]*,', all_items)
    results = [elem[1:-1] for elem in results]
    results.sort(key = lambda x: len(x))
    return {i: results[i] for i in range(min(8,len(results)))}
