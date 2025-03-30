import redis
import time
import random

# Verbindung zur Redis-Datenbank herstellen
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Redis-Key für das aktuelle Turnier
CURRENT_TOURNAMENT_KEY = "highscore:current"

# Hauptmenü des Programms
def main():
    while True:
        print("\nHauptmenü:")
        print("1 Nutzerrolle auswählen")
        print("2 Highscore-Liste anzeigen")
        print("3 Turnierstatus abrufen")
        print("4 Vergangene Turniere anzeigen")
        print("5 Programm beenden")

        choice = input("Wähle eine Option (1-5): ").strip()
        if choice == "1":
            select_user_role()
        elif choice == "2":
            try:
                get_top_players()
            except Exception as e:
                print(f"Fehler beim Abrufen der Highscore-Liste: {e}")
        elif choice == "3":
            try:
                status = r.get("tournament_status")
                print(f"Turnierstatus: {status}")
            except Exception as e:
                print(f"Fehler beim Abrufen des Turnierstatus: {e}")
        elif choice == "4":
            try:
                past_tournaments = list_past_tournaments()
                if past_tournaments:
                    date = input("Gib das Turnierdatum ein (YYYYMM): ").strip()
                    if not date.isdigit() or len(date) != 6:
                        print("Ungültiges Datum! Bitte im Format YYYYMM eingeben.")
                        continue
                    get_past_highscore(date)
            except Exception as e:
                print(f"Fehler beim Abrufen vergangener Turniere: {e}")
        elif choice == "5":
            print("Programm wird beendet.")
            break
        else:
            print("Ungültige Eingabe! Bitte eine Zahl zwischen 1 und 5 eingeben.")

# Auswahl der Nutzerrolle
def select_user_role():
    while True:
        print("\nWähle deine Rolle:")
        print("1 Spieler")
        print("2 Zuschauer")
        print("3 Administrator")

        role = input("Gib die Nummer deiner Rolle ein (1-3): ").strip()
        if role == "1":
            player_menu()
            break
        elif role == "2":
            spectator_menu()
            break
        elif role == "3":
            admin_menu()
            break
        else:
            print("Ungültige Eingabe! Bitte eine Zahl zwischen 1 und 3 eingeben.")

# Menü für Spieler
def player_menu():
    while True:
        print("\nSpieler-Menü:")
        print("1 Registrieren")
        print("2 Highscore setzen")
        print("3 Meine Platzierung anzeigen")
        print("4 Highscore-Liste anzeigen")
        print("5 Vergangene Turniere anzeigen")
        print("6 Beenden")

        choice = input("Wähle eine Option (1-6): ").strip()
        if choice == "1":
            name = input("Dein Name: ").strip()
            password = input("Passwort: ").strip()
            if not name or not password:
                print("Name und Passwort dürfen nicht leer sein!")
                continue
            try:
                register_player(name, password)
            except Exception as e:
                print(f"Fehler beim Registrieren des Spielers: {e}")
        elif choice == "2":
            name = input("Dein Name: ").strip()
            score = input("Punktzahl: ").strip()
            if not score.isdigit():
                print("Ungültige Punktzahl! Bitte eine Zahl eingeben.")
                continue
            try:
                add_score(name, int(score))
            except Exception as e:
                print(f"Fehler beim Setzen des Highscores: {e}")
        elif choice == "3":
            name = input("Dein Name: ").strip()
            try:
                get_player_rank(name)
            except Exception as e:
                print(f"Fehler beim Abrufen der Platzierung: {e}")
        elif choice == "4":
            try:
                get_top_players()
            except Exception as e:
                print(f"Fehler beim Abrufen der Highscore-Liste: {e}")
        elif choice == "5":
            try:
                list_past_tournaments()
            except Exception as e:
                print(f"Fehler beim Abrufen vergangener Turniere: {e}")
        elif choice == "6":
            print("Beende das Spieler-Menü.")
            break
        else:
            print("Ungültige Eingabe! Bitte eine Zahl zwischen 1 und 6 eingeben.")

