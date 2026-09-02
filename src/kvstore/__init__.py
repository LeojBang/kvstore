from concurrent.futures import ThreadPoolExecutor
import grpc
from . import kvstore_pb2_grpc
from .server import KeyValueStoreServicer
from .store import InMemoryStore


def main():
    store = InMemoryStore()
    servicer = KeyValueStoreServicer(store)

    # Пул потоков — чтобы обрабатывать запросы параллельно
    server = grpc.server(ThreadPoolExecutor(max_workers=10))

    # Привязать servicer к серверу
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(servicer, server)

    # Слушать порт 8000
    server.add_insecure_port("[::]:8000")
    server.start()

    print("Server on :8000")
    server.wait_for_termination()


if __name__ == "__main__":
    main()