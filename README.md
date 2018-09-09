# About

This is a command line program that prints out food truck information from the [Mobile Food Schedule dataset](https://data.sfgov.org/Economy-and-Community/Mobile-Food-Schedule/jjew-r69b).

# Installation

Minimally, you need Python 2 and the requests library to run the program. You can run it within a virtual environment or globally on your machine.

1. Virtual Environment (Recommended)

Clone this repository.

`$ git clone https://github.com/neonbadger/sf-food-truck.git`

Create a virtual environment for this project. If you don't have virtualenv installed, follow the guide [here](https://docs.python-guide.org/dev/virtualenvs/) to install.

```$ virtualenv env```

Activate the virtual environment.

```$ source env/bin/activate```

Install dependencies.

```$ pip install -r requirements.txt```

Run the program.

```$ python main.py```

Deactivate the virtual environment.

```$ deactivate```

2. Global

Clone this repository.

```$ git clone https://github.com/neonbadger/sf-food-truck.git```

Install requests library globally.

```$ pip install requests```

Run the program.

```$ python main.py```

# Scalability