# Menü für Zuschauer
def spectator_menu():
    while True:
        print("\nZuschauer-Menü:")
        print("1 Echtzeit-Rangliste anzeigen")
        print("2 Live-Updates abonnieren")
        print("3 Vergangene Turniere anzeigen")
        print("4 Spieler favorisieren")
        print("5 Beenden")

        choice = input("Wähle eine Option (1-5): ").strip()
        if choice == "1":
            try:
                get_top_players()
            except Exception as e:
                print(f"Fehler beim Abrufen der Highscore-Liste: {e}")
        elif choice == "2":
            print("Live-Updates aktiviert! Öffne ein zweites Terminal und tippe:")
            print("   redis-cli SUBSCRIBE highscore_updates")
        elif choice == "3":
            try:
                list_past_tournaments()
            except Exception as e:
                print(f"Fehler beim Abrufen vergangener Turniere: {e}")
        elif choice == "4":
            user_id = input("Deine Zuschauer-ID: ").strip()
            player_name = input("Favorisierter Spieler: ").strip()
            if not user_id or not player_name:
                print("Zuschauer-ID und Spielername dürfen nicht leer sein!")
                continue
            try:
                add_favorite(user_id, player_name)
            except Exception as e:
                print(f"Fehler beim Hinzufügen eines Favoriten: {e}")
        elif choice == "5":
            print("Beende das Zuschauer-Menü.")
            break
        else:
            print("Ungültige Eingabe! Bitte eine Zahl zwischen 1 und 5 eingeben.")

# Menü für Administratoren
def admin_menu():
    while True:
        print("\nAdministrator-Menü:")
        print("1 Turnier starten")
        print("2 Turnier beenden & archivieren")
        print("3 Betrüger entfernen")
        print("4 Highscore-Log anzeigen")
        print("5 Vergangene Turniere anzeigen")
        print("6 Turniersimulation starten")
        print("7 Beenden")

        choice = input("Wähle eine Option (1-7): ").strip()
        if choice == "1":
            try:
                start_tournament()
            except Exception as e:
                print(f"Fehler beim Starten des Turniers: {e}")
        elif choice == "2":
            try:
                end_tournament()
            except Exception as e:
                print(f"Fehler beim Beenden des Turniers: {e}")
        elif choice == "3":
            name = input("Betrügername: ").strip()
            if not name:
                print("Der Name des Betrügers darf nicht leer sein!")
                continue
            try:
                remove_cheater(name)
            except Exception as e:
                print(f"Fehler beim Entfernen eines Betrügers: {e}")
        elif choice == "4":
            show_highscore_log()
        elif choice == "5":
            try:
                list_past_tournaments()
            except Exception as e:
                print(f"Fehler beim Abrufen vergangener Turniere: {e}")
        elif choice == "6":
            try:
                num_players = int(input("Anzahl der Spieler: ").strip())
                num_spectators = int(input("Anzahl der Zuschauer: ").strip())
                num_admins = int(input("Anzahl der Administratoren: ").strip())
                max_score = int(input("Maximale Punktzahl: ").strip())
                simulate_tournament(num_players, num_spectators, num_admins, max_score)
            except ValueError:
                print("Ungültige Eingabe! Bitte nur Zahlen eingeben.")
            except Exception as e:
                print(f"Fehler bei der Turniersimulation: {e}")
        elif choice == "7":
            print("Beende das Admin-Menü.")
            break
        else:
            print("Ungültige Eingabe! Bitte eine Zahl zwischen 1 und 7 eingeben.")

