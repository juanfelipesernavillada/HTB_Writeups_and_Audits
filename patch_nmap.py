import re

with open("HackTheBox/Linux/Easy/Cap/README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Buscamos la línea de Service Detection y la reemplazamos con el bloque técnico estructurado
old_pattern = r"\* \*\*Service Detection:\*\* vsftpd 3\.0\.3, OpenSSH 8\.2p1, Gunicorn \(Python web app\)\."

new_text = """### Service Version & Script Enumeration

Following the initial discovery, a targeted service enumeration scan (`-sCV`) was conducted specifically on the open ports (21, 22, and 80). This assessment aims to determine software versioning, identifying potential vulnerabilities or misconfigurations, and validating underlying operating system details. The findings were exported in an Nmap format (`-oN targeted`) for internal audit review.

![Nmap Targeted Service Enumeration Scan](./assets/Segundo_Nmap.png)

*Figure 5: Targeted service version scanning and script execution details.*

The aggressive enumeration script provided definitive context regarding the target's attack surface:
* **Port 21 (FTP):** Running `vsftpd 3.0.3`.
* **Port 22 (SSH):** Running `OpenSSH 8.2p1` hosted on an Ubuntu Linux distribution.
* **Port 80 (HTTP):** Running a Python-based web server application managed by `Gunicorn`, explicitly exposing a web panel titled *"Security Dashboard"*."""

updated_content = re.sub(old_pattern, new_text, content)

with open("HackTheBox/Linux/Easy/Cap/README.md", "w", encoding="utf-8") as f:
    f.write(updated_content)
