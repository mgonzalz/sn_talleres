VENV=venv
BIN=$(VENV)/Scripts

# Creación del entorno virtual e instalación de dependencias
install:
	python -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/python -m pip install -r requirements.txt

activate-cmd: # Activar en CMD
	$(BIN)/activate.bat

activate-ps: # Activar en PowerShell
	$(BIN)/Activate.ps1

activate-bash: # Activar en Git Bash (Windows)
	.$(VENV)/Scripts/activate

clean:
	- rm -rf $(VENV) __pycache__ 2>/dev/null || rmdir /s /q $(VENV) __pycache__

reset: clean install