def simulate_tournament(num_players, num_spectators, num_admins, max_score):
    # CRUD-Zeiten messen
    crud_times = {"create": [], "read": [], "update": [], "delete": []}

    # Verfügbarkeitsprüfung
    total_requests = 0
    successful_requests = 0

    # Turnier starten (UPDATE)
    total_requests += 1
    start_time = time.time()
    try:
        start_tournament()
        crud_times["update"].append((time.time() - start_time) * 1000)
        successful_requests += 1
    except Exception as e:
        print(f"Fehler beim Starten des Turniers: {e}")

    # Spieleraktionen simulieren
    registered_players = []
    for i in range(1, num_players + 1):
        player_name = f"Spieler{i}"
        password = "password"

        # Spieler registrieren (CREATE)
        total_requests += 1
        start_time = time.time()
        try:
            register_player(player_name, password)
            registered_players.append(player_name)
            crud_times["create"].append((time.time() - start_time) * 1000)
            successful_requests += 1
        except Exception as e:
            print(f"Fehler beim Registrieren von {player_name}: {e}")

        # Highscore setzen (UPDATE)
        total_requests += 1
        start_time = time.time()
        try:
            add_score(player_name, random.randint(1, max_score))
            crud_times["update"].append((time.time() - start_time) * 1000)
            successful_requests += 1
        except Exception as e:
            print(f"Fehler beim Setzen des Highscores für {player_name}: {e}")

        # Platzierung anzeigen (READ)
        total_requests += 1
        start_time = time.time()
        try:
            get_player_rank(player_name)
            crud_times["read"].append((time.time() - start_time) * 1000)
            successful_requests += 1
        except Exception as e:
            print(f"Fehler beim Abrufen der Platzierung für {player_name}: {e}")

        # Vergangene Turniere anzeigen (READ)
        total_requests += 1
        start_time = time.time()
        try:
            list_past_tournaments()
            crud_times["read"].append((time.time() - start_time) * 1000)
            successful_requests += 1
        except Exception as e:
            print(f"Fehler beim Abrufen vergangener Turniere: {e}")

    # Zuschaueraktionen simulieren
    for i in range(1, num_spectators + 1):
        user_id = f"Zuschauer{i}"
        player_name = random.choice(registered_players)  # Nur registrierte Spieler

        # Favoriten hinzufügen (CREATE)
        total_requests += 1
        start_time = time.time()
        try:
            add_favorite(user_id, player_name)
            crud_times["create"].append((time.time() - start_time) * 1000)
            successful_requests += 1
        except Exception as e:
            print(f"Fehler beim Hinzufügen eines Favoriten für {user_id}: {e}")

        # Highscore-Liste anzeigen (READ)
        total_requests += 1
        start_time = time.time()
        try:
            get_top_players()
            crud_times["read"].append((time.time() - start_time) * 1000)
            successful_requests += 1
        except Exception as e:
            print(f"Fehler beim Abrufen der Highscore-Liste: {e}")

        # Vergangene Turniere anzeigen (READ)
        total_requests += 1
        start_time = time.time()
        try:
            list_past_tournaments()
            crud_times["read"].append((time.time() - start_time) * 1000)
            successful_requests += 1
        except Exception as e:
            print(f"Fehler beim Abrufen vergangener Turniere: {e}")

    # Administratoraktionen simulieren
    for i in range(1, num_admins + 1):
        if random.choice([True, False]):
            player_name = random.choice(registered_players)  # Nur registrierte Spieler

            # Betrüger entfernen (DELETE)
            total_requests += 1
            start_time = time.time()
            try:
                remove_cheater(player_name)
                registered_players.remove(player_name)  # Spieler aus der Liste entfernen
                crud_times["delete"].append((time.time() - start_time) * 1000)
                successful_requests += 1
            except Exception as e:
                print(f"Fehler beim Entfernen von {player_name}: {e}")

        # Highscore-Log anzeigen (READ)
        total_requests += 1
        start_time = time.time()
        try:
            logs = r.lrange("highscore_log", 0, -1)
            crud_times["read"].append((time.time() - start_time) * 1000)
            successful_requests += 1
        except Exception as e:
            print(f"Fehler beim Abrufen des Highscore-Logs: {e}")

        # Vergangene Turniere anzeigen (READ)
        total_requests += 1
        start_time = time.time()
        try:
            list_past_tournaments()
            crud_times["read"].append((time.time() - start_time) * 1000)
            successful_requests += 1
        except Exception as e:
            print(f"Fehler beim Abrufen vergangener Turniere: {e}")

    # Turnier beenden (UPDATE)
    total_requests += 1
    start_time = time.time()
    try:
        end_tournament()
        crud_times["update"].append((time.time() - start_time) * 1000)
        successful_requests += 1
    except Exception as e:
        print(f"Fehler beim Beenden des Turniers: {e}")

    # Durchschnittszeiten berechnen
    print("\nDurchschnittszeiten für CRUD-Operationen (in ms):")
    for operation, times in crud_times.items():
        if times:
            avg_time = sum(times) / len(times)
            print(f"{operation.upper()}: {avg_time:.2f} ms")
        else:
            print(f"{operation.upper()}: Keine Operationen durchgeführt.")

    # Verfügbarkeit berechnen
    availability_percentage = (successful_requests / total_requests) * 100 if total_requests > 0 else 0
    print(f"\nSystemverfügbarkeit während des Turniers: {availability_percentage:.2f}%")

    print("Turniersimulation abgeschlossen.")

