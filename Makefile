srctree := $(shell pwd)
default: help
obj := .
KCONFIG_CONFIG := .env

profiles_dir:
	@mkdir -p profiles

config_exists:
	@if [ ! -f ./.config ]; then echo "Error: .config file not found"; exit 1; fi

.PHONY: setup
setup: deps # Update the local repo and install deps
	@git pull
	@pip install -r deps

.PHONY: clean
clean: # remove uneeded files
	@rm -rfv cogs/__pycache__
	@rm -rfv misc/__pycache__
	@rm -rfv __pycache__
	@rm -v .config.old

.PHONY: deploy
deploy: profiles_dir config_exists # Run the bot
	@python -m main.py

.PHONY: menuconfig
menuconfig: # Configure the bot
	$(Q)kconfig-mconf Kconfig

.PHONY: config
config: # Configure the bot (alias for menuconfig)
	$(Q)kconfig-mconf Kconfig


.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
