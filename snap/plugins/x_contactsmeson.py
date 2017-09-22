# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-

import os
import snapcraft
from snapcraft import common
from snapcraft.plugins import meson


class ContactsMesonPlugin(meson.MesonPlugin):

    def build(self):
        snapcraft.BasePlugin.build = lambda self: None
        super().build()
        self._run_meson()
        self._run_ninja_build_default()
        self._run_ninja_install()

    def _run_meson(self):
        os.makedirs(self.mesonbuilddir, exist_ok=True)
        env = self._build_environment()
        meson_command = ['meson']
        if self.options.meson_parameters:
            meson_command.extend(self.options.meson_parameters)
        meson_command.append(self.snapbuildname)
        self.run(meson_command, env=env)

    def _run_ninja_build_default(self):
        env = self._build_environment()
        ninja_command = ['ninja']
        self.run(ninja_command, env=env, cwd=self.mesonbuilddir)

    def _run_ninja_install(self):
        env = self._build_environment()
        env['DESTDIR'] = self.installdir
        ninja_install_command = ['ninja', 'install']
        self.run(ninja_install_command, env=env, cwd=self.mesonbuilddir)

    def _build_environment(self):
        env = os.environ.copy()
        env['CFLAGS'] = ' '.join(
            ['-I{0}/usr/include/evolution-data-server', '-I{0}/usr/include']).format(
                self.project.stage_dir)
        env['LDFLAGS'] = ' '.join(
            ['-Wl,-Bsymbolic-functions -Wl,-z,relro', ' -Wl,-rpath,{0}/usr/lib/evolution-data-server']).format(
                self.project.stage_dir)
        return env
