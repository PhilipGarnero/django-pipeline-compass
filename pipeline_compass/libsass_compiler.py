import os
import sass
from .compass_compiler import CompassCompiler


class LibSassCompassCompiler(CompassCompiler):
    def compile_file(self, infile, outfile, outdated=False, force=False):
        self.include_paths.append(os.path.dirname(infile))
        if force or outdated:
            self.save_file(self.raw_path, sass.compile_file(str(infile), ','.join(self.include_paths)))
