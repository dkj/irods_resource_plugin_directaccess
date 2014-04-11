import sys
if (sys.version_info >= (2,7)):
    import unittest
else:
    import unittest2 as unittest
from pydevtest_common import assertiCmd, assertiCmdFail, getiCmdOutput, get_hostname
import pydevtest_sessions as s
from resource_suite import ResourceBase, ResourceSuite, ShortAndSuite
from test_chunkydevtest import ChunkyDevTest
import socket
import os
import commands
import shutil
import subprocess
import re
import time



class Test_Direct_Access(unittest.TestCase, ResourceBase):
    ### iRODS server must have been started as root
    ### For this test the following user account and test file must exist:
    # username (alice)
    username = s.users[1]['name']
    
    # test file name
    filename = 'foo.txt'
    
    # test file path (/home/alice/foo.txt)
    filepath = os.path.join('/home', username, filename)


    # timestamp
    ts = str(int(time.time()))

    # make a direct access resource but leave demoResc alone
    hostname = socket.gethostname()
    my_test_resource = {
        "setup"    : [
            "iadmin mkresc daresc directaccess "+hostname+":/tmp/daresc."+ts+" ''"
        ],
        "teardown" : [
            "iadmin rmresc daresc",
            "rm -rf /tmp/daresc."+ts
        ],
    }
    
    def setUp(self):
        ResourceBase.__init__(self)
        s.oneuser_up()
        self.run_resource_setup()

    def tearDown(self):
        self.run_resource_teardown()
        s.oneuser_down()
        
    def test_phymove_back_and_forth(self):
        '''This test puts a file on a direct access resource on behalf of a given user, then 
            physically moves the file to a non-DA resource and then back to the direct access resource.
            In the process the test verifies that:
            * Filesystem metadata is properly collected and added to the object
            * Original file permissions are maintained on the direct access resource
            * Original file UID and GID are maintained on the direct access resource
            * On the non-DA resource the file gets the UID and GID of the iRODS service account
        '''
        
        ### stat test file
        orig_stat = os.stat(self.filepath)        
        
        ### put test file on direct resource from client user
        assertiCmd(s.sessions[1],"iput -R daresc "+self.filepath)   # expects success
        
        ### check the object's FS metadata (just owner and group for now)
        current_coll = s.sessions[1].runCmd("ipwd")[0].rstrip()
        query = "select DATA_FILEMETA_OWNER, DATA_FILEMETA_GROUP where COLL_NAME = '{0}' and DATA_NAME = '{1}'".format(current_coll, self.filename)
        
        # query for FS metadata
        res = s.sessions[1].runCmd('iquest', ['%s %s', query])
        
        # check owner and group in FS metadata
        assert (res[0].split() == [self.username, self.username])
        
        
        ### check ownership and permissions on the physical file
        # get physical file path
        res = s.sessions[1].runCmd("ils", ['-L', self.filename])
        phys_filename = res[0].rsplit(None, 1)[1]
        
        # stat physical file
        stat = os.stat(phys_filename)
        
        # compare with original file
        assert (orig_stat.st_mode == stat.st_mode 
                and orig_stat.st_uid == stat.st_uid
                and orig_stat.st_gid == stat.st_gid)


        ### phymove object to non-DA resource (demoResc)
        assertiCmd(s.sessions[1],"iphymv -R demoResc "+self.filename)   # expects success
        res = s.sessions[1].runCmd("ils", ['-L', self.filename])
        
        # get physical file on resource
        phys_filename = res[0].rsplit(None, 1)[1]
        
        # stat physical file
        stat = os.stat(phys_filename)
        

        # file's uid and gid should now be those of the current process (irods/irods)
        assert (stat.st_uid == os.getuid() and stat.st_gid == os.getgid())
        
        
        ### phymove object back to direct access resource
        assertiCmd(s.sessions[1],"iphymv -R daresc "+self.filename)   # expects success
        res = s.sessions[1].runCmd("ils", ['-L', self.filename])
        
        # get physical file on resource
        phys_filename = res[0].rsplit(None, 1)[1]
        
        # stat physical file
        stat = os.stat(phys_filename)

        # compare with original file
        assert (orig_stat.st_mode == stat.st_mode 
                and orig_stat.st_uid == stat.st_uid
                and orig_stat.st_gid == stat.st_gid)
        
        
        ### remove object
        assertiCmd(s.sessions[1],"irm -f "+self.filename)   # expects success
        



class Test_Regular_UFS_Operations(unittest.TestCase, ResourceSuite, ChunkyDevTest):
    
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