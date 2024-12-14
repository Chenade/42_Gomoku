###############################################################################
#                                                                             #
#                              Basic Config                                   #
#                                                                             #
###############################################################################
NAME = Gomoku

VENV           = venv
VENV_PYTHON    = $(VENV)/bin/python
BIN            = $(VENV)/bin/


YELLOW2		= "\033[33m"
RED			= "\033[31m"
GREEN		= "\033[92m"
GREEN2		= "\033[42m"
BLUE2		= "\033[44m"
X			= "\033[0m"
UP			= "\033[A"
CUT			= "\033[K"
DARKCYAN 	= '\033[36m'
BOLD 		= '\033[1m'
GREY		= '\033[90m'
###############################################################################
#                                                                             #
#                                   COMMAND                                   #
#                                                                             #
###############################################################################

all: clear install $(NAME)

clear:
	clear
	@echo ${YELLOW2}"/****************************************************************************/"
	@echo "/*                                                                          */"
	@echo "/*                                                       :::      ::::::::  */"
	@echo "/*  GomoKu  <Post Common Core>                         :+:      :+:    :+:  */"
	@echo "/*                                                   +:+ +:+         +:+    */"
	@echo "/*  By: ykuo & rukobaya                            +#+  +:+       +#+       */"
	@echo "/*                                               +#+#+#+#+#+   +#+          */"
	@echo "/*                                                    #+#    #+#            */"
	@echo "/*                                                   ###   ########.fr      */"
	@echo "/*                                                                          */"
	@echo "/****************************************************************************/"${X}

install: venv/touchfile

venv/touchfile: requirements.txt
	virtualenv $(VENV)
	@echo ${GREEN2}"\nVirtual Environment Created Successfully"${X}"\n\n"
	. $(BIN)activate; pip install -Ur requirements.txt
	@echo ${GREEN2}"\nRequirements Installed Successfully"${X}"\n"

$(NAME):	
	@echo ${BLUE2}"\nStarting Gomoku......"${X}
	$(VENV_PYTHON) main.py

clean:
	@find . -iname "*.pyc" -delete
	@find . -type d -name __pycache__ -delete
	@echo ${RED}"Clean Successfully\n"${X}

fclean: clean
	@rm -rf $(VENV)
	@echo ${RED}"Virtual Environment Remove Successfully\n"${X}

re: fclean all

.PHONY: all clean fclean re install venv
