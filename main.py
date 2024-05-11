import apcParser
import testData
import subprocess
import time
from prometheus_client import start_http_server, Gauge

POLLING_INTERVAL_SECS = 60

# available metrics
apc_line_voltage = Gauge("apc_line_voltage", "Current AC Line voltage")
apc_battery_change_pct = Gauge("apc_battery_change_pct", "Battery change percent")
apc_load_pct = Gauge("apc_load_pct", "UPS load percent")


def updateMetrics():
    proc = subprocess.run("cmd /c dir", capture_output = True)
    apc = apcParser.parseUpsData(testData.testMessage) #proc.stdout
    print(f"UPS {apc.model} serial {apc.serial} is {apc.status}, line {apc.lineV} V, battery changed {apc.battPct}%, UPS load {apc.loadPct}%. Last start time is {apc.lastStartTime}")

    apc_line_voltage.set(apc.lineV)
    apc_load_pct.set(apc.loadPct)
    apc_battery_change_pct.set(apc.battPct)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(9099)
    print("Exporter running at http://localhost:9099")

    while True:
        updateMetrics()
        time.sleep(POLLING_INTERVAL_SECS)