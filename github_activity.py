import sys
import urllib.request
import json

def main():
    if len(sys.argv) != 2:
        print("Uso: github-activity <username>")
        sys.exit(1)

    username = sys.argv[1]
    url = f"https://api.github.com/users/{username}/events"

    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                print(f"Error: No se pudo obtener la actividad (código {response.status})")
                return

            data = json.loads(response.read().decode())

            if not data:
                print("No hay actividad reciente.")
                return

            print(f"Actividad reciente de @{username}:\n")

            for event in data[:10]:  # Limita a 10 eventos recientes
                print(parse_event(event))

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("Error: Usuario no encontrado.")
        else:
            print(f"Error HTTP: {e.code}")
    except urllib.error.URLError as e:
        print(f"Error de conexión: {e.reason}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def parse_event(event):
    type = event["type"]
    repo = event["repo"]["name"]

    if type == "PushEvent":
        count = len(event["payload"]["commits"])
        return f"- Pushed {count} commits to {repo}"
    elif type == "IssuesEvent":
        action = event["payload"]["action"]
        return f"- {action.capitalize()} an issue in {repo}"
    elif type == "WatchEvent":
        return f"- Starred {repo}"
    elif type == "ForkEvent":
        return f"- Forked {repo}"
    else:
        return f"- {type} in {repo}"

if __name__ == "__main__":
    main()
