import sys
if (sys.version_info >= (2,7)):
    import unittest
else:
    import unittest2 as unittest
from pydevtest_common import assertiCmd, assertiCmdFail, getiCmdOutput, get_hostname
import pydevtest_sessions as s
from resource_suite import ResourceSuite, ShortAndSuite
from test_chunkydevtest import ChunkyDevTest
import socket
import os
import commands
import shutil
import subprocess
import re
import time


class Test_DirectAccess_Resource(unittest.TestCase, ResourceSuite, ChunkyDevTest):
    
    # timestamp
    ts = str(int(time.time()))

    hostname = socket.gethostname()
    my_test_resource = {
        "setup"    : [
            "iadmin modresc demoResc name origResc",
            "iadmin mkresc demoResc directaccess "+hostname+":/tmp/demoResc."+ts+" ''"
        ],
        "teardown" : [
            "iadmin rmresc demoResc",
            "iadmin modresc origResc name demoResc",
            "rm -rf /tmp/demoResc."+ts
        ],
    }

    def setUp(self):
        ResourceSuite.__init__(self)
        s.twousers_up()
        self.run_resource_setup()

    def tearDown(self):
        self.run_resource_teardown()
        s.twousers_down()
        
    @unittest.skip("skipped")
    def test_iput_ibun_gzip_bzip2_from_devtest(self):
        pass
    
    @unittest.skip("skipped")
    def test_ireg_as_rodsuser(self):
        pass
    
    @unittest.skip("skipped")
    def test_ireg_as_rodsuser_in_vault(self):
        pass    
    
    @unittest.skip("skipped")
    def test_ireg_from_devtest(self):
        pass
    
    @unittest.skip("skipped")
    def test_irm(self):
        pass
        
    @unittest.skip("skipped")
    def test_irm_recursive_file(self):
        pass
    
    @unittest.skip("skipped")
    def test_irmtrash_admin(self):
        pass
    
    @unittest.skip("skipped")
    def test_large_dir_and_mcoll_from_devtest(self):
        pass
    
    @unittest.skip("skipped")
    def test_local_imv_to_directory(self):
        pass
    
    @unittest.skip("skipped")
    def test_mcoll_from_devtest(self):
        pass
        
    @unittest.skip("Will actually succeed when server is run as root")
    def test_local_iput_physicalpath_no_permission(self):
        pass

    @unittest.skip("Need to restart server as root")
    def test_ssl_iput_small_and_large_files(self):
        pass