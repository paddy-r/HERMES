# HERMES
## Hierarchical Economic and Residential Microsimulation for Small areas

```
     ___         ___         ___         ___         ___         ___     
    /__/\       /  /\       /  /\       /__/\       /  /\       /  /\    
    \  \:\     /  /:/_     /  /::\     |  |::\     /  /:/_     /  /:/_   
     \__\:\   /  /:/ /\   /  /:/\:\    |  |:|:\   /  /:/ /\   /  /:/ /\  
 ___ /  /::\ /  /:/ /:/_ /  /:/~/:/  __|__|:|\:\ /  /:/ /:/_ /  /:/ /::\ 
/__/\  /:/\:/__/:/ /:/ //__/:/ /:/__/__/::::| \:/__/:/ /:/ //__/:/ /:/\:\
\  \:\/:/__\\  \:\/:/ /:\  \:\/:::::\  \:\~~\__\\  \:\/:/ /:\  \:\/:/~/:/
 \  \::/     \  \::/ /:/ \  \::/~~~~ \  \:\      \  \::/ /:/ \  \::/ /:/ 
  \  \:\      \  \:\/:/   \  \:\      \  \:\      \  \:\/:/   \__\/ /:/  
   \  \:\      \  \::/     \  \:\      \  \:\      \  \::/      /__/:/   
    \__\/       \__\/       \__\/       \__\/       \__\/       \__\/    

```

HERMES is a dynamic microsimulation framework for fast, efficient modelling of demographic processes. How HERMES works, and what the package includes, is described below.

- A demonstrator model including basic demographic processes (ageing, fertility, mortality and migration).
- An input population for use with the demonstrator model consisting of the population of the beautiful (but fictional) island of Meropis. This population was created with our artificial population generator.
- A Jupyter notebook, in which the model runs.

Developed for use within the [PHI-UK research consortium](https://www.phiuk.org/), "Innovating with people, places and communities".

Contact the development team below with queries, or raise an issue here.
- Hugh P. Rice (lead), h.p.rice@leeds.ac.uk
- Ric Colasanti, r.l.colasanti@leeds.ac.uk
- Andreas Hoehn, andreas.hoehn@glasgow.ac.uk

You can install the package in multiple ways.

1. The simplest way is to install via `pip`. First create a suitable Python environment using ```conda``` or ```venv```, for example, then run the following command. Ensure your Python version is 3.13 or later.

```
pip install git+https://github.com/paddy-r/HERMES.git
```

2. Alternatively, if you'd like to contribute to the development of HERMES, clone the repository using Git, then install it in development mode, as follows.

```
git clone https://github.com/paddy-r/HERMES.git
pip install -e .
```
