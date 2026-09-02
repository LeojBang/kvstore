import grpc
from . import kvstore_pb2, kvstore_pb2_grpc



class KeyValueStoreServicer(kvstore_pb2_grpc.KeyValueStoreServicer):

    def __init__(self, store):
        self.store = store

    def Get(self, request, context):
        value = self.store.get(request.key)
        if value is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "key not found")
        return kvstore_pb2.GetResponse(value=value)

    def Put(self, request, context):
        self.store.put(request.key, request.value, request.ttl_seconds)
        return kvstore_pb2.PutResponse()

    def Delete(self, request, context):
        self.store.delete(request.key)
        return kvstore_pb2.DeleteResponse()

    def List(self, request, context):
        pairs = self.store.list(request.prefix)

        items = [
            kvstore_pb2.KeyValue(key=k, value=v)
            for k, v in pairs
        ]

        return kvstore_pb2.ListResponse(items=items)

