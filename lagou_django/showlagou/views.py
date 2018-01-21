import sys
import os
sys.path.append(os.path.abspath('..'))

from django.shortcuts import render
from lagou.model import mysqldb
from lagou.model.mysqldb import lagou_position_info
from peewee import fn
import json


# Create your views here.
def index(request):
    try:
        mysqldb.db.connect()
        nums = lagou_position_info.select(lagou_position_info.position_kind, fn.Count(1).alias('kind_num')).\
            group_by(lagou_position_info.position_kind)
        kinds = {}
        for num in nums:
            kinds[num.position_kind] = num.kind_num

        position_kind = []
        kind_num = []
        kind = sorted(kinds.items(), key=lambda d:d[1], reverse=True)[:15]
        for i in range(15):
            position_kind = position_kind + [kind[i][0]]
            kind_num = kind_num + [kind[i][1]]

        return render(request, 'index.html', {'position_kind': position_kind, 'kind_num': kind_num})
    except Exception as e:
        print(e)

