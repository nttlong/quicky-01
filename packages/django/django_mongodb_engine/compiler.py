from functools import wraps
import re
import sys

import django
from django.db.models import F, NOT_PROVIDED
from django.db.models.sql import aggregates as sqlaggregates
from django.db.models.sql.constants import MULTI
from django.db.models.sql.where import OR
from django.db.utils import DatabaseError, IntegrityError
from django.utils.encoding import smart_str
from django.utils.tree import Node

from pymongo import ASCENDING, DESCENDING
from pymongo.errors import PyMongoError, DuplicateKeyError

from djangotoolbox.db.basecompiler import (
    NonrelQuery,
    NonrelCompiler,
    NonrelInsertCompiler,
    NonrelUpdateCompiler,
    NonrelDeleteCompiler,
    EmptyResultSet)

from .aggregations import get_aggregation_class_by_name
from .query import A
from .utils import safe_regex


if django.VERSION >= (1, 6):
    def get_selected_fields(query):
        fields = None
        if query.select and not query.aggregates:
            fields = [info.field.column for info in query.select]
        return fields
else:
    def get_selected_fields(query):
        fields = None
        if query.select_fields and not query.aggregates:
            fields = [field.column for field in query.select_fields]
        return fields


OPERATORS_MAP = {
    'exact':  lambda val: val,
    'gt':     lambda val: {'$gt': val},
    'gte':    lambda val: {'$gte': val},
    'lt':     lambda val: {'$lt': val},
    'lte':    lambda val: {'$lte': val},
    'in':     lambda val: {'$in': val},
    'range':  lambda val: {'$gte': val[0], '$lte': val[1]},
    'isnull': lambda val: None if val else {'$ne': None},

    # Regex matchers.
    'iexact':      safe_regex('^%s$', re.IGNORECASE),
    'startswith':  safe_regex('^%s'),
    'istartswith': safe_regex('^%s', re.IGNORECASE),
    'endswith':    safe_regex('%s$'),
    'iendswith':   safe_regex('%s$', re.IGNORECASE),
    'contains':    safe_regex('%s'),
    'icontains':   safe_regex('%s', re.IGNORECASE),
    'regex':       lambda val: re.compile(val),
    'iregex':      lambda val: re.compile(val, re.IGNORECASE),

    # Date OPs.
    'year': lambda val: {'$gte': val[0], '$lt': val[1]},
}

NEGATED_OPERATORS_MAP = {
    'exact':  lambda val: {'$ne': val},
    'gt':     lambda val: {'$lte': val},
    'gte':    lambda val: {'$lt': val},
    'lt':     lambda val: {'$gte': val},
    'lte':    lambda val: {'$gt': val},
    'in':     lambda val: {'$nin': val},
    'isnull': lambda val: {'$ne': None} if val else None,
}


def safe_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DuplicateKeyError as e:
            raise (IntegrityError, IntegrityError(smart_str(e)), sys.exc_info()[2])
        except PyMongoError as e:
            raise (DatabaseError, DatabaseError(smart_str(e)), sys.exc_info()[2])
        except Exception as ex:
            raise (ex)

    return wrapper


