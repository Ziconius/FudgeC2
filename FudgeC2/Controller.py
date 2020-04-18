#!/usr/bin/python3
import logging.config
import _thread
import time
import os
import yaml

from Storage.settings import Settings

with open(Settings.logging_config, 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

from ServerApp import ImplantManager
from NetworkProfiles.NetworkListenerManagement import NetworkListenerManagement

logger = logging.getLogger(__name__)


def check_tls_certificates(cert, key):
    cert_result = os.path.isfile(f"{os.getcwd()}/Storage/{cert}")
    key_result = os.path.isfile(f"{os.getcwd()}/Storage/{key}")
    if key_result is False or cert_result is False:
        logger.warning("Missing private keys for TLS listeners, this will cause them to fail.")
    return


def check_key_folders():
    # Placeholder for initialisation checking.
    try:
        if not os.path.isdir(Settings.file_download_folder):
            os.mkdir(f"{Settings.file_download_folder}")
            logger.info(f"Missing directory, now creating: {Settings.file_download_folder}")

        if not os.path.isdir(Settings.implant_resource_folder):
            os.mkdir(f"{Settings.implant_resource_folder}")
            logger.info(f"Missing directory, now creating: {Settings.implant_resource_folder}")

        if not os.path.isdir(Settings.campaign_export_folder):
            os.mkdir(f"{Settings.campaign_export_folder}")
            logger.info(f"Missing directory, now creating: {Settings.campaign_export_folder}")
        return True
    except Exception as Error:
        logger.warning(f"Exception setting up important directories: {Error}")
        return False


def start_controller():
    # Server configuration can be found in Storage/settings.py
    Manager.run(debug=Settings.server_app_debug,
                use_reloader=False,
                host='0.0.0.0',
                port=Settings.server_app_port,
                threaded=True,
                ssl_context=Settings.server_app_ssl)


if __name__ == "__main__":
    NLM = NetworkListenerManagement.instance
    Manager = ImplantManager.app
    NLM.startup_auto_run_listeners()

    try:
        check_tls_certificates(Settings.tls_listener_cert, Settings.tls_listener_key)
        check_key_folders()
        _thread.start_new_thread(start_controller, ())
    except Exception as E:
        print(f"Unable to start FudgeC2 server thread: {E}")
        exit()

    while 1:
        # Hold the application threads open
        time.sleep(15)
        pass
