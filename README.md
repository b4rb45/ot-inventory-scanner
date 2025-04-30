![banner](OT_b4rb45.png)
<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.8%2B-blue.svg"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-green.svg"></a>
  <img src="https://img.shields.io/badge/status-stable-brightgreen.svg">
  <img src="https://img.shields.io/badge/OT%20Ready-Yes-blueviolet">
</p>
# OT Inventory Scanner — b4rb45 edition

🔥 Offensive OT/ICS Recon Tool built for serious SCADA mapping 🔥  
Scan & fingerprint industrial control system devices over TCP/UDP (Modbus, BACnet, DNP3, S7Comm, EtherNet/IP, and more).

## Features

- 🧠 Detects real industrial protocols: Modbus, OPC UA, DNP3, BACnet/IP, S7Comm, EtherNet/IP, and more.
- 🔍 Extracts vendor information (Vendor ID mapping).
- 🧪 Marks likely honeypots based on response timing.
- ⚙️ Multithreaded with optional stealth mode (evade IDS/IPS).
- 📜 Loads ports and vendor IDs dynamically from `.txt` files.
- ✅ Supports both TCP and UDP protocols.

---

## Usage

```bash
git clone https://github.com/yourname/ot-inventory-scanner.git
cd ot-inventory-scanner
pip install -r requirements.txt
python3 scanner.py
```

---

## Files

- `scanner.py`: Main scanning engine
- `ot_ports_tcp.txt`: TCP OT protocol ports
- `ot_ports_udp.txt`: UDP OT protocol ports
- `vendor_ids.txt`: Manufacturer IDs for EtherNet/IP
- `requirements.txt`: Python dependencies
- `README.md`: This manual

---

## Add/Extend Protocols or Vendors

- Add new ports in `ot_ports_tcp.txt` or `ot_ports_udp.txt`
- Add Vendor IDs in `vendor_ids.txt`
- Format: `<id>,<name>`

---

## License

MIT License — Free to use and contribute.
