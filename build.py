#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")

name = "informaticup21-team-chillow"
default_task = "publish"

@init
def set_properties(project):
    project.depends_on_requirements("requirements.txt")
    project.set_property("coverage_break_build", False)
