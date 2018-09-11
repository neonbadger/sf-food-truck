# About

This is a command line program that prints out food truck information from the [Mobile Food Schedule dataset](https://data.sfgov.org/Economy-and-Community/Mobile-Food-Schedule/jjew-r69b).

# Installation

You will need **Python 2.7** and the Python **requests** library. You can run this program within a virtual environment (recommended), or without if you have those dependencies installed globally.

## 1. Virtual Environment (Recommended)

Clone this repository.

```
$ git clone https://github.com/neonbadger/sf-food-truck.git
```

Create a virtual environment for this project. If you don't have virtualenv already installed, follow the guide [here](https://docs.python-guide.org/dev/virtualenvs/) to install.

```
$ virtualenv env
```

Activate the virtual environment.

```
$ source env/bin/activate
```

Install dependencies.

```
$ pip install -r requirements.txt
```

Run the program with **Python 2.7**.

```
$ python main.py
```
or execute as a script.
```
$ ./main.py
```

When you are done with the program, you can deactivate the virtual environment.

```
$ deactivate
```

## 2. Global Install (Alternative)

Clone this repository.

```
$ git clone https://github.com/neonbadger/sf-food-truck.git
```

Install requests library globally on your machine.

```
$ pip install requests
```

Run the program with Python 2.7.

```
$ python main.py
```
or
```
$ ./main.py
```

# Scalability

What I would do differently if this is a web application:

- Caching and data persistence

Right now, after the initial load, if the user chooses to continue, only the $offset URL parameter is
updated while all other URL parameters ($select, $order, $where, $limit) remain the same, and the endpoint is hit again and again -- each time for just 10 results. This is an expensive process, and it would slow down our application for the end user.

A caching mechanism can improve performance and make the program scalable. If identical query is received in the future, the results can be quickly returned from the cache. This is useful in a high-read, low-write environment, such as a web application retrieving data from external APIs.

Since the program may return the same result for a long interval (i.e. running it at 9:01 AM and 9:59 AM may make little difference), and the same query can be repeated every week (i.e. running it around the same time every Monday), and the responses are identical for all users, a web application doing the same can be a good candidate for caching and data persistence.

- Load balancing

A web application may be accessed by many users at the same time, hitting the same endpoint at the same time. A good web application should gracefully handle peaks and dips in traffic.

I would imagine a web application showing food truck information may see heavy traffic during lunch and dinner hours, and may potentially crash the website if the traffic is too high. A load balancer to distribute incoming traffic and spread them evenly over multiple servers based on capacity can improve speed and reduce lags during peak hours.
