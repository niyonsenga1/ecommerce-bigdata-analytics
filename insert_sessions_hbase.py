import happybase
import json
import os
from tqdm import tqdm

# Configuration
HBASE_HOST = 'localhost'
TABLE_NAME = 'user_sessions'
SESSION_DIR = '.'  # where JSON files are

print("🔌 Connecting to HBase...")
connection = happybase.Connection(HBASE_HOST)
connection.open()
table = connection.table(TABLE_NAME)
print(f"✅ Connected to table: {TABLE_NAME}\n")

session_files = sorted([f for f in os.listdir(SESSION_DIR) if f.startswith('sessions_') and f.endswith('.json')])
print(f"📂 Found {len(session_files)} session files\n")

TOTAL_INSERTED = 0
SKIPPED = 0

for filename in tqdm(session_files, desc="📥 Inserting Sessions", unit="file"):
    filepath = os.path.join(SESSION_DIR, filename)
    with open(filepath, 'r') as f:
        sessions = json.load(f)

    batch = table.batch(batch_size=1000)

    for session in sessions:
        try:
            row_key = f"{session['user_id']}_{session['start_time']}_{session['session_id']}"
            batch.put(row_key, {
                b'info:session_id': session['session_id'].encode(),
                b'info:user_id': session['user_id'].encode(),
                b'info:start_time': session['start_time'].encode(),
                b'info:end_time': session['end_time'].encode(),
                b'info:duration': str(session['duration_seconds']).encode(),
                b'info:conversion': session['conversion_status'].encode(),
                b'info:referrer': session.get('referrer', 'unknown').encode(),
                b'info:viewed_products': json.dumps(session.get('viewed_products', [])).encode(),
                b'info:cart_contents': json.dumps(session.get('cart_contents', {})).encode(),

                b'geo:city': session['geo_data']['city'].encode(),
                b'geo:state': session['geo_data']['state'].encode(),
                b'geo:country': session['geo_data']['country'].encode(),
                b'geo:ip_address': session['geo_data']['ip_address'].encode(),

                b'device:type': session['device_profile']['type'].encode(),
                b'device:os': session['device_profile']['os'].encode(),
                b'device:browser': session['device_profile']['browser'].encode()
            })
            TOTAL_INSERTED += 1
        except Exception as e:
            print(f"[⚠️] Skipped session in {filename}: {e}")
            SKIPPED += 1

    batch.send()
    print(f"✅ Processed {len(sessions)} in {filename}")

print(f"\n🎉 FINISHED\n✅ Inserted: {TOTAL_INSERTED:,}\n⚠️ Skipped: {SKIPPED:,}")
