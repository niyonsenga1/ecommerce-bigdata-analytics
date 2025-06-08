@echo off
echo 🛑 Stopping HBase, ZooKeeper, Hadoop...
taskkill /F /IM java.exe >nul 2>&1
echo ✅ All Java-based services stopped.
powercfg /change standby-timeout-ac 30
pause
