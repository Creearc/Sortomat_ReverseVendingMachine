from pymongo import MongoClient, ASCENDING, DESCENDING
from pprint import pprint
import random
import time


class DB:

    def __init__(self, ip='127.0.0.1', port=27017, database='plywood'):
        self.client = MongoClient( 'mongodb://{}:{}/'.format(ip, port))
        self.knowledge_base = self.client[database]

    def add(self, theme, element):
        result = self.knowledge_base[theme].insert_one(element)
        return result.inserted_id

    def delete(self, theme, element):
        self.knowledge_base[theme].delete_one(element)

    def show(self, theme):
        for obj in list(self.knowledge_base[theme].find({})):
            print(obj)

    def clear(self, theme):
        for obj in list(self.knowledge_base[theme].find({})):
            self.delete(theme=theme, element=obj)

    def find(self, theme, named_entities, answer_field):
        tmp = answer_field
        answer_field = dict()
        for element in tmp:
            answer_field[element] = 1
        answer_field['_id'] = 0
        
        out = []
        if named_entities != {}:
            for key in named_entities.keys():
                if isinstance(named_entities[key], list):
                    for element in named_entities[key]:
                        out.append({key : element})
                else:
                    out.append({key : named_entities[key]})

            named_entities = {'$and' : out}

        result = list(self.knowledge_base[theme].find(named_entities, answer_field))
        return result


    def find_manual(self, theme, named_entities, answer_field):
        tmp = answer_field
        answer_field = dict()
        for element in tmp:
            answer_field[element] = 1
        answer_field['_id'] = 0        
        result = list(self.knowledge_base[theme].find(named_entities, answer_field))
        return result


    def find_limit(self, theme, named_entities, answer_field, limit):
        tmp = answer_field
        answer_field = dict()
        for element in tmp:
            answer_field[element] = 1
            sort_fild = element
        answer_field['_id'] = 0
        result = list(self.knowledge_base[theme].find(named_entities, answer_field).sort([(sort_fild, -1)]).limit(limit))
        return result


    def count_arr_el(self, theme, named_entities_match, named_entities_group):
        tmp = named_entities_group.copy()
        for key in tmp.keys():
            named_entities = [{"$match": named_entities_match}, {"$unwind":"${}".format(key)}, {"$group":{"_id":"${}".format(key), "count": {"$sum": 1}}}]
            result = list(self.knowledge_base[theme].aggregate(named_entities))

            #pprint(result)

            #for el in result:
            #    if el['_id'] == tmp[key]:
            #        return el['count']

            return result


if __name__ == '__main__':

    #db = DB(ip='192.168.2.95', port=27017, database='plywood')
    db = DB(ip='46.229.132.100', port=27017, database='plywood')
    theme = 'rebroskleyka'

    db.knowledge_base[theme].create_index([('sec_time', DESCENDING)])
    
    # defects = ['smallhole', 'zakor', 'zazor', 'rubbish']
    defects = ['Сучки', 'Закорины', 'Зазоры', 'Мусор']

    test_info = [{'date' : '06.04.2022',
                  'sec_time': 1649238609,
                  # 'defects' : ['smallhole', 'zazor', 'zakor'],
                  'defects' : ['Сучки', 'Сучки', 'Сучки', 'Закорины', 'Закорины', 'Зазоры'],
                  'length' : random.randint(100, 200),
                  'width' : random.randint(100, 200),
                  'path_to_img' : '/folder/file.png'},
                 
                 {'date' : '06.04.2022',
                  'sec_time': 1649238623,
                  'defects' : [],
                  'length' : random.randint(100, 200),
                  'width' : random.randint(100, 200),
                  'path_to_img' : '/folder/file1.png'},
                 
                 {'date' : '06.04.2022',
                  'sec_time': 1649238631,
                  # 'defects' : ['zakor', 'rubbish'],
                  'defects' : ['Закорины', 'Мусор'],
                  'length' : random.randint(100, 200),
                  'width' : random.randint(100, 200),
                  'path_to_img' : '/folder/file2.png'},

                 {'date' : '06.04.2022',
                  'sec_time': 1649238639,
                  # 'defects' : ['zazor', 'zazor'],
                  'defects' : ['Зазоры', 'Зазоры'],
                  'length' : random.randint(100, 200),
                  'width' : random.randint(100, 200),
                  'path_to_img' : '/folder/file3.png'},]

##    db.clear(theme) 
##    for i in test_info:
##        db.add(theme=theme, element=i)

    '''
    named_entities = {}
    #named_entities = {'defects': {'$all': ['zazor']}}
    start = time.mktime(time.strptime('00:00:00 01.02.2022', '%H:%M:%S %d.%m.%Y'))
    end = time.mktime(time.strptime('00:00:00 01.03.2022', '%H:%M:%S %d.%m.%Y'))
    #named_entities['sec_time'] = start 
    named_entities['sec_time'] = {'$gt': start, '$lt': end} 
    named_entities['mode'] = '3 Середина' 
    answer_field = []
    answer = db.find_manual(theme = theme,
                            named_entities = named_entities,
                            answer_field = answer_field)
    pprint(answer)

    #'''

    
    '''
    named_entities = {}
    answer_field = ['sec_time']
    answer = db.find_limit(theme = theme,
                           named_entities = named_entities,
                           answer_field = answer_field,
                           limit = 20)

    pprint(answer)
    print(' ')
    '''


    ''' # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    answer.reverse()
    named_entities_match = {}
    named_entities_group = {}
    #named_entities_match['sec_time'] = 1649238609
    named_entities_match['sec_time'] = answer[18]['sec_time']
    named_entities_group['defects'] = ''
    answer = db.count_arr_el(theme=theme,
                             named_entities_match=named_entities_match,
                             named_entities_group=named_entities_group)
    
    out = {}
    for defect in answer:
        out[defect['_id']] = defect['count']    

    #'''


    '''
    named_entities = {}
    answer_field = ['sec_time']
    sec_times = db.find_limit(theme = theme,
                              named_entities = named_entities,
                              answer_field = answer_field,
                              limit = 20)
    sec_times.reverse()    

    named_entities = {}
    named_entities['sec_time'] = sec_times[19]['sec_time']
    answer_field = ['length', 'width']
    answer = db.find_manual(theme=theme,
                            named_entities = named_entities,
                            answer_field = answer_field)
    pprint(answer[0])
    #out = dict()
    #for defect in answer:
    #    out[defect['_id']] = defect['count'] 
    '''


    #'''
    named_entities = {}
    time = int(time.mktime(time.strptime('00:00:00 01.01.2022', '%H:%M:%S %d.%m.%Y')))
    named_entities['sec_time'] = time 
    answer_field = ['path_to_img']
    answer = db.find_manual(theme = theme,
                            named_entities = named_entities,
                            answer_field = answer_field)
    
    pprint(answer)
    #'''
    
#    print(' ')
#    print(len(answer))
