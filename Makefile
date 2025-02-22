PYTHON=python
VENV_DIR=env
ACTIVATE= . $(VENV_DIR)/Scripts/activate

.PHONY: set-permissions
set-permissions: # Setear permisos para ejecutar PowerShell como administrador.
	PowerShell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force"

venv: set-permissions # Creación de un entorno virtual.
	$(PYTHON) -m venv $(VENV_DIR)
	$(ACTIVATE) && $(PYTHON) -m pip install --upgrade pip

install: venv # Instalación de dependencias.
	$(ACTIVATE) && $(PYTHON) -m pip install -r requirements.txt

clean: # Limpiar archivos.
	rm -rf $(VENV_DIR)

reset: clean venv install # Limpiar y reinstalar dependencias.
