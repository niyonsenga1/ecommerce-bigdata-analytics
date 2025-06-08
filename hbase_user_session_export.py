import happybase
import csv

# 🔌 Connect to HBase
connection = happybase.Connection('localhost')
table = connection.table('user_sessions')

# 🧑 Target user
user_id = 'user_000042'

# 📦 For storing all session rows
all_sessions = []
total_sessions = 0
total_duration = 0

print(f"🔍 Scanning sessions for user: {user_id}...\n")

# 🔁 Scan all sessions by user_id prefix (must be bytes!)
for key, data in table.scan(row_prefix=f"{user_id}_".encode()):
    row_key = key.decode()
    session_data = {k.decode(): v.decode() for k, v in data.items()}

    # 🧮 Count + aggregate duration
    total_sessions += 1
    duration_str = session_data.get('info:duration', '0')
    try:
        duration = int(duration_str)
    except (ValueError, TypeError):
        duration = 0
    total_duration += duration

    # Add row_key to data for tracking
    session_data['row_key'] = row_key
    all_sessions.append(session_data)

# ------------------------------------------
# ✅ Export 1: Full sessions for this user
csv_file_1 = "hbase_user_sessions.csv"
with open(csv_file_1, mode='w', newline='', encoding='utf-8') as f:
    if all_sessions:
        writer = csv.DictWriter(f, fieldnames=sorted(all_sessions[0].keys()))
        writer.writeheader()
        writer.writerows(all_sessions)
    else:
        f.write("No sessions found.")

print(f"✅ Exported all session data to: {csv_file_1}")

# ------------------------------------------
# ✅ Export 2: Summary (Total Sessions + Duration)
csv_file_2 = "hbase_user_summary.csv"
with open(csv_file_2, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["user_id", "total_sessions", "total_duration_seconds"])
    writer.writerow([user_id, total_sessions, total_duration])

print(f"✅ Exported session summary to: {csv_file_2}")

# ✅ Done
print("\n🎉 HBase session export complete.")