class MongoQuery(NonrelQuery):

    def __init__(self, compiler, fields,schema=None):

        if schema == None:  # add schema
            import inspect
            fx = inspect.stack()
            error_detail = ""
            for x in fx:
                error_detail += "\n\t {0}, line {1}".format(fx[1], fx[2])
            raise (
                Exception(
                    "can not call ''{1}'' without schema in '{0}'.\nDetail:\n{2}".format(
                        __file__, "MongoQuery.init",
                        error_detail
                    )))
        self.schema=schema
        import threading
        ct=threading.currentThread()
        if hasattr(ct,"tenancy_code"):
            schema=ct.tenancy_code
        super(MongoQuery, self).__init__(compiler, fields)
        self.ordering = []
        self.collection = self.compiler.get_collection(schema)
        if self.collection.collection.name == "django_session":
            if schema == None:  # add schema
                import inspect
                fx = inspect.stack()
                error_detail = ""
                for x in fx:
                    error_detail += "\n\t {0}, line {1}".format(fx[1], fx[2])
                raise (
                    Exception("can not query on 'django_session' at '{1}' without schema in '{0}'\n Detail:\n{2}".format(__file__,
                                                                                                   "MongoQurey.django_session__init__",
                                                                                                   error_detail)))
            import threading
            ct=threading.currentThread()
            if hasattr(ct,"DEFAULT_DB_SCHEMA"):
                schema=ct.DEFAULT_DB_SCHEMA
            self.mongo_query = getattr(compiler.query, 'raw_query', {"schema":schema})
        else:
            self.mongo_query = getattr(compiler.query, 'raw_query', {})

    def __repr__(self):
        return '<MongoQuery: %r ORDER %r>' % (self.mongo_query, self.ordering)

    def fetch(self, low_mark, high_mark):
        results = self.get_cursor()
        pk_column = self.query.get_meta().pk.column
        for entity in results:
            entity[pk_column] = entity.pop('_id')
            yield entity

    @safe_call
    def count(self, limit=None,schema = None):
        if schema == None:  # add schema
            import inspect
            fx = inspect.stack()
            error_detail = ""
            for x in fx:
                error_detail += "\n\t {0}, line {1}".format(fx[1], fx[2])
            raise (
                Exception(
                    "can not call ''{1}'' without schema in '{0}'.\nDetail:\n{2}".format(
                        __file__, "MongoQuery.count",
                        error_detail
                    )))
        results = self.get_cursor()
        if limit is not None:
            results.limit(limit)
        return results.count()

    @safe_call
    def order_by(self, ordering):
        if isinstance(ordering, bool):
            # No need to add {$natural: ASCENDING} as it's the default.
            if not ordering:
                self.ordering.append(('$natural', DESCENDING))
        else:
            for field, ascending in ordering:
                column = '_id' if field.primary_key else field.column
                direction = ASCENDING if ascending else DESCENDING
                self.ordering.append((column, direction))

    @safe_call
    def delete(self):
        options = self.connection.operation_flags.get('delete', {})
        self.collection.remove(self.mongo_query, **options)

    def get_cursor(self):
        if self.query.low_mark == self.query.high_mark:
            return []

        fields = get_selected_fields(self.query)
        if self.collection.collection.name != "django_session" and hasattr(self,"__schema_filter__"):
            pass

            # if self.collection.collection.name.split('.').__len__()>1:
            #     collection_name=self.collection.collection.name.split('.')[1]
            # else:
            #     collection_name = self.collection.collection.name
            # if self.__schema_filter__ !="":
            #     self.collection=self.collection.collection.database.get_collection(self.__schema_filter__+"."+collection_name)
            # else:
            #     self.collection = self.collection.collection.database.get_collection(
            #         self.schema + "." + collection_name)
        else:
            self.collection = self.collection.collection.database.get_collection("django_session")
        print("Exec query on {0} with filter {1}".format(self.collection.collection.name,self.mongo_query.__str__()))
        cursor = self.collection.find(self.mongo_query, fields)
        if self.ordering:
            cursor.sort(self.ordering)
        if self.query.low_mark > 0:
            cursor.skip(self.query.low_mark)
        if self.query.high_mark is not None:
            cursor.limit(int(self.query.high_mark - self.query.low_mark))
        return cursor

    def add_filters(self, filters, query=None):
        children = self._get_children(filters.children)

        if query is None:
            query = self.mongo_query

        if filters.connector == OR:
            assert '$or' not in query, "Multiple ORs are not supported."
            or_conditions = query['$or'] = []

        if filters.negated:
            self._negated = not self._negated

        for child in children:
            if filters.connector == OR:
                subquery = {}
            else:
                subquery = query

            if isinstance(child, Node):
                if filters.connector == OR and child.connector == OR:
                    if len(child.children) > 1:
                        raise DatabaseError("Nested ORs are not supported.")

                if filters.connector == OR and filters.negated:
                    raise NotImplementedError("Negated ORs are not supported.")

                self.add_filters(child, query=subquery)

                if filters.connector == OR and subquery:
                    or_conditions.extend(subquery.pop('$or', []))
                    if subquery:
                        or_conditions.append(subquery)

                continue

            field, lookup_type, value = self._decode_child(child)

            if lookup_type in ('month', 'day'):
                raise DatabaseError("MongoDB does not support month/day "
                                    "queries.")
            if self._negated and lookup_type == 'range':
                raise DatabaseError("Negated range lookups are not "
                                    "supported.")

            if field.primary_key:
                column = '_id'
            else:
                column = field.column

            existing = subquery.get(column)

            if isinstance(value, A):
                column, value = value.as_q(field)

            if self._negated and lookup_type in NEGATED_OPERATORS_MAP:
                op_func = NEGATED_OPERATORS_MAP[lookup_type]
                already_negated = True
            else:
                op_func = OPERATORS_MAP[lookup_type]
                if self._negated:
                    already_negated = False

            lookup = op_func(value)

            if existing is None:
                if self._negated and not already_negated:
                    lookup = {'$not': lookup}
                subquery[column] = lookup
                if filters.connector == OR and subquery:
                    or_conditions.append(subquery)
                continue

            if not isinstance(existing, dict):
                if not self._negated:
                    # {'a': o1} + {'a': o2} --> {'a': {'$all': [o1, o2]}}
                    assert not isinstance(lookup, dict)
                    subquery[column] = {'$all': [existing, lookup]}
                else:
                    # {'a': o1} + {'a': {'$not': o2}} -->
                    #     {'a': {'$all': [o1], '$nin': [o2]}}
                    if already_negated:
                        assert lookup.keys() == ['$ne']
                        lookup = lookup['$ne']
                    assert not isinstance(lookup, dict)
                    subquery[column] = {'$all': [existing], '$nin': [lookup]}
            else:
                not_ = existing.pop('$not', None)
                if not_:
                    assert not existing
                    if isinstance(lookup, dict):
                        assert lookup.keys() == ['$ne']
                        lookup = lookup.values()[0]
                    assert not isinstance(lookup, dict), (not_, lookup)
                    if self._negated:
                        # {'not': {'a': o1}} + {'a': {'not': o2}} -->
                        #     {'a': {'nin': [o1, o2]}}
                        subquery[column] = {'$nin': [not_, lookup]}
                    else:
                        # {'not': {'a': o1}} + {'a': o2} -->
                        #     {'a': {'nin': [o1], 'all': [o2]}}
                        subquery[column] = {'$nin': [not_], '$all': [lookup]}
                else:
                    if isinstance(lookup, dict):
                        if '$ne' in lookup:
                            if '$nin' in existing:
                                # {'$nin': [o1, o2]} + {'$ne': o3} -->
                                #     {'$nin': [o1, o2, o3]}
                                assert '$ne' not in existing
                                existing['$nin'].append(lookup['$ne'])
                            elif '$ne' in existing:
                                # {'$ne': o1} + {'$ne': o2} -->
                                #    {'$nin': [o1, o2]}
                                existing['$nin'] = [existing.pop('$ne'),
                                                    lookup['$ne']]
                            else:
                                existing.update(lookup)
                        else:
                            if '$in' in lookup and '$in' in existing:
                                # {'$in': o1} + {'$in': o2}
                                #    --> {'$in': o1 union o2}
                                existing['$in'] = list(
                                    set(lookup['$in'] + existing['$in']))
                            else:
                                # {'$gt': o1} + {'$lt': o2}
                                #    --> {'$gt': o1, '$lt': o2}
                                assert all(key not in existing
                                           for key in lookup.keys()), \
                                       [lookup, existing]
                                existing.update(lookup)
                    else:
                        key = '$nin' if self._negated else '$all'
                        existing.setdefault(key, []).append(lookup)

                if filters.connector == OR and subquery:
                    or_conditions.append(subquery)

        if filters.negated:
            self._negated = not self._negated


