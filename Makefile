init:
	pip install -r requirements.txt


#Pour les utilisateus ayant seulement python
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


#Pour les utilisateurs ayant python 3
test3:
	@echo "\033[1mRunning unit tests: \033[0m"
	@echo "-------------------"
	@python3 -m tests.unittests
	@echo "------------------- "
	@echo "\033[1mDone! \033[0m"

build3:
	@echo "\033[1mRunning the app: \033[0m"
	@echo "-------------------"
	@python -m src.main
	@echo "------------------- "
	@echo "\033[1mDone! \033[0m"