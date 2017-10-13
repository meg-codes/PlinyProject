PlinyProject
------------

.. image:: https://www.travis-ci.org/bwhicks/PlinyProject.svg?branch=develop
    :target: https://www.travis-ci.org/bwhicks/PlinyProject

.. image:: https://codecov.io/gh/bwhicks/PlinyProject/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/bwhicks/PlinyProject


About
=====

The Pliny Project is part of an attempt to reconstruct the social world of 
Pliny the Younger through his personal letters. These are books 1-9 of the
larger corpus preserved in two manuscripts.

The project itself is held in a MySQL database using `Django <https://www.djangoproject.com/>`_ 
as the web front-end and ORM. 

The ultimate objective is to be able to make statistical assertions and 
visualizations dynamically regarding the social connections and status of 
Pliny's correspondents. While considerable scholarship has been directed at
these goals, very little of it has had a focus on being open access and 
dynamically searchable.

Installation and Running
========================

This is a pretty standard Django project, but to run it, ``pip install -r requirements.txt`` the 
requirements from ``requirements.txt`` and then run ``./manage.py`` from the 
project root. I highly recommend setting up a virtual environment in your
favorite Python tool (i.e. Virtualenv or Conda).

Obviously, this does not yet include a data import (but by all means contact
me if you're interested in my preliminary entries). 

To run the unit tests::
        
        pip install -r dev-requirements.txt
        pytest --cov

    

Bibliography
============

This is **not** comprehensive, but it lists some major prosopography sources
for Pliny the Younger.

* Birley, Anthony. *Onomasticon to the Younger Pliny. Letters and Panegyric.*
  Munich/Leipzig: K.G. Saur 2000.
* Sherwin-White, A.N. *The Letters of Pliny: A Historical and Social Commentary.* Clarendon: 1966.
* Syme, Ronald. *Tacitus* Oxford: 1958.
* ------. "Pliny's less successful friends," *Historia* 9 (1960): 362-79.
* ------. "People in Pliny," *Journal of Roman Studies* 58 (1968): 135-151.
* ------. "Correspondents of Pliny," *Historia* 34 (1985): 324-59.
  

  