class SQLCompiler(NonrelCompiler):
    """
    Base class for all Mongo compilers.
    """
    query_class = MongoQuery

    def get_collection(self,schema):
        """
        get collection with schema
        :param schema:
        :return:
        """
        if self.query.get_meta().db_table == "auth_user":
            print ("prepare query for {0} with schema {1}".format("auth_user",schema))
        if self.query.get_meta().db_table=="django_session":
            schema="sys"
            print ("prepare query for {0}  with schema '{1}".format("django_session",schema))
            return self.connection.get_collection("django_session")
        if schema == None:  # add schema
            import inspect
            fx = inspect.stack()
            error_detail = ""
            for x in fx:
                error_detail += "\n\t {0}, line {1}".format(fx[1], fx[2])
            raise (
                Exception(
                    "can not call ''{1}'' without schema in '{0}'.\nDetail:\n{2}".format(
                        __file__, "SQLCompiler.get_collection",
                        error_detail
                    )))
        coll_name=""
        if schema=="" or schema==None:
            coll_name=self.query.get_meta().db_table
        else:
            coll_name = schema+"."+self.query.get_meta().db_table
        print ("prepare query for {0}".format(coll_name))
        return self.connection.get_collection(coll_name)


    def execute_sql(self, result_type=MULTI,schema = None):
        """
        Handles aggregate/count queries.
        """
        if schema == None:
            schema = self.schema
        if schema == None:  # add schema
            import inspect
            fx = inspect.stack()
            error_detail = ""
            for x in fx:
                error_detail += "\n\t {0}, line {1}".format(fx[1], fx[2])
            raise (
                Exception(
                    "can not call ''{1}'' without schema in '{0}'.\nDetail:\n{2}".format(
                        __file__, "insert_query",
                        error_detail
                    )))
        collection = self.get_collection(schema=schema)
        aggregations = self.query.aggregate_select.items()

        if len(aggregations) == 1 and isinstance(aggregations[0][1],
                                                 sqlaggregates.Count):
            # Ne need for full-featured aggregation processing if we
            # only want to count().
            if result_type is MULTI:
                return [[self.get_count(schema = schema)]]
            else:
                return [self.get_count(schema = schema)]

        counts, reduce, finalize, order, initial = [], [], [], [], {}
        try:
            query = self.build_query()
        except EmptyResultSet:
            return []

        for alias, aggregate in aggregations:
            assert isinstance(aggregate, sqlaggregates.Aggregate)
            if isinstance(aggregate, sqlaggregates.Count):
                order.append(None)
                # Needed to keep the iteration order which is important
                # in the returned value.
                # XXX: This actually does a separate query... performance?
                counts.append(self.get_count())
                continue

            aggregate_class = get_aggregation_class_by_name(
                aggregate.__class__.__name__)
            lookup = aggregate.col
            if isinstance(lookup, tuple):
                # lookup is a (table_name, column_name) tuple.
                # Get rid of the table name as aggregations can't span
                # multiple tables anyway.
                if lookup[0] != collection.name:
                    raise DatabaseError("Aggregations can not span multiple "
                                        "tables (tried %r and %r)." %
                                        (lookup[0], collection.name))
                lookup = lookup[1]
            self.query.aggregates[alias] = aggregate = aggregate_class(
                alias, lookup, aggregate.source)
            order.append(alias) # Just to keep the right order.
            initial.update(aggregate.initial())
            reduce.append(aggregate.reduce())
            finalize.append(aggregate.finalize())

        reduce = 'function(doc, out){ %s }' % '; '.join(reduce)
        finalize = 'function(out){ %s }' % '; '.join(finalize)
        cursor = collection.group(None, query.mongo_query, initial, reduce,
                                  finalize)

        ret = []
        for alias in order:
            result = cursor[0][alias] if alias else counts.pop(0)
            if result_type is MULTI:
                result = [result]
            ret.append(result)
        return ret


