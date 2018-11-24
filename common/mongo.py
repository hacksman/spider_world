#!/usr/bin/env python 
# coding:utf-8
# @Time :11/24/18 15:59


import copy
import json
import sys

import pymongo
from pymongo.errors import WriteError, DocumentTooLarge


class MongDb(object):
    ASCENDING = pymongo.ASCENDING
    DESCENDING = pymongo.DESCENDING

    def __init__(self, dbhost, dbport, dbname, dbuser, dbpass, log=None, max_pool_size=100):
        try:
            self.log = log

            self.conn = pymongo.MongoClient(dbhost, dbport,
                                            connectTimeoutMS=5 * 60 * 1000,
                                            serverSelectionTimeoutMS=5 * 60 * 1000,
                                            maxPoolSize=max_pool_size)
            self.db = self.conn[dbname]
            if dbuser and dbpass:
                self.connected = self.db.authenticate(dbuser, dbpass)
            else:
                self.connected = True
            self.log.info("mongodb连接完成...")
        except Exception as e:
            self.log.error('{db} {port} {name} {user} {pwd}'.format(db=dbhost, port=dbport, name=dbname, user=dbuser,
                                                                    pwd=dbpass))
            self.log.exception(e)
            sys.exit(1)

    def __del__(self):
        self.db.logout()
        self.conn.close()
        self.log.info('释放mongodb资源')

    def insert(self, table, value):
        try:
            self.db[table].insert(value)
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def update(self, table, conditions, value, s_upsert=False, s_multi=False):
        try:
            return self.db[table].update(conditions, value, upsert=s_upsert, multi=s_multi)
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def update_many(self, table, filter, update, s_upsert=False, **kwargs):
        try:
            return self.db[table].update_many(filter, update, upsert=s_upsert, **kwargs)
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def upsert(self, table, data):
        try:
            query = {'_id': data['_id']}
            if not self.db[table].find_one(query):
                self.db[table].insert(data)
            else:
                data.pop('_id')
                self.db[table].update(query, {'$set': data})
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def find_and_modify(self, table, query=None, update=None,
                        upsert=False, sort=None, full_response=False,
                        manipulate=False, **kwargs):
        query = {} if query is None else query
        try:
            self.db[table].find_and_modify(query=query, update=update, upsert=upsert,
                                           sort=sort, full_response=full_response,
                                           manipulate=manipulate, **kwargs)
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def traverse(self, table, where=None):
        cursor = None
        try:
            where = {} if where is None else where
            cursor = self.db[table].find(where, no_cursor_timeout=True)
            for item in cursor:
                yield item
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e
        finally:
            if cursor is not None:
                cursor.close()

    def traverse_batch(self, table, where=None, batch_size=500, limit=0):
        cursor = None
        try:
            where = {} if where is None else where
            cursor = self.db[table].find(where, no_cursor_timeout=True).batch_size(batch_size).limit(limit)
            for item in cursor:
                yield item
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e
        finally:
            if cursor is not None:
                cursor.close()
                # self.log.info('关闭traverse_batch游标')

    def traverse_batch_field(self, table, where=None, field=None):
        cursor = None
        try:
            where = {} if where is None else where
            if field is None:
                cursor = self.db[table].find(where, no_cursor_timeout=True).batch_size(500)
            else:
                cursor = self.db[table].find(where, field, no_cursor_timeout=True).batch_size(500)
            for item in cursor:
                yield item
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e
        finally:
            if cursor is not None:
                cursor.close()
                # self.log.info('关闭traverse_batch游标')

    def traverse_field(self, table, where, field):
        cursor = None
        try:
            where = {} if where is None else where
            cursor = self.db[table].find(where, field, no_cursor_timeout=True)
            for item in cursor:
                yield item
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e
        finally:
            if cursor is not None:
                cursor.close()

    def select_field(self, table, where=None, field_list=None):
        try:
            where = {} if where is None else where
            field_list = [] if field_list is None else field_list
            return self.db[table].find(where, field_list)
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def select(self, table, value=None):
        try:
            value = {} if value is None else value
            return self.db[table].find(value, no_cursor_timeout=True).batch_size(500)
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def select_colum(self, table, value, colum):
        try:
            return self.db[table].find(value, {colum: 1})
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def select_count(self, table, value=None):
        try:
            value = {} if value is None else value
            return self.db[table].find(value).count()
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def select_one(self, table, value):
        try:
            result = self.db[table].find(value).limit(1)  # fix-me to findOne function  find_one
            for item in result:
                return item
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e
        return None

    def select_limit(self, table, value, limit=500):
        try:
            result = self.db[table].find(value).limit(limit)  # fix-me to findOne function  find_one
            for item in result:
                return item
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e
        return None

    def select_one_field(self, table, value, field):
        try:
            result = self.db[table].find(value, field).limit(1)  # fix-me to findOne function  find_one
            for item in result:
                return item
            return None
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def find_one(self, table, query, field=None):
        try:
            if field is None:
                return self.db[table].find_one(query)
            return self.db[table].find_one(query, field)
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def select_sort(self, table, value, sort):
        try:
            return self.db[table].find(value).sort(sort)
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def delete(self, table, value):
        try:
            return self.db[table].remove(value)
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    # 删除数据库
    def drop(self, table):
        try:
            self.db[table].drop()
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.exception(e)
            raise e

    # index => [(index_colunm, pymongo.DESCENDING/pymongo.ASCENDING)]
    def create_index(self, table, index):
        try:
            # 后台建索引
            self.db[table].ensure_index(index, background=True)
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    # 删除索引
    def drop_indexes(self, table):
        try:
            # 后台建索引
            self.db[table].drop_indexes()
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def close_all_databases(self):
        try:
            admin = self.conn['admin']
            auth = admin.authenticate('admin', 'liveadmin')
            if auth:
                return admin.command({'closeAllDatabases': 1})
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e
        return None

    def traverse_(self, table, where=None):
        cursor = None
        try:
            where = {} if where is None else where
            cursor = self.db[table].find(where, no_cursor_timeout=True).sort('_utime', self.DESCENDING).batch_size(500)
            for item in cursor:
                yield item
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e
        finally:
            if cursor is not None:
                cursor.close()

    def insert_many(self, table, documents, ordered=True,
                    bypass_document_validation=False):
        try:
            if documents is None or len(documents) <= 0:
                return

            self.db[table].insert_many(
                documents=documents, ordered=ordered, bypass_document_validation=bypass_document_validation)
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except Exception as e:
            self.log.error("mongo操作异常: ")
            self.log.exception(e)
            raise e

    def insert_batch_data(self, table, data_list, is_order=False, insert=False, key='_id'):
        count = 0
        if data_list is None:
            return count

        length = len(data_list)
        if length <= 0:
            return count

        try:
            bulk = self.db[table].initialize_ordered_bulk_op() if is_order else self.db[
                table].initialize_unordered_bulk_op()
            for item in data_list:
                if insert:
                    bulk.insert(item)
                else:
                    item_copy = item.copy()
                    _id = item_copy.pop(key)
                    bulk.find({key: _id}).upsert().update({'$set': item_copy})
                count += 1
            bulk.execute({'w': 0})
            # self.log.info('insert_logs: {length}'.format(length=len(data_list)))
        except WriteError as e:
            self.log.error('mongo写入异常:')
            self.log.exception(e)
            sys.exit(1)
        except DocumentTooLarge as e1:
            self.log.error("采集数据异常:")
            for data in data_list:
                self.log.error("数据太大: {}".format(json.dumps(data, ensure_ascii=False)))
            self.log.exception(e1)
            sys.exit(1)

        except Exception as e2:
            self.log.error("mongo操作异常: ")
            self.log.exception(e2)
            raise e2

        return count

    # 重写save
    def update_save(self, table, data):
        if not isinstance(data, dict):
            return
        copy_data = copy.deepcopy(data)
        _id = copy_data.pop('_id')
        # self.log.info('_id = {}'.format(_id))
        if _id is None:
            return
        self.update(table, {'_id': _id}, {"$set": copy_data}, s_upsert=True)
        # self.log.info("存储: result = {}".format(result))
