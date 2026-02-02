import time

def linear_search(transactions, search_id):
    for t in transactions:
        if t["id"] == search_id:
            return t
    return None

def dict_lookup(transactions_dict, search_id):
    return transactions_dict.get(search_id)

if __name__ == "__main__":
    from dsa.parse_sms import parse_sms

    txs = parse_sms()
    tx_dict = {t["id"]: t for t in txs}

    test_id = txs[0]["id"]  # pick first transaction for testing

    # Linear Search
    start = time.time()
    res1 = linear_search(txs, test_id)
    end = time.time()
    print(f"Linear search found: {res1['receiver']}, time: {end-start:.6f}s")

    # Dictionary Lookup
    start = time.time()
    res2 = dict_lookup(tx_dict, test_id)
    end = time.time()
    print(f"Dict lookup found: {res2['receiver']}, time: {end-start:.6f}s")
