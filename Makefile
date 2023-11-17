init:
	pip install -r requirements.txt

test:
	@echo "\033[1mRunning unit tests: \033[0m"
	@echo "-------------------"
	@python -m tests.unittests
	@echo "------------------- "
	@echo "\033[1mDone! \033[0m"

build:
	@echo "\033[1mRunning the app: \033[0m"
	@echo "-------------------"
	@python -m src.main
	@echo "------------------- "
	@echo "\033[1mDone! \033[0m"
