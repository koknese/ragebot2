profiles_dir:
	@mkdir -p profiles

env_exists:
	@if [ ! -f ./.env ]; then echo "Error: .env file not found"; exit 1; fi

setup: deps
	@pip install -r deps

clean:
	@rm -rf __pycache__

deploy: profiles_dir env_exists
	@python bot.py

