```bash
import sys
import os

# Ruta al activate_this.py dentro del entorno virtual
activate_this = '/home/ubuntu/.local/share/virtualenvs/webApp-c1qRIGue/bin/activate_this.py'

# Ejecuta activate_this.py para activar el entorno virtual
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Agrega la ruta de tu proyecto al sistema
project_dir = '/var/www/webApp'
if project_dir not in sys.path:
    sys.path.append(project_dir)

# Verifica si el entorno virtual se ha activado
if hasattr(sys, 'real_prefix'):
    print("El entorno virtual se ha activado correctamente.")
else:
    print("¡Advertencia! El entorno virtual no parece estar activado.")

# Importa tu aplicación Flask después de activar el entorno virtual
from app import app as application


```