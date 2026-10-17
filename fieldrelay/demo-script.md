# FieldRelay Demo Run Sheet

Target length: 2-3 minutes

## 1. Start the system

Run `docker compose up --build` and open `http://localhost:8500`. Keep `http://localhost:8000/v1/stats` open in another tab.

## 2. Show durable local capture

Add a record for site `SITE-01`, category `Supply update`, item `Drinking water`, status `Low`, quantity `4`, and note `Restock requested`. Point out that the queue count increases immediately.

## 3. Simulate a connection failure

Choose **Simulate offline**. Add a second record for `SITE-02` and a different item. The new record should remain pending. Press **Sync now** and show that the interface keeps it in the local queue while offline mode is active.

## 4. Restore the connection

Choose **Restore connection**, then **Sync now**. Show the pending count fall and synced count rise. Refresh the cloud statistics tab to show the new records in the cloud store.

## 5. Explain the safeguards

Show the test results using `PYTHONPATH=src python -m pytest -q`. Explain that a batch signature is verified before parsing, event hashes are checked before storage, the cloud acknowledges replays without inserting duplicates, and conflicting reuse of an event ID is rejected. The local benchmark tests 1,000 synthetic events and then replays them; describe it as a functional test-client benchmark, not production cloud performance.
