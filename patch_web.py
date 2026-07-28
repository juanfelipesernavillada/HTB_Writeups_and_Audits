import re

with open("HackTheBox/Linux/Easy/Cap/README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Buscamos la sección inicial de la Phase 2
old_pattern = r"### Phase 2: Exploitation \(IDOR \& PCAP\)\n- \*\*IDOR Discovery:\*\*"

new_text = """### Phase 2: Exploitation & Insecure Direct Object References (IDOR)

#### Web Application Enumeration
Navigating to the operational HTTP service on port 80 (`http://10.129.68.112`) grants unauthenticated access to a customized administrative panel titled *"Security Dashboard"*. To systematically map the web application's infrastructure and components, passive fingerprinting was performed using the *Wappalyzer* extension.

![Web Application Passive Fingerprinting](./assets/Web_Dashboard.png)

*Figure 6: Administrative web interface analysis and technology stack detection via Wappalyzer.*

The technological analysis confirmed that the platform backend is powered by **Python**, running on top of a **Gunicorn** web server. The dashboard provides statistical visualizations tracking network metrics, port scans, and failed login events, explicitly operating under the active session profile of a local user named **Nathan**.

#### IDOR Discovery"""

updated_content = re.sub(old_pattern, new_text, content)

with open("HackTheBox/Linux/Easy/Cap/README.md", "w", encoding="utf-8") as f:
    f.write(updated_content)
