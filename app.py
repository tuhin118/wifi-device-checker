from flask import Flask, render_template, jsonify
import subprocess
import re

app = Flask(__name__)


def scan_devices():
    devices = []

    try:
        result = subprocess.check_output(
            ["ip", "neigh"],
            text=True,
            stderr=subprocess.DEVNULL
        )

        for line in result.splitlines():
            match = re.search(
                r"(\d+\.\d+\.\d+\.\d+).*?lladdr\s+([0-9a-fA-F:]{17})",
                line
            )

            if match:
                ip = match.group(1)
                mac = match.group(2)

                devices.append({
                    "ip": ip,
                    "mac": mac,
                    "hostname": "Unknown",
                    "manufacturer": "Unknown"
                })

    except Exception as e:
        print("Scan error:", e)

    return devices


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/devices")
def devices():
    return jsonify(scan_devices())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
