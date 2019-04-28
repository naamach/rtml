# ScheduleRTML

Write Remote Telescope Markup Language (RTML) XML files to be read by [ACP Scheduler](http://scheduler.dc3.com/).
ACP Scheduler is a commercial tool used to automatically schedule and execute observing plans for telescopes.
The observing plans can be entered manually using the Scheduler's GUI, or imported from RTML files.
The `ScheduleRTML` package allows you to automatically write these RTML plans.

## Getting started

### Prerequisites

* `python 2.7` or above
* `lxml`
* `configparser`

### Installing

Create and activate a `conda` environment with the necessary modules:
```
$ conda create -n schedulertml lxml configparser
$ source activate schedulertml
```
Install the `ScheduleRTML` package:
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

The `parse_config` script helps you to create an RTML plan with all available observing constraints, for a single target, defined in a configuration text file called `config.ini`.

Create a `config.ini` file, and save it in your work directory. Adjust the parameters according to your needs. Parameters that are left blank or omitted will be assigned with the default values:

```
; config.ini
[GENERAL]
PATH = 				; path of the output plan file, default: current directory
FILENAME =  			; output plan file name, default: current timestamp (YYYYMMDD_hhmmss.xml)

[PROJECT]
PI = New Observer 		; PI's name, for contact, default: New Observer
EMAIL = observer@example.com 	; PI's email, default: observer@example.com
ORGANIZATION = 			; PI's organization, default: empty
DESCRIPTION = 			; project description, default: empty
NAME = Project name 		; project name, default: empty

[PLAN]
USER = New Observer	; ACP Scheduler observer name, default: New Observer
BESTEFFORTS = 1 	; best efforts. 1 - execute plan as long as the constraints are met, 0 - execute only if the plan can be completed within the constraints. default: 1
NAME = Plan1 		; plan's name, default: empty
AIRMASS = 		; maximal airmass limit (to be used with no minimal airmass limit), default: empty
AIRMASS_MIN = 1.02  	; minimal airmass limit, together with AIRMASS_MAX, default: empty
AIRMASS_MAX = 3 	; maximal airmass limit, together with AIRMASS_MIN, default: empty
HORIZON = 		; min elevation (integer), default: empty
HOURANGLE_MIN = -4.6 	; eastern hour angle limit, together with HOURANGLE_MAX, deafult: empty
HOURANGLE_MAX = 4.6 	; western hour angle limit, together with HOURANGLE_MIN, deafult: empty
SKY_CONDITION = 	; sky condition (Excellent, Good, Fair, Poor), deafult: empty
MOON_DOWN = 		; moon down (True/False), default: empty
MOON_DIST = 		; moon distance. needs to be set together with MOON_WIDTH, default: empty
MOON_WIDTH = 		; moon width. needs to be set together with MOON_DIST, default: empty
START_NOW = 		; if True - start plan immediately. default: empty
EARLIEST = 		; earliest observing date (format: 0001-01-01T00:00:00), default: empty
LATEST = 		; latest observing date (format: 0001-01-01T00:00:00), default: empty
PRIORITY = 		; plan priority
DESCRIPTION = 		; plan description

[OBSERVATION]
NAME = Target1		; observation name, default: empty
COUNT = 1		; observation count (how many times to repeat), default: 1
INTERVAL = 		; observation interval (between repeats) in hours. default: empty
TOLERANCE =  		; observation interval's tolerance (between repeats) in hours. default: empty
AUTOFOCUS = 		; perform autofocus before executing the observation, default: empty
DESCRIPTION = 		; observation description, default: empty
RA = 50.123		; target's RA, in deg, default: empty
DEC = +30.123		; target's Dec, in deg, default: empty
POSITION_ANGLE = 	; position angle, default: empty

[IMAGESET]
COUNT = 1		; imageset count (how many times to repeat), default: 1
AUTOSTACK = 		; stack imageset automatically (True/False), default: empty
SOLVE = True		; astrometrically solve the images (True/False), default: True
DESCRIPTION = 		; imageset description
EXPTIME = 300 		; imageset exposure time in seconds, default: 5. Use either EXPTIME or LIMITING_MAG. If both are included, use LIMITING_MAG.
LIMITING_MAG = 		; imageset limiting magnitude, default: empty. Use either EXPTIME or LIMITING_MAG. If both are included, use LIMITING_MAG.
BINNING = 1		; imageset binning, default: 1
FILTER = ExoP		; imageset filter, default: empty
DITHER = 		; dither telescope between exposures (0 - no dither, -1 - auto), deafult: empty
```

In python, run:

```
from schedulertml import parse_config

parse_config
```

### Creating a Complex Plan

Use the `schedulertml.rtml` methods following the above conventions, to add more requests, targets, and pictures.

### Uploading the plan to a remote ACP Scheduler server

Assuming ACP Scheduler is installed on a remote Windows host, with `ssh` connection available using `Cygwin`, you can automatically upload and add the RTML plan you created to the ACP Scheduler database, using:

```
from schedulertml import rtml

rtml.import_to_remote_scheduler("NewPlan.xml",
                                username="remote_user",
                                remote_host="remote_host",
                                remote_path="/home/remote_user/",
                                cygwin_path="C:\\cygwin64\\home\\remote_user\\")
```

This will upload to the RTML plan `NewPlan.xml` and a VBScript `import.vbs` to the remote host `remote_user@remote_host`, to the remote `Cygwin` directory `/home/remote_user/`. It will then use the VBScript `import.vbs` to import the new plan (now located at `C:\cygwin64\home\remote_user\`) to the ACP Scheduler database.
