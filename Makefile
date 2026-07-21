# Nom de l'exécutable/script principal
PYTHON = python3
ENTRY = a_maze_ing.py
CONFIG = config.txt

.PHONY: all run install clean help

# Règle par défaut
all: run

# Règle pour lancer l'application
run:
	@if [ ! -f $(CONFIG) ]; then \
		echo "Erreur : Fichier $(CONFIG) introuvable."; \
		exit 1; \
	fi
	$(PYTHON) $(ENTRY) $(CONFIG)

# Installer les dépendances si vous avez un requirements.txt ou un package mazegen local
install:
	@if [ -f requirements.txt ]; then \
		$(PYTHON) -m pip install -r requirements.txt; \
	fi
	@if [ -d mazegen ] && [ -f mazegen/setup.py ]; then \
		$(PYTHON) -m pip install -e ./mazegen; \
	fi

# Nettoyer les fichiers de cache Python (__pycache__, .pyc, etc.)
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Aide sur les commandes disponibles
help:
	@echo "Commandes disponibles :"
	@echo "  make run     - Exécute l'application avec $(CONFIG)"
	@echo "  make install - Installe les dépendances requises"
	@echo "  make clean   - Supprime les fichiers de cache Python"