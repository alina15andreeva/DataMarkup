# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class JobparserPipeline:
    def __init__(self):
        client = MongoClient(host='localhost', port=27017)
        self.mongo_base = client.vacancies2310232


    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        salary = item['salary']
        if isinstance(salary, list):
            if len(salary) == 8:
                item['salary'] = [int(re.sub(r'\D', '', salary[1])), int(re.sub(r'\D', '', salary[3])), salary[5], salary[7]]
            elif len(salary) == 6:
                item['salary'] = [int(re.sub(r'\D', '', salary[1])), salary[3], salary[5]]
            else:
                item['salary'] = salary

        collection.insert_one(item)
        return item