class SQLInsertCompiler(NonrelInsertCompiler, SQLCompiler):

    @safe_call
    def insert(self, docs, return_id=False,schema=None):
        """
        Stores a document using field columns as element names, except
        for the primary key field for which "_id" is used.

        If just a {pk_field: None} mapping is given a new empty
        document is created, otherwise value for a primary key may not
        be None.
        """
        if schema == None:  # add schema
            import inspect
            fx = inspect.stack()
            error_detail = ""
            for x in fx:
                error_detail += "\n\t {0}, line {1}".format(fx[1], fx[2])
            raise (
                Exception(
                    "can not call ''{1}'' without schema in '{0}'.\nDetail:\n{2}".format(
                        __file__, "SQLInsertCompiler.insert",
                        error_detail
                    )))
        for doc in docs:
            try:
                doc['_id'] = doc.pop(self.query.get_meta().pk.column)
                if self.query.get_meta().model_name == "session":


                    import threading
                    ct=threading.currentThread()
                    if hasattr(ct,"__current_schema__"):
                        doc["schema"]=ct.__current_schema__
                    else:
                        doc["schema"] = schema
            except KeyError:
                pass
            if doc.get('_id', NOT_PROVIDED) is None:
                if len(doc) == 1:
                    # insert with empty model
                    doc.clear()
                else:
                    raise DatabaseError("Can't save entity with _id set to None")

        collection = self.get_collection(schema)
        options = self.connection.operation_flags.get('save', {})
        if collection.collection.name == "django_session":
            import threading
            ct=threading.currentThread()
            if hasattr(ct,"DEFAULT_DB_SCHEMA"):
                doc["schema"] = ct.DEFAULT_DB_SCHEMA
            else:
                if hasattr(ct,"tenancy_code"):
                    doc["schema"]=ct.tenancy_code
                else:
                    from django.conf import settings
                    doc["schema"] = settings.MULTI_TENANCY_DEFAULT_SCHEMA

        if return_id:


            return collection.save(doc, **options)
        else:
            collection.save(doc, **options)


