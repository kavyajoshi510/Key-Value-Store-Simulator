# 🗄️ Key-Value Store Simulator

This project is a **simplified NoSQL key-value store** written in Python.  
It simulates core concepts used in distributed systems, including:

- Configurable **strong vs. eventual consistency**.
- Write-Ahead Logging (WAL) for durability.
- Disk-backed persistence.
- Time-to-Live (TTL) support for automatic key expiration.
- Conflict resolution logic using timestamps (last write wins).

---


## ⚙️ Features

✅ **Strong and eventual consistency**  
- You can choose if reads should always be up-to-date (strong) or allow a slight delay (eventual).

✅ **Versioned updates with timestamps**  
- Every key tracks its version and timestamp, similar to how real systems manage updates and conflicts.

✅ **Write-Ahead Logging (WAL)**  
- All updates and deletes are logged before being applied, helping simulate crash recovery.

✅ **Disk persistence**  
- Keys and their metadata are saved to disk (`store_data.json`) and can survive restarts.

✅ **TTL (Time-to-Live)**  
- Keys automatically expire if they live past the configured TTL.

✅ **Conflict resolution**  
- If two writes happen with different timestamps, "last write wins" logic resolves the conflict.

---

##  How to run (CLI)

```bash
python run_store.py
```

## How to run Streamlit

```bash
streamlit run app.py
```
