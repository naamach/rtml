from lxml import etree


def init(name="", email="", organization=""):
    root = etree.Element("RTML", version="2.3")

    # Contact
    contact = etree.SubElement(root, "Contact")
    etree.SubElement(contact, "User").text = name
    etree.SubElement(contact, "Email").text = email
    if organization:  # optional
        etree.SubElement(contact, "Organization").text = organization

    return root


def add_request(root, request_id, bestefforts="True", user="New Observer", description="", project="", airmass=None,
                airmass_min=None, airmass_max=None, horizon=None, hourangle_min=None, hourangle_max=None,
                sky_condition="", moon_down="", moon_dist=None, moon_width=None, earliest="", latest="",
                start_now=False, priority=None):

    # Request
    req = etree.SubElement(root, "Request")
    if bestefforts:
        req.set("bestefforts", bestefforts)
    etree.SubElement(req, "ID").text = request_id
    etree.SubElement(req, "UserName").text = user
    if description:
        etree.SubElement(req, "Description").text = description
    if project:
        etree.SubElement(req, "Project").text = project

    # Schedule constraints
    if any([airmass, airmass_min, airmass_max, hourangle_min, hourangle_max, start_now, earliest, latest]):
        schedule = etree.SubElement(req, "Schedule")

    # airmass
    if airmass:
        etree.SubElement(etree.SubElement(schedule, "Airmass"), "Value").text = airmass
    if airmass_max:
        am = etree.SubElement(schedule, "AirmassRange")
        etree.SubElement(etree.SubElement(am, "Minimum"), "Value").text = airmass_min
        etree.SubElement(etree.SubElement(am, "Maximum"), "Value").text = airmass_max

    # horizon
    if horizon:
        etree.SubElement(etree.SubElement(schedule, "Horizon"), "Value").text = horizon  # min elevation (integer)

    # hour angle
    if hourangle_min:
        ha = etree.SubElement(schedule, "HourAngleRange")
        etree.SubElement(etree.SubElement(ha, "East"), "Value").text = hourangle_min
        etree.SubElement(etree.SubElement(ha, "West"), "Value").text = hourangle_max

    # sky condition
    if sky_condition:
        etree.SubElement(schedule, "SkyCondition").text = sky_condition  # 'Excellent', 'Good', 'Fair', 'Poor'

    # moon
    if any([moon_down, moon_dist, moon_width]):
        moon = etree.SubElement(schedule, "Moon")
    if moon_down:
        etree.SubElement(moon, "Down").text = moon_down
    elif moon_dist:
        etree.SubElement(etree.SubElement(moon, "Distance"), "Value").text = moon_dist
        etree.SubElement(etree.SubElement(moon, "Width"), "Value").text = moon_width

    # time range
    if start_now:
        earliest = "0001-01-01T00:00:00"
        latest = "0001-01-01T00:00:00"
    if earliest:
        time = etree.SubElement(schedule, "TimeRange")
        etree.SubElement(time, "Earliest").text = earliest
        etree.SubElement(time, "Latest").text = latest

    # priority
    if priority:
        etree.SubElement(schedule, "Priority").text = priority

    return root


def add_target(root, request_id, ra, dec, name, description="", count="1", interval=None, tolerance=None, autofocus="",
               position_angle=None):
    req = root.find("./Request[ID='{}']".format(request_id))

    # Target
    target = etree.SubElement(req, "Target")
    if count:
        target.set("count", count)
    if interval:
        target.set("interval", interval)  # [hr]
    if tolerance:
        target.set("tolerance", tolerance)  # [hr]
    if autofocus:
        target.set("autofocus", autofocus)

    etree.SubElement(target, "Name").text = name

    if description:
        etree.SubElement(target, "Description").text = description

    # coordinates
    coo = etree.SubElement(target, "Coordinates")
    etree.SubElement(etree.SubElement(coo, "RightAscension"), "Value").text = ra
    etree.SubElement(etree.SubElement(coo, "Declination"), "Value").text = dec

    # position angle
    if position_angle:
        etree.SubElement(etree.SubElement(target, "PositionAngle"), "Value").text = position_angle

    return root


def add_picture(root, filt, target_name, exptime="5", solve=True, binning="1", description="", count="1", autostack=False,
                lim_mag=None, dither=None):
    target = root.find("./Request/Target[Name='{}']".format(target_name))

    # Picture
    pic = etree.SubElement(target, "Picture")
    if count:
        target.set("count", count)
    if autostack:
        target.set("autostack", autostack)

    etree.SubElement(pic, "Name").text = "{}_{}s".format(filt, exptime)
    if not solve:
        if description:
            description += ", #nosolve"
        else:
            description = "#nosolve"
    if description:
        etree.SubElement(pic, "Description").text = description
    if lim_mag:
        etree.SubElement(etree.SubElement(pic, "LimitingMagnitude"), "Value").text = lim_mag
    else:
        etree.SubElement(etree.SubElement(pic, "ExposureTime"), "Value").text = exptime
    etree.SubElement(etree.SubElement(pic, "Binning"), "Value").text = binning
    etree.SubElement(pic, "Filter").text = filt

    if dither:
        etree.SubElement(etree.SubElement(pic, "Dither"), "Value").text = dither

    return root


def write(root, filename):
    et = etree.ElementTree(root)
    et.write(filename, pretty_print=True)

    return


def import_to_scheduler(filename, username, remote_host, remote_path):

    # from Naked.toolshed.shell import execute_js, muterun_js
    # import sys
    # from subprocess import call

    f = open('import.js', 'w')
    f.write('// JavaScript (JScript)\n')
    f.write('var DB = new ActiveXObject("DC3.Scheduler.Database");\n')
    f.write('DB.Connect();\n')
    f.write('var I = new ActiveXObject("DC3.RTML23.Importer");\n')
    f.write('I.DB = DB;\n')
    f.write('I.Import("{}");\n'.format(filename))
    f.write('DB.Disconnect();\n')
    f.close()

    # # copy the plan file and import script to the remote machine
    # call('rsync -av {} {}@{}:{}'.format(filename, username, remote_host, remote_path))
    #
    # # import the RTML file to the Scheduler database on the remote machine
    # response = muterun_js('import.js')
    # if response.exitcode == 0:
    #     print(response.stdout)
    # else:
    #     sys.stderr.write(response.stderr)

    return