# TODO: Define a common nonrel API for updates and add it to the nonrel
#       backend base classes and port this code to that API.
class SQLUpdateCompiler(NonrelUpdateCompiler, SQLCompiler):
    query_class = MongoQuery

    def update(self, values):
        multi = True
        spec = {}
        for field, value in values:
            if field.primary_key:
                raise DatabaseError("Can not modify _id.")
            if getattr(field, 'forbids_updates', False):
                raise DatabaseError("Updates on %ss are not allowed." %
                                    field.__class__.__name__)
            if hasattr(value, 'evaluate'):
                # .update(foo=F('foo') + 42) --> {'$inc': {'foo': 42}}
                lhs, rhs = value.children
                assert (value.connector in (value.ADD, value.SUB) and
                        not value.negated and
                        isinstance(lhs, F) and not isinstance(rhs, F) and
                        lhs.name == field.name)
                if value.connector == value.SUB:
                    rhs = -rhs
                action = '$inc'
                value = rhs
            else:
                # .update(foo=123) --> {'$set': {'foo': 123}}
                action = '$set'
            spec.setdefault(action, {})[field.column] = value

            if field.unique:
                multi = False

        return self.execute_update(spec, multi)

    @safe_call
    def execute_update(self, update_spec, multi=True, **kwargs):
        collection = self.get_collection()
        try:
            criteria = self.build_query().mongo_query
        except EmptyResultSet:
            return 0
        options = self.connection.operation_flags.get('update', {})
        options = dict(options, **kwargs)
        info = collection.update(criteria, update_spec, multi=multi, **options)
        if info is not None:
            return info.get('n')


class SQLDeleteCompiler(NonrelDeleteCompiler, SQLCompiler):
    pass
