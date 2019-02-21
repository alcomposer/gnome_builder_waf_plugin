#!/usr/bin/env-python3

import threading
import os

from gi.repository import Gio
from gi.repository import GLib
from gi.repository import Ide
from gi.repository import GObject

_ = Ide.gettext

_WAF = 'waf'

class WafBuildSystemDiscovery(Ide.SimpleBuildSystemDiscovery):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.props.glob = 'waf'
        self.props.hint = 'waf_plugin'
        self.props.priority = -200

class WafBuildSystem(Ide.Object, Ide.BuildSystem):
    project_file = GObject.Property(type=Gio.File)

    def do_get_id(self):
        return 'waf'

    def do_get_display_name(self):
        return 'Waf'

    def do_get_priority(self):
        return -200

class WafPipelineAddin(Ide.Object, Ide.PipelineAddin):
    """
    The WafPipelineAddin is responsible for creating the necessary build
    stages and attaching them to phases of the build pipeline.
    """

    def do_load(self, pipeline):
        context = self.get_context()
        build_system = Ide.BuildSystem.from_context(context)
        srcdir = pipeline.get_srcdir()

        # Ignore pipeline unless this is a waf project
        if type(build_system) != WafBuildSystem:
            return

        # Launcher for project configuration
        config_launcher = pipeline.create_launcher()
        config_launcher.set_cwd(srcdir)
        config_launcher.push_argv('python2')
        config_launcher.push_argv('waf')
        config_launcher.push_argv('configure')
        self.track(pipeline.attach_launcher(Ide.PipelinePhase.CONFIGURE, 0, config_launcher))

        # Now create our launcher to build the project
        build_launcher = pipeline.create_launcher()
        build_launcher.set_cwd(srcdir)
        build_launcher.push_argv('python2')
        build_launcher.push_argv('waf')

        clean_launcher = pipeline.create_launcher()
        clean_launcher.set_cwd(srcdir)
        clean_launcher.push_argv('python2')
        clean_launcher.push_argv('waf')
        clean_launcher.push_argv('clean')

        build_stage = Ide.PipelineStageLauncher.new(context, build_launcher)
        build_stage.set_name(_("Building project"))
        build_stage.set_clean_launcher(clean_launcher)
        build_stage.connect('query', self._query)
        self.track(pipeline.attach(Ide.PipelinePhase.BUILD, 0, build_stage))

    def do_unload(self, application):
        pass

    def _query(self, stage, pipeline, targets, cancellable):
        stage.set_completed(False)



