init:
	pip install -r requirements.txt

test:
	@echo "\033[1mRunning unit tests: \033[0m"
	@echo "-------------------"
	@python3 -m tests.unittests
	@echo "------------------- "
	@echo "\033[1mDone! \033[0m"
