===============
MLWrapper
===============

MLWrapper is a Python Flask application for `survivors` library.

It allows building survival models and visualize forecasts.

=======================
About Survival Analysis
=======================

The objective in `survival analysis`_ (also referred to as time-to-event or reliability analysis)
is to establish a connection between covariates and the time of an event.

Survival analysis is a set of statistical models and methods used for estimating  time until the occurrence of an event (or the probability that an event has not occurred). These methods are widely used in demography, e.g. for estimating lifespan or age at the first childbirth, in healthcare, e.g. for estimating duration of staying in a hospital or survival time after the diagnosis of a disease, in engineering (for reliability analysis), in insurance, economics, and social sciences.

Statistical methods need data, but complete data may not be available, i.e. the exact time of the event may be unknown for certain reasons  (the event did not occur before the end of the study or it is unknown whether it occurred). In this case, events are called censored. The data are censored from below (left censored) when below a given value the exact values of observations is unknown. Right censored data (censored from above) does not have exact observations above a given value. Further in this paper, right censoring is considered.

==========
References
==========

Methods from **survivors** are based on following paper.

  Vasilev I., Petrovskiy M., Mashechkin I. Survival Analysis Algorithms based on Decision Trees with Weighted Log-rank Criteria. – 2022.

.. code::

  @article{vasilev2022survival,
    title={Survival Analysis Algorithms based on Decision Trees with Weighted Log-rank Criteria},
    author={Vasilev, Iulii and Petrovskiy, Mikhail and Mashechkin, Igor},
    year={2022}
  }

.. _survival analysis: https://en.wikipedia.org/wiki/Survival_analysis