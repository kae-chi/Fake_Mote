VENV = venv

#OS
UNAME := $(shell uname)

# lowkey cooked if it's windows lol idk 
ifeq ($(UNAME), Linux)
    libcap_install = sudo apt-get install -y libcap-dev
else ifeq ($(UNAME), Darwin)
    libcap_install = brew install libpcap
endif

#install dependencies 
install:
	python3 -m venv $(VENV)
	# Install libcap with the platform-specific package manager
	$(libcap_install)
	./$(VENV)/bin/pip install -r requirements.txt

#run virtual enviorment
run:
	@read -p "Enter file path: " path; \
	echo "You entered: $$path"; \
	. venv/bin/activate && python3 fakemote.py $$path

#Clean up VENV
clean:
	rm -rf $(VENV)

# Reinstall all dependencies
reinstall: clean install
