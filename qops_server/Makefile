MANAGE_CMD = python manage.py
check:
	cat LOGO
	isort --recursive -c -df .
	isort -v
	yapf --recursive --diff .
	flake8 .
format:
	cat LOGO
	isort -rc .
	yapf --recursive -i .
mmg:
	cat LOGO
	$(MANAGE_CMD) makemigrations
mg:
	cat LOGO
	$(MANAGE_CMD) migrate
dev:
	cat LOGO
	ENV=dev  $(MANAGE_CMD) runserver 0.0.0.0:8000
serve:
	cat LOGO
	$(MANAGE_CMD) runserver 0.0.0.0:8000
test:
	cat LOGO
	ENV=test $(MANAGE_CMD) test
freeze:
	pipenv lock -r > requirements.txt
	pipenv lock -r --dev > dev-requirements.txt
help:
	@echo "    check"
	@echo "        Check your code style using flake8 & isort"
	@echo "    format"
	@echo "        Format your code using yapf && isort"
	@echo "    dev"
	@echo "        Start dev server."
	@echo "    serve"
	@echo "        Start server."
	@echo "    test"
	@echo "        Run unit test."
	@echo "    makemigrations"
	@echo "        Creating migrations for all apps."
	@echo "    migrate"
	@echo "        Running migrations."