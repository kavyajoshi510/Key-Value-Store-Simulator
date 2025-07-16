import streamlit as st
import time
from key_value_store import KeyValueStore

st.title("Key-Value Store Simulator")

# Sidebar option to choose consistency
consistency_mode = st.sidebar.selectbox("Choose Consistency", ["Strong", "Eventual"])

# Slider for eventual consistency delay
if consistency_mode == "eventual":
    delay_seconds = st.sidebar.slider("Eventual Consistency Delay (seconds)", min_value=0, max_value=5, value=1)
else:
    delay_seconds = 0  # No delay for strong consistency

# Checkbox to enable or disable TTL
useTTL = st.checkbox("Enable TTL (10 seconds)", value=True)

# Initialize session state if not already set
if 'consistency' not in st.session_state:
    st.session_state['consistency'] = "strong"
if 'delay_seconds' not in st.session_state:
    st.session_state['delay_seconds'] = 0

# Create or reset store if consistency, TTL, or delay changes
if ('kvStore' not in st.session_state 
    or st.session_state['ttlEnabled'] != useTTL 
    or st.session_state['consistency'] != consistency_mode
    or st.session_state['delay_seconds'] != delay_seconds):

    ttlValue = 10 if useTTL else None
    st.session_state['kvStore'] = KeyValueStore(consistency=consistency_mode, ttl=ttlValue, delay_seconds=delay_seconds)
    st.session_state['ttlEnabled'] = useTTL
    st.session_state['consistency'] = consistency_mode
    st.session_state['delay_seconds'] = delay_seconds

kvStore = st.session_state['kvStore']

#Put section 
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

#Get section 
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

#Delete section
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

#Store display 
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

