from key_value_store import KeyValueStore
import time

if __name__ == "__main__":
    # onsistency mode or TTL can be changed here if needed
    kvStore = KeyValueStore(consistency='strong', ttl=10)

    while True:
        print("\nAvailable commands:")
        print("1 -> Put key-value")
        print("2 -> Get value by key")
        print("3 -> Delete key")
        print("4 -> Exit")
        print("5 -> Simulate conflict resolution")

        cmd = input("Enter command number: ")

        if cmd == '1':
            key = input("Enter key: ")
            value = input("Enter value: ")
            kvStore.put(key, value)
            print(f"Stored ({key}, {value}).")

        elif cmd == '2':
            key = input("Enter key to get: ")
            value = kvStore.get(key)
            if value is None:
                print("Key not found or expired.")
            else:
                print(f"Value: {value}")

        elif cmd == '3':
            key = input("Enter key to delete: ")
            kvStore.delete(key)
            print(f"Deleted key: {key}")

        elif cmd == '4':
            print("Bye!")
            break

        elif cmd == '5':
            key = input("Enter key for conflict simulation: ")
            val1 = input("Enter first value: ")
            val2 = input("Enter second value: ")

            ts1 = time.time()
            ts2 = ts1 + 1  # simulate second write a bit later

            kvStore.resolveConflict(key, val1, 1, ts1)
            kvStore.resolveConflict(key, val2, 2, ts2)

            finalVal = kvStore.get(key)
            print(f"After conflict resolution, key '{key}' has value: {finalVal}")

        else:
            print("Invalid command. Please enter 1, 2, 3, 4, or 5.")
