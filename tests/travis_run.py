#!/usr/bin/env python
# https://github.com/ahelal/travis-in-box

import yaml
import subprocess
import sys
import os.path


class TravisExec(object):
    def __init__(self, filename="travis.yml"):
        self.fail = False
        stream = open(filename, 'r')
        yaml_file = yaml.load(stream)
        # language
        self.language = yaml_file.get("language", None)

        # Section
        self.section_before_install = yaml_file.get("before_install", None)
        self.section_install = yaml_file.get("install", None)
        self.section_before_script = yaml_file.get("before_script", None)
        self.section_script = yaml_file.get("script", None)

        #self.section_after_script = yaml_file.get("after_script", None)
        self.section_after_failure = yaml_file.get("after_failure", None)
        self.section_after_success = yaml_file.get("after_success", None)

    def _setup(self):
        if self.language == "python":
            print "********** Setup Python  **********"
            print ""
            # Since we are not using container we have to install various lang our self
            # So this is probably not the best way to do it
            self._execute_command(["sudo apt-get install python-setuptools python-pip -y"])
        else:
            print "Errors unsupported language {}".format(self.language)
            exit(1)

    def life_cycle(self):
        # See http://docs.travis-ci.com/user/build-configuration/

            # 1. setup language
            self._setup()
            # 4. Run before_install commands
            self.run_command("before_install", self.section_before_install, self.section_after_failure)
            # 5. Run install commands
            self.run_command("install", self.section_install, self.section_after_failure)
            # 6. Run before_script commands
            self.run_command("before_script", self.section_before_script, self.section_after_failure)
            # 7. Run test script commands
            self.run_command("script", self.section_script, self.section_after_failure)
            # 8 . if we reach this point we made it run after_success
            self.run_command("after_success", self.section_after_success, None)

    @staticmethod
    def _execute_command(command):
        new_command = ["echo '> " + item.rstrip('\n') + "' && { " + item.rstrip('\n') + " ; }" for item in command]
        new_command = " && ".join(new_command)

        p = subprocess.Popen(new_command, shell=True, stderr=subprocess.PIPE)
        while True:
            out = p.stderr.read(1)
            if out == '' and p.poll() is not None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()
        print ""
        return p.returncode

    def run_command(self, section_name=None, command=None, execute_on_failure=None):
        if command:
            print ""
            print "********** Running '{}' **********".format(section_name)
            return_code = self._execute_command(command)
            if return_code != 0:
                print ""
                print "********** Failed in '{}' **********".format(section_name)
                if execute_on_failure:
                    print ""
                    print "********** Running after_failure  **********".format(section_name)
                    self._execute_command(execute_on_failure)
                    exit(1)

filename = None
if len(sys.argv) == 1:
    filename = ".travis.yml"
elif len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print "Invalid number of arguments"
    exit(1)

if os.path.exists(filename):
    TravisExec(filename).life_cycle()
else:
    print "Could not file travis file '{}'".format(filename)
    exit(1)
