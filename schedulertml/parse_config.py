from configparser import ConfigParser
import rtml

config = ConfigParser()
config.read('config.ini')

# default field values
request = {
    'general_filename': '',
    'general_path': '',
    'imageset_autostack': False,
    'imageset_binning': '1',
    'imageset_count': '1',
    'imageset_description': '',
    'imageset_dither': None,
    'imageset_exptime': '5',
    'imageset_filter': '',
    'imageset_limiting_mag': None,
    'imageset_solve': True,
    'observation_autofocus': '',
    'observation_count': '1',
    'observation_dec': '',
    'observation_description': None,
    'observation_interval': None,
    'observation_name': '',
    'observation_position_angle': None,
    'observation_ra': '',
    'observation_tolerance': None,
    'plan_airmass': None,
    'plan_airmass_max': None,
    'plan_airmass_min': None,
    'plan_bestefforts': 'True',
    'plan_description': '',
    'plan_earliest': '',
    'plan_horizon': None,
    'plan_hourangle_max': None,
    'plan_hourangle_min': None,
    'plan_latest': '',
    'plan_moon_dist': None,
    'plan_moon_down': '',
    'plan_moon_width': None,
    'plan_name': '',
    'plan_priority': None,
    'plan_sky_condition': '',
    'plan_start_now': 'False',
    'plan_user': 'New Observer',
    'project_description': '',
    'project_email': 'observer@example.com',
    'project_name': '',
    'project_organization': None,
    'project_pi': 'New Observer'
}

for key in request.iterkeys():
    section = key.split('_')[0].upper()
    keyword = '_'.join(key.split('_')[1:]).upper()
    if config.has_option(section, keyword) and len(config.get(section, keyword)) > 0:
        if config.get(section, keyword)[0] != ';':
            request[key] = config.get(section, keyword)

root = rtml.init(name=request['project_pi'],
                 email=request['project_email'],
                 organization=request['project_organization'])

root = rtml.add_request(root,
                        request_id=request['plan_name'],
                        bestefforts=request['plan_bestefforts'],
                        user=request['plan_user'],
                        description=request['plan_description'],
                        project=request['project_name'],
                        airmass=request['plan_airmass'],
                        airmass_min=request['plan_airmass_min'],
                        airmass_max=request['plan_airmass_max'],
                        horizon=request['plan_horizon'],
                        hourangle_min=request['plan_hourangle_min'],
                        hourangle_max=request['plan_hourangle_max'],
                        sky_condition=request['plan_sky_condition'],
                        moon_down=request['plan_moon_down'],
                        moon_dist=request['plan_moon_dist'],
                        moon_width=request['plan_moon_width'],
                        earliest=request['plan_earliest'],
                        latest=request['plan_latest'],
                        start_now=request['plan_start_now'],
                        priority=request['plan_priority'])

root = rtml.add_target(root,
                       request_id=request['plan_name'],
                       ra=request['observation_ra'],
                       dec=request['observation_dec'],
                       name=request['observation_name'],
                       description=request['observation_description'],
                       count=request['observation_count'],
                       interval=request['observation_interval'],
                       tolerance=request['observation_tolerance'],
                       autofocus=request['observation_autofocus'],
                       position_angle=request['observation_position_angle'])

root = rtml.add_picture(root,
                        filt=request['imageset_filter'],
                        target_name=request['observation_name'],
                        exptime=request['imageset_exptime'],
                        solve=request['imageset_solve'],
                        binning=request['imageset_binning'],
                        description=request['imageset_description'],
                        count=request['imageset_count'],
                        autostack=request['imageset_autostack'],
                        lim_mag=request['imageset_limiting_mag'],
                        dither=request['imageset_dither'])

if not request['general_filename']:
    if not request['project_name']:
        import datetime
        request['general_filename'] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    else:
        request['general_filename'] = request['project_name']

rtml.write(root, request['general_path']+request['general_filename']+'.xml')
