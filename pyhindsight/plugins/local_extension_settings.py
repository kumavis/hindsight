###################################################################################################
#
# local_extension_settings.py
#   Adds the settings of each Chrome extension found to the LocalSettings field
#
# Plugin Author: Aaron Kumavis (aaron@kumavis.me)
#
###################################################################################################

import os
import logging
from pyhindsight import utils

log = logging.getLogger(__name__)

# Config
friendlyName = "Local Extension Settings"
description = "Adds the settings of each Chrome extension found to the LocalSettings field"
version = "20210424"

artifactTypes = ("url", "LES")
remoteLookups = 0
browser = "Chrome"
browserVersion = 1
parsedItems = 0


def plugin(analysis_session=None):
    if analysis_session is None:
        return

    global parsedItems
    parsedItems = 0

    for found_profile_path in analysis_session.profile_paths:
        les_path = os.path.join(found_profile_path, 'Local Extension Settings')
        extensions_list = os.listdir(les_path)
        for extension_id in extensions_list:
            if extension_id != 'nkbihfbeogaeaoehlefnkodbefgpgknn':
                continue
            
            f = open("metamask-vault-history.json", "w")
            f.write('{')

            les_ext_path = os.path.join(les_path, extension_id)
            ldb_path = les_ext_path

            les_ldb_records = utils.get_ldb_records(les_ext_path)
            for record in les_ldb_records:
                if record["key"] != b'data':
                    continue
                
                if (parsedItems > 0):
                    f.write(',')
                parsedItems += 1

                f.write(f'\n"{record["seq"]}": {record["value"].decode("utf-8")}')

            f.write('}')
            f.close()

    # Description of what the plugin did
    return f'{parsedItems} extension settings parsed'
