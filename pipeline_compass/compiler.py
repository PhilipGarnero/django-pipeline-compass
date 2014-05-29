from pipeline.compilers import CompilerBase
from django.utils.encoding import smart_str
from django.conf import settings

import scss
import os


def add_to_scss_path(path):
    load_paths = scss.config.LOAD_PATHS.split(',')  # get all saved paths
    if path not in load_paths:
        load_paths.append(path)
        scss.config.LOAD_PATHS = ','.join(load_paths) # reconstruct saved paths

def get_attr_from_file(filename, attr):
    """Get the value of an attribute within a file."""

    with open(filename) as fd:
        for line in fd:
            if line.startswith(attr):
                return line[:-1].split('=')[1].strip(' ').strip("'").strip('"')
    raise AttributeError("Couldn't find the attribute {0} in the file {1}".format(attr, filename))


def init_compiler():
    if "done" not in init_compiler.__dict__:
        global css_path
        try:
            css_path = os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'css_dir'))
        except:
            css_path = ''
        try:
            add_to_scss_path(os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'sass_dir')))
        except:
            pass
        try:
            images_path = os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'images_dir'))
        except:
            images_path = ''
        try:
            generated_images_path = os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'generated_images_dir'))
        except:
            generated_images_path = ''
        scss.config.STATIC_ROOT = images_dir if images_dir else os.path.join(compass_project_path, "images")
        scss.config.ASSETS_ROOT = generated_images_dir if generated_images_dir else scss.config.STATIC_ROOT
        init_compiler.done = True


class CompassCompiler(CompilerBase):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith(('.scss', '.sass'))

    def compile_file(self, infile, outfile, outdated=False, force=False):
        init_compiler()
        if css_path:
            outfile = os.path.join(css_path, os.path.basename(outfile))
        add_to_scss_path(os.path.dirname(infile))
        if force or outdated:
            self.save_file(outfile, scss.Scss(scss_opts={
                'compress': False,
                'debug_info': settings.DEBUG,
            }).compile(None, infile))

    def save_file(self, path, content):
        return open(path, 'w').write(smart_str(content))

compass_project_path = os.path.abspath(os.path.join(settings.PIPELINE_COMPASS_CONFIG_RB, os.pardir)) if settings.PIPELINE_COMPASS_CONFIG_RB else scss.config.PROJECT_ROOT
# add compass builtins to scss load path
add_to_scss_path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pipeline_compass', 'compass'))
