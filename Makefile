PF := gen_ # profix
SCRIPT = c_cpp_properties.json file_exclude.json
TAR_DIR = ./
CUR_DIR := $(shell pwd)
MODE := --just-print
OPT := # optional parameter

run: $(SCRIPT)

%.json:
	-python3 $(addsuffix $*.py, $(PF)) $(TAR_DIR) $(MODE) $(OPT)

clean:
	-rm -rf $(TAR_DIR).vscode $(TAR_DIR)/.vscode