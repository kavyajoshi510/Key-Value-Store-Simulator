import json
import time
import threading

class KeyValueStore:
    def __init__(self, consistency='strong', ttl=None):
        # You can set strong or eventual consistency
        # ttl means keys expire after given seconds (optional)
        self.store = {}
        self.consistency = consistency
        self.ttl = ttl
        self.lock = threading.Lock()
        self.walFile = 'wal.log'

        self.loadFromDisk()
        self.replayWal()

    def put(self, key, value):
        with self.lock:
            version = self.store[key]['version'] + 1 if key in self.store else 1
            timestamp = time.time()
            expiry = timestamp + self.ttl if self.ttl else None

            self.store[key] = {
                'value': value,
                'version': version,
                'timestamp': timestamp,
                'expiry': expiry
            }

            # Save to WAL (write-ahead log)
            with open(self.walFile, 'a') as f:
                logEntry = json.dumps({
                    'op': 'put',
                    'key': key,
                    'value': value,
                    'version': version,
                    'timestamp': timestamp,
                    'expiry': expiry
                })
                f.write(logEntry + '\n')

            self.saveToDisk()

    def get(self, key):
        with self.lock:
            if key not in self.store:
                return None

            # Remove if expired
            if self.store[key]['expiry'] and time.time() > self.store[key]['expiry']:
                del self.store[key]
                self.saveToDisk()
                return None

            if self.consistency == 'eventual':
                time.sleep(0.5)  # simulate delay for eventual consistency

            return self.store[key]['value']

    def delete(self, key):
        with self.lock:
            if key in self.store:
                del self.store[key]
                with open(self.walFile, 'a') as f:
                    logEntry = json.dumps({'op': 'delete', 'key': key})
                    f.write(logEntry + '\n')
                self.saveToDisk()

    def resolveConflict(self, key, newValue, newVersion, newTimestamp):
        # Last write wins
        if key not in self.store:
            self.store[key] = {
                'value': newValue,
                'version': newVersion,
                'timestamp': newTimestamp,
                'expiry': None
            }
            return

        existing = self.store[key]
        if newTimestamp > existing['timestamp']:
            self.store[key] = {
                'value': newValue,
                'version': newVersion,
                'timestamp': newTimestamp,
                'expiry': existing.get('expiry')
            }

        self.saveToDisk()

    def saveToDisk(self):
        with open('store_data.json', 'w') as f:
            json.dump(self.store, f, indent=2)

    def loadFromDisk(self):
        try:
            with open('store_data.json', 'r') as f:
                self.store = json.load(f)
        except FileNotFoundError:
            self.store = {}

    def replayWal(self):
        try:
            with open(self.walFile, 'r') as f:
                for line in f:
                    entry = json.loads(line.strip())
                    if entry['op'] == 'put':
                        self.store[entry['key']] = {
                            'value': entry['value'],
                            'version': entry['version'],
                            'timestamp': entry['timestamp'],
                            'expiry': entry.get('expiry')
                        }
                    elif entry['op'] == 'delete' and entry['key'] in self.store:
                        del self.store[entry['key']]
        except FileNotFoundError:
            pass
