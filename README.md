# rtml

Write Remote Telescope Markup Language (RTML) XML files to be read by [ACP Scheduler](http://scheduler.dc3.com/).
ACP Scheduler is a commercial tool used to automatically schedule and execute observing plans for telescopes.
The observing plans can be entered manually using the Scheduler's GUI, or imported from RTML files.
The `rtml` package allows you to automatically write these RTML plans.

## Getting started

### Prerequisites

* `python 2.7`
* `lxml`
* `configparser`

### Installing

Create and activate a `conda` environment with the necessary modules:
```
$ conda create -p /path/to/rtml python=2.7 lxml configparser
$ source activate /path/to/rtml
```
Clone the `rtml` repository:
```
$ git clone https://github.com/naamach/rtml.git
```
Enter the `rtml` folder and run:
```
$ python setup.py install
```

## Using `rtml`

## The ACP Scheduler RTML Schema

The RTML schema compatible with ACP Scheduler is described [here](http://solo.dc3.com/ar/RefDocs/HelpFiles/ACPScheduler81Help/images/rtmlschema.png).
More details can be found [here](http://solo.dc3.com/ar/RefDocs/HelpFiles/ACPScheduler81Help/ImportExport.htm#rtml).






