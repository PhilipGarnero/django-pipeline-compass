from pipeline.compilers import CompilerBase
from django.utils.encoding import smart_str
from django.conf import settings
from datetime import datetime
import sass
import os


def get_attr_from_file(filename, attr):
    with open(filename) as fd:
        for line in fd:
            if line.startswith(attr):
                return line[:-1].split('=')[1].strip(' ').strip("'").strip('"')
    return ''

def init_compiler():
    if "done" not in init_compiler.__dict__:
        global CSS_PATH
        global IMAGES_PATH
        global INCLUDE_PATHS

        INCLUDE_PATHS = []
        try:
            compass_project_path = os.path.abspath(os.path.join(settings.PIPELINE_COMPASS_CONFIG_RB, os.pardir))
        except AttributeError:
            CSS_PATH = ""
            IMAGES_PATH = ""
        else:
            INCLUDE_PATHS.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pipeline_compass', 'compass'))
            INCLUDE_PATHS.append(os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'sass_dir')))
            CSS_PATH = os.path.abspath(os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'css_dir')))
            IMAGES_PATH = os.path.abspath(os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'images_dir')))
        init_compiler.done = True


class LibSassCompassCompiler(CompilerBase):
    output_extension = 'css'

    def match_file(self, filename):
        init_compiler()
        return filename.endswith(('.scss', '.sass'))

    def output_path(self, filename):
        global raw_path
        if CSS_PATH:
            raw_path = os.path.join(CSS_PATH, '.'.join((os.path.splitext(os.path.basename(filename))[0], self.output_extension)))
            for p in settings.STATICFILES_DIRS:
                if raw_path.startswith(os.path.abspath(p)):
                    return raw_path.replace(os.path.abspath(p), "", 1).lstrip('/')
        filename = os.path.splitext(filename)
        raw_path = '.'.join((filename[0], self.output_extension))
        return raw_path

    def compile_file(self, infile, outfile, outdated=False, force=False):
        INCLUDE_PATHS.append(os.path.dirname(infile))
        if force or outdated:
            self.save_file(raw_path, sass.compile_file(str(infile), ','.join(INCLUDE_PATHS), IMAGES_PATH))

    def save_file(self, path, content):
        return open(path, 'w').write(smart_str(content))

    def is_outdated(self, infile, outfile):
        try:
            return datetime.fromtimestamp(os.path.getmtime(infile)) > datetime.fromtimestamp(os.path.getmtime(outfile))
        except OSError:
            return True
        #need a better way to find out if files need recompiling
