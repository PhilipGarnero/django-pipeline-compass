import os
import scss
from .compass_compiler import CompassCompiler


class PyScssCompassCompiler(CompassCompiler):
    def compile_file(self, infile, outfile, outdated=False, force=False):
        scss.config.STATIC_ROOT = self.images_path
        scss.config.ASSETS_ROOT = self.generated_images_path if self.generated_images_path else scss.config.STATIC_ROOT

        paths = self.include_paths + [os.path.dirname(infile)]
        load_paths = scss.config.LOAD_PATHS.split(',')  # get all saved paths
        for path in paths:
            if path not in load_paths:
                load_paths.append(path)
                scss.config.LOAD_PATHS = ','.join(load_paths)  # reconstruct saved paths

        if force or outdated:
            self.save_file(self.raw_path, scss.Scss(scss_opts={
                'compress': False,
                'style': "legacy",
                'debug_info': False,
            }).compile(None, infile))
