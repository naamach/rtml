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

### The ACP Scheduler RTML Schema

The RTML schema compatible with ACP Scheduler is described [here](http://solo.dc3.com/ar/RefDocs/HelpFiles/ACPScheduler81Help/images/rtmlschema.png).
More details can be found [here](http://solo.dc3.com/ar/RefDocs/HelpFiles/ACPScheduler81Help/ImportExport.htm#rtml).

### Minimal Working Example

This is a minimal working example, that creates a plan, `NewPlan.xml`, with a single 300s exposure in V-band:

```
from schedulertml import rtml

root = rtml.init(name="Observer",
		 email="email@example.com")

root = rtml.add_request(root,
			request_id="Plan1",
			user="Observer")

root = rtml.add_target(root,
		       request_id="Plan1",
		       ra="50.123",
		       dec="+30.123",
		       name="Target1")

root = rtml.add_picture(root,
			filt="V",
			target_name="Target1",
			exptime="300",
			count="1")

rtml.write(root, "NewPlan.xml")
```

### Creating a Simple Plan Using `parse_config`

The `parse_config` module helps you to create an RTML plan with all available observing constraints, for a single target, defined in a configuration text file called `config.ini`.

Create a `config.ini` file, and save it in your work directory. Adjust the parameters according to your needs. Parameters that are left blank or omitted will be assigned with the default values:

```
; config.ini
[GENERAL]
PATH = 
FILENAME = 

[PROJECT]
USER = New Observer
EMAIL = observer@example.com
ORGANIZATION = 
DESCRIPTION = 
NAME = Project name

[PLAN]
BESTEFFORTS = 1
NAME = Plan1
AIRMASS = 
AIRMASS_MIN = 1.02  ; the shutter blocks the CCD above 80deg
AIRMASS_MAX = 3
HORIZON = ; min elevation (integer)
HOURANGLE_MIN = -4.6
HOURANGLE_MAX = 4.6
SKY_CONDITION = ; Excellent, Good, Fair, Poor
MOON_DOWN = ; True
MOON_DIST = 
MOON_WIDTH = 
START_NOW = True
EARLIEST = 
LATEST = 
PRIORITY = 
DESCRIPTION = 

[OBSERVATION]
COUNT = 1
INTERVAL = ; [hr]
TOLERANCE =  ; [hr]
AUTOFOCUS = 
NAME = Target1
DESCRIPTION = 
RA = 50.123
DEC = +30.123
POSITION_ANGLE = 

[IMAGESET]
COUNT = 1
AUTOSTACK = ; False
SOLVE = True
DESCRIPTION = 
EXPTIME = 300 ; [s]
LIMITING_MAG = 
BINNING = 1
FILTER = ExoP
DITHER = ; (0 - no dither, -1 - auto)
```

In python, run:

```
from schedulertml import parse_config

parse_config
```

### Creating Complex Plan

Use the `schedulertml.rtml` methods following the above conventions, to add more requests, targets, and pictures.
