profiles_dir:
	@mkdir -p profiles

env_exists:
	@test -f ./.env

setup: deps
	@pip install -r deps

clean:
	@rm -rf __pycache__

deploy: profiles_dir env_exists
	@python bot.py

