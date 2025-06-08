@echo off
title 🔁 Starting Hadoop + ZooKeeper + HBase

:: Prevent system from sleeping (while plugged in)
powercfg /change standby-timeout-ac 0

echo 🔄 Killing old Java processes (if any)...
taskkill /F /IM java.exe >nul 2>&1

:: --- Start Hadoop ---
echo 🚀 Starting Hadoop...
start cmd /k "title 🟢 Hadoop & cd C:\hadoop\sbin && start-all.cmd"

:: --- Start ZooKeeper ---
echo 🚀 Starting ZooKeeper...
start cmd /k "title 🟢 ZooKeeper & cd C:\zookeeper\bin && zkServer.cmd"

:: --- Start HBase Master ---
echo 🚀 Starting HBase Master...
start cmd /k "title 🟢 HBase Master & cd C:\hbase\bin && hbase master start"

:: --- Start HBase RegionServer ---
echo 🚀 Starting HBase RegionServer...
start cmd /k "title 🟢 HBase RegionServer & cd C:\hbase\bin && hbase regionserver start"

:: --- Start HBase Thrift Server ---
echo 🚀 Starting HBase Thrift Server...
start cmd /k "title 🟢 HBase Thrift & cd C:\hbase\bin && hbase thrift start"

:: --- Open HBase Shell ---
echo 💻 Opening HBase Shell...
start cmd /k "title 🟢 HBase Shell & cd C:\hbase\bin && hbase shell"

echo ✅ All services started in separate windows.
echo 🔒 This window prevents PC from sleeping. Don’t close it!
pause >nul
