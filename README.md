# Neue_Datenbankkonzepte

Der zu beachtende branch ist main

Als erstes muss Redis installiert werden. Dies geschieht auf Windows mit WSL.

Öffnen Sie dazu die PowerShell als Administrator und führen Sie folgenden Befehl aus: 

wsl --install

Das installiert WSL zusammen mit Ubuntu als Standarddistribution. Danach muss der PC neu gestartet werden.
Gegebenenfalls muss im BIOS die CPU Virtualisierung aktiviert werden.
Dies kann auch in folgender Dokumentation nachgelesen werden: https://learn.microsoft.com/en-us/windows/wsl/install

Öffnen Sie dann Ubuntu und erstellen Sie Benutzernamen und Passwort.
Danach können Sie Redis in Ubuntu installieren:

curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis

Dies kann auch in der Redis Dokumentation unter https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-windows/  nachgelesen werden.
Danach den Redis Server starten:

sudo service redis-server start

Danach kann die Verbindung zum Redis Server hergestellt werden:

redis-cli

Mit "ping" kann die Verbindung getestet werden, bei erfolgreicher Verbindung erscheint "PONG".

Danach können sie den Code starten. Je nach Entwicklungsumgebung und vorinstallierten Paketen muss dafür ein Redis Modul installiert werden,
auf Visual Studio Code beispielsweise geben Sie dafür: 
pip install redis 
im Terminal ein. Der Code ist in Python geschrieben, deshalb wird zudem eine Python Extension benötigt.

Nach erfolgreichem Starten des Programmes können dann die unterschiedlichen Funktionen über die Konsole aufgerufen werden. Mit Auswahl der Nutzerrolle "Admin" kann zudem eine Turniersimulation gestartet werden.
