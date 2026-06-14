VENV=venv

PYTHON ?= python3.14
VENV_BIN=$(VENV)/bin

.PHONY: help info check setup create run clean

# -------------------------
# HELP
# -------------------------
help:
	@echo ""
	@echo "Multimedia Builder - Available Commands"
	@echo "---------------------------------------"
	@echo "make create        - Full setup (system check + python env)"
	@echo "make check         - Check system dependencies only"
	@echo "make run           - Run pipeline engine"
	@echo "make clean         - Remove virtual environment"
	@echo ""

# -------------------------
# INFO
# -------------------------
info:
	@echo "Project Info"
	@echo "------------"
	@echo "Python target: 3.11.*"
	@echo "System deps: ffmpeg, espeak-ng"
	@echo "Python deps: requirements.txt"
	@echo "Run: make create && make run"

# -------------------------
# SYSTEM CHECK ONLY
# -------------------------
check:
	@echo "Checking system dependencies..."

	@command -v $(PYTHON) >/dev/null 2>&1 || (echo "ERROR: $(PYTHON) not found" && exit 1)
	@$(PYTHON) --version

	@echo ""
	@command -v ffmpeg >/dev/null 2>&1 || (echo "ERROR: ffmpeg not found" && exit 1)
	@ffmpeg -version | head -n 1

	@echo ""
	@command -v espeak-ng >/dev/null 2>&1 || (echo "ERROR: espeak-ng not found" && exit 1)
	@espeak-ng --version | head -n 1

	@echo ""
	@echo "System dependencies OK."

# -------------------------
# PYTHON DEPENDENCIES ONLY
# -------------------------
setup:
	@echo "Setting up Python environment..."

	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
	fi

	@$(VENV_BIN)/python -m pip install --upgrade pip setuptools wheel
	@$(VENV_BIN)/python -m pip install -r requirements.txt

	@echo "Python dependencies installed."

# -------------------------
# CREATE (USER ENTRY POINT)
# -------------------------
create: check setup
	@echo ""
	@echo "Project ready."
	@echo "Run: make run"

# -------------------------
# RUN
# -------------------------
run:
	@echo "Running pipeline engine..."
	@$(VENV_BIN)/python runner.py

# -------------------------
# CLEAN
# -------------------------
clean:
	rm -rf $(VENV)
	@echo "Clean complete."
