.PHONY: install install-py install-npm dev dev-py dev-ui build clean

install: install-py install-npm
	@echo "All dependencies installed."

install-py:
	cd core && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "Python dependencies installed."

install-npm:
	cd apps/desktop && npm install
	@echo "Node dependencies installed."

dev:
	@echo "Starting HANTER..."
	@cd core && . venv/bin/activate && python main.py &
	@cd apps/desktop && npm run dev &
	@wait

dev-py:
	cd core && . venv/bin/activate && python main.py

dev-ui:
	cd apps/desktop && npm run dev

build:
	cd apps/desktop && npm run tauri-build

test:
	cd core && . venv/bin/activate && python -m pytest ../tests -v

lint:
	cd core && . venv/bin/activate && ruff check .
	cd apps/desktop && npx tsc --noEmit

clean:
	rm -rf core/venv apps/desktop/node_modules data/ apps/desktop/src-tauri/target
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned."