# Vergangene Turniere anzeigen
def list_past_tournaments():
    keys = r.keys("highscore:*")
    if not keys:
        print("Keine vergangenen Turniere gefunden!")
        return []

    keys.sort(reverse=True)
    print("\nVergangene Turniere:")
    for key in keys:
        print(f"- {key.replace('highscore:', '')}")
    return keys

def get_past_highscore(tournament_date):
    key = f"highscore:{tournament_date}"
    if not r.exists(key):
        print(f"Kein Turnier mit dem Datum {tournament_date} gefunden!")
        return

    past_scores = r.zrevrange(key, 0, -1, withscores=True)
    print(f"\nHighscore-Liste für Turnier {tournament_date}:")
    for rank, (player, score) in enumerate(past_scores, start=1):
        print(f"{rank}. {player}: {int(score)} Punkte")

# Spieler Registrierung
def register_player(player_name, password):
    r.hset(f"user:{player_name}", "password", password)
    print(f"Spieler {player_name} wurde registriert!")

# Turnier-Verwaltung
def start_tournament():
    r.set("tournament_status", "active")
    print("Turnier wurde gestartet!")

def end_tournament():
    r.set("tournament_status", "ended")
    print("Turnier wurde beendet!")
    archive_tournament()

def archive_tournament():
    timestamp = time.strftime("%Y%m")
    archive_key = f"highscore:{timestamp}"
    r.rename(CURRENT_TOURNAMENT_KEY, archive_key)
    print(f"Turnier wurde archiviert als {archive_key}.")
    r.delete(CURRENT_TOURNAMENT_KEY)

# aktuelle Highscore Liste
def get_top_players(limit=10):
    top_players = r.zrevrange(CURRENT_TOURNAMENT_KEY, 0, limit - 1, withscores=True)

    if not top_players:
        print("Keine Highscores verfügbar!")
        return

    print("\nHighscore-Rangliste:")
    for rank, (player, score) in enumerate(top_players, start=1):
        print(f"{rank}. {player}: {int(score)} Punkte")

# neuen Score hinzufügen
def add_score(player_name, score):
    if not r.hexists(f"user:{player_name}", "password"):
        print(f"Spieler {player_name} ist nicht registriert!")
        return

    r.zadd(CURRENT_TOURNAMENT_KEY, {player_name: score})
    log_highscore_change(player_name, score)
    notify_score_change(player_name)
    print(f"{player_name} hat {score} Punkte erzielt!")

# Platzierung eines Spielers anzeigen
def get_player_rank(player_name):
    rank = r.zrevrank(CURRENT_TOURNAMENT_KEY, player_name)

    if rank is not None:
        print(f"{player_name} ist aktuell auf Platz {rank + 1}.")
    else:
        print(f"{player_name} ist nicht in der Rangliste!")

# Zuschauer-Funktionen
def add_favorite(user_id, player_name):
    r.sadd(f"favoriten:{user_id}", player_name)
    print(f"Spieler {player_name} wurde zur Favoritenliste von {user_id} hinzugefügt!")

# Admin-Funktionen
# Spieler entfernen
def remove_cheater(player_name):
    if r.zrem(CURRENT_TOURNAMENT_KEY, player_name):
        print(f"{player_name} wurde aus der Rangliste entfernt!")
    else:
        print(f"{player_name} wurde nicht in der Rangliste gefunden!")

# Logging- und Benachrichtigungsfunktionen
# Speichert Highscore-Änderungen im Log
def log_highscore_change(player_name, score):
    r.rpush("highscore_log", f"{player_name} hat {score} Punkte erzielt")

# Sendet eine Nachricht, wenn ein Spieler überholt wurde
def notify_score_change(player_name):
    r.publish("highscore_updates", f"{player_name} wurde überholt!")

def calculate_highscore(scores):
    # Sicherstellen, alle Scores integer sind
    if not all(isinstance(score, int) for score in scores):
        raise ValueError("All scores must be integers")

    # Calculate the high score
    highscore = max(scores)
    return highscore

def show_highscore_log():
    try:
        logs = r.lrange("highscore_log", 0, -1)  # Alle Einträge im Highscore-Log abrufen
        if not logs:
            print("Das Highscore-Log ist leer.")
            return

        print("\nHighscore-Log:")
        for log in logs:
            print(log)
    except Exception as e:
        print(f"Fehler beim Abrufen des Highscore-Logs: {e}")

# Hauptprogramm starten
if __name__ == "__main__":
    main()