Change Log
----------
0.8.0
=====
* Fully refactor Javascript to use Next.js/React
* Refactor Django application as an API server
* Revise and make visualizations more thoroughly accessible.

0.7.0
=====
* Add support for Django 2.2 and update dependencies as possible

0.6.0
=====
* Finalize visualizations for now (TODO: better accessibility)
* Fix bug where filtering people list by social class could result in 404s

0.5.9
=====
* Minor updates to make citation admin functionality more useful

0.5.8
=====
* Add ego network visualization of Pliny and his correspondents to data viz
* Add citation models and backend functionality for scholarly citations of letters and people.
* Add detail view for correspondents in the letters.

0.5.6
=====

* Add tracking to people for their residency in Comum

0.5.5
=====

* Significant admin improvements:
   * Improvements to letter and person admins
   * Signal handling to create reciprocal relationships between people when appropriate
   * Open up possibility of the pre-BC birth dates if necessary

0.5.0
=====

* Initial release, with basic search functionality:
   * Django application with info pages
   * Search by nomina with autocomplete
   * Filter by social class, with buttons for mixing different strata
   * Sample visualizations of initial dataset
   * Unit tests of most functionality (90%+ coverage)
