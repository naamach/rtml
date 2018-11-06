# ScheduleRTML

Write Remote Telescope Markup Language (RTML) XML files to be read by [ACP Scheduler](http://scheduler.dc3.com/).
ACP Scheduler is a commercial tool used to automatically schedule and execute observing plans for telescopes.
The observing plans can be entered manually using the Scheduler's GUI, or imported from RTML files.
The `schedulrtml` package allows you to automatically write these RTML plans.

## Getting started

### Prerequisites

* `python 2.7`
* `lxml`
* `configparser`

### Installing

Create and activate a `conda` environment with the necessary modules:
```
$ conda create -n schedulertml python=2.7 lxml configparser
$ source activate schedulertml
```
Install the `schedulertml` package:
```
$ pip install git+https://github.com/naamach/schedulertml.git
```

## Using `ScheduleRTML`

## The ACP Scheduler RTML Schema

The RTML schema compatible with ACP Scheduler is described [here](http://solo.dc3.com/ar/RefDocs/HelpFiles/ACPScheduler81Help/images/rtmlschema.png).
More details can be found [here](http://solo.dc3.com/ar/RefDocs/HelpFiles/ACPScheduler81Help/ImportExport.htm#rtml).






