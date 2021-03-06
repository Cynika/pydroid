import unittest
import sys
import os
import time
import ConfigParser

import test_utils

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydroid import create_example
from pydroid.path_utils import *
from pydroid import complete_deploy
from pydroid.script_utils import is_device_rooted

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestExamples(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conf = ConfigParser.ConfigParser()
        cls.conf.read(examples_config_file())

    def test_examples_config(self):
        """
        Check whether all examples are present in the libs.conf
        configuration file.
        """
        examples = [l for l in os.listdir(examples_dir()) if l != 'examples.conf']
        self.assertTrue(sorted(examples), sorted(self.conf.sections()))

    def test_examples(self):
        """Test deploying all examples."""

        for example_name in self.conf.sections():
            os.chdir(TESTS_DIR)
            app_name = example_name + create_example.APP_NAME_SUFFIX
            package_name = "%s.%s" % (create_example.DOMAIN, app_name)
            project_dir = os.path.join(TESTS_DIR, app_name)
            test_utils.remove_directories_if_exist([project_dir])

            self.assertFalse(os.path.exists(project_dir))

            if is_device_rooted():
                test_utils.stop_app(package_name)
                self.assertFalse(test_utils.is_app_running(package_name))

            create_example.create_example([example_name])
            self.assertTrue(os.path.exists(project_dir))
            complete_deploy.complete_deploy()
            time.sleep(8)
            self.assertTrue(test_utils.is_app_running(package_name))
            if is_device_rooted():
                test_utils.stop_app(package_name)
            test_utils.remove_directories_if_exist([project_dir])


if __name__ == '__main__':
    unittest.main()
