#import json
import logging
import os
from NHentai import NHentai
from NHentai.entities.doujin import Doujin
from NHentai.entities.options import Sort
from NHentai.entities.page import SearchPage, PopularPage


logger = logging.getLogger("hentai_lib")
logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )


# Ищет додзинси по названию. Возвращает список додзинси
def search_doujin(name: str):
    if name != "":
        nhentai = NHentai()
        search_obj: SearchPage = nhentai.search(query=name, sort=Sort.TODAY, page=1)
        result = []
        temp = search_obj.doujins
        for i in range(len(temp)):
            result.append(temp[i].to_dict())
            result[i].pop("upload_at")
        return result


def get_doujin_by_id(id: str):
    nhentai = NHentai()
    doujin: Doujin = nhentai.get_doujin(id=id)
    result = doujin.to_dict()
    return result


# Возвращает  словарь с данными по рандомному додзинси
def get_douijin_random():
    nhentai = NHentai()
    random_doujin: Doujin = nhentai.get_random()
    result = random_doujin.to_dict()
    return result


# Возвращает  список самых популярных додзинси
def get_most_popular_list():
    nhentai = NHentai()
    doujins_popular: PopularPage = nhentai.get_popular_now()
    result = []
    temp = doujins_popular.doujins
    for i in range(len(temp)):
        result.append(temp[i].to_dict())
    return result


def delete_json():
    os.remove("current_doujin.json")


if __name__ == '__main__':

    #name = input()
    #id = get_most_popular_list()[0]["id"]
    doj = get_doujin_by_id("401424")
    #print(doj)
    #doujin2pdf(doj)
    #clear_directory()
