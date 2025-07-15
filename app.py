import streamlit as st
import time
from key_value_store import KeyValueStore

st.title("Key-Value Store Simulator")

useTTL = st.checkbox("Enable TTL (10 seconds)", value=True)

# Create or reset store if TTL setting changes
if 'kvStore' not in st.session_state or st.session_state['ttlEnabled'] != useTTL:
    ttlValue = 10 if useTTL else None
    st.session_state['kvStore'] = KeyValueStore(consistency='strong', ttl=ttlValue)
    st.session_state['ttlEnabled'] = useTTL

kvStore = st.session_state['kvStore']

# --- Put section ---
st.header("Add or Update a Key")
with st.form("put_form"):
    putKey = st.text_input("Key (Put)")
    putValue = st.text_input("Value")
    putSubmitted = st.form_submit_button("Put")
    if putSubmitted:
        if putKey and putValue:
            kvStore.put(putKey, putValue)
            st.success(f"Stored ({putKey}, {putValue})")
        else:
            st.warning("Please enter both key and value.")

# --- Get section ---
st.header("Get a Value")
with st.form("get_form"):
    getKey = st.text_input("Key (Get)")
    getSubmitted = st.form_submit_button("Get")
    if getSubmitted:
        if getKey:
            value = kvStore.get(getKey)
            if value is None:
                st.error("Key not found or expired.")
            else:
                st.info(f"Value: {value}")
        else:
            st.warning("Please enter a key.")

# --- Delete section ---
st.header("Delete a Key")
with st.form("delete_form"):
    delKey = st.text_input("Key (Delete)")
    delSubmitted = st.form_submit_button("Delete")
    if delSubmitted:
        if delKey:
            kvStore.delete(delKey)
            st.success(f"Deleted key: {delKey}")
        else:
            st.warning("Please enter a key.")

# --- Store display ---
st.header("Current Store")

storeTable = []
for k, v in kvStore.store.items():
    expired = v['expiry'] and time.time() > v['expiry']
    if expired:
        continue
    storeTable.append({
        "Key": k,
        "Value": v['value'],
        "Version": v['version'],
        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(v['timestamp']))
    })

if storeTable:
    st.table(storeTable)
else:
    st.write("Store is empty or keys expired.")
