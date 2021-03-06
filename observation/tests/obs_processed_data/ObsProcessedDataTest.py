import datetime
import json
import logging
import logging.config
import os
import traceback
from os.path import join as pjoin

import unittest2 as unittest
from curwmysqladapter import MySQLAdapter

from observation.obs_processed_data.ObsProcessedData import create_processed_timeseries


class ObsProcessedDataTest(unittest.TestCase):
    logger = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.root_dir = os.path.dirname(os.path.realpath(__file__))
            config = json.loads(open(pjoin(cls.root_dir, '../../config/CONFIG.json')).read())

            # Initialize Logger
            logging_config = json.loads(open(pjoin(cls.root_dir, '../../config/LOGGING_CONFIG.json')).read())
            logging.config.dictConfig(logging_config)
            cls.logger = logging.getLogger('MySQLAdapterTest')
            cls.logger.addHandler(logging.StreamHandler())
            cls.logger.info('setUpClass')

            MYSQL_HOST = "localhost"
            MYSQL_USER = "root"
            MYSQL_DB = "curw"
            MYSQL_PASSWORD = ""

            if 'MYSQL_HOST' in config:
                MYSQL_HOST = config['MYSQL_HOST']
            if 'MYSQL_USER' in config:
                MYSQL_USER = config['MYSQL_USER']
            if 'MYSQL_DB' in config:
                MYSQL_DB = config['MYSQL_DB']
            if 'MYSQL_PASSWORD' in config:
                MYSQL_PASSWORD = config['MYSQL_PASSWORD']

            cls.adapter = MySQLAdapter(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB)
            cls.eventIds = []
        except Exception as e:
            traceback.print_exc()

    @classmethod
    def tearDownClass(cls):
        cls.logger.info('tearDownClass')

    def setUp(self):
        self.logger.info('setUp')

    def tearDown(self):
        self.logger.info('tearDown')

    def test_createProcessedDataForLastHour(self):
        self.logger.info('createRawDataForLastHour')
        OBS_CONFIG = pjoin(self.root_dir, "../../config/StationConfig.json")
        CON_DATA = json.loads(open(OBS_CONFIG).read())
        stations = CON_DATA['stations']
        self.logger.debug('stations %s', stations)
        start_date_time = datetime.datetime(2018, 1, 2, 12, 0, 0)
        end_date_time = datetime.datetime(2018, 1, 2, 16, 0, 0)
        duration = dict(start_date_time=start_date_time, end_date_time=end_date_time)
        opts = dict(force_insert=True)

        create_processed_timeseries(self.adapter, stations, duration, opts)
