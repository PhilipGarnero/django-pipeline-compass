from pipeline.compilers import CompilerBase
from django.utils.encoding import smart_str
from django.conf import settings

from datetime import datetime
import scss
import os


def add_to_scss_path(path):
    load_paths = scss.config.LOAD_PATHS.split(',')  # get all saved paths
    if path not in load_paths:
        load_paths.append(path)
        scss.config.LOAD_PATHS = ','.join(load_paths) # reconstruct saved paths

def get_attr_from_file(filename, attr):
    with open(filename) as fd:
        for line in fd:
            if line.startswith(attr):
                return line[:-1].split('=')[1].strip(' ').strip("'").strip('"')
    return ''


def init_compiler():
    if "done" not in init_compiler.__dict__:
        global css_path
        css_path = os.path.abspath(os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'css_dir')))
        add_to_scss_path(os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'sass_dir')))
        images_path = os.path.abspath(os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'images_dir')))
        generated_images_path = os.path.abspath(os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'generated_images_dir')))
        scss.config.STATIC_ROOT = images_path if images_path != compass_project_path else os.path.join(compass_project_path, "images")
        scss.config.ASSETS_ROOT = generated_images_path if generated_images_path != compass_project_path else scss.config.STATIC_ROOT
        init_compiler.done = True


class CompassCompiler(CompilerBase):
    output_extension = 'css'

    def match_file(self, filename):
        init_compiler()
        return filename.endswith(('.scss', '.sass'))

    def output_path(self, filename):
        if css_path != compass_project_path:
            return os.path.join(css_path, '.'.join((os.path.splitext(os.path.basename(filename))[0], self.output_extension)))
        else:
            filename = os.path.splitext(filename)
            return '.'.join((filename[0], self.output_extension))

    def compile_file(self, infile, outfile, outdated=False, force=False):
        add_to_scss_path(os.path.dirname(infile))
        if force or outdated:
            self.save_file(outfile, scss.Scss(scss_opts={
                'compress': False,
                'debug_info': settings.DEBUG,
            }).compile(None, infile))

    def save_file(self, path, content):
        return open(path, 'w').write(smart_str(content))

    def is_outdated(self, infile, outfile):
        try:
            return datetime.fromtimestamp(os.path.getmtime(infile)) > datetime.fromtimestamp(os.path.getmtime(outfile))
        except OSError:
            return True
        # temporary solution, find a way with pyscss to do it


compass_project_path = os.path.abspath(os.path.join(settings.PIPELINE_COMPASS_CONFIG_RB, os.pardir)) if settings.PIPELINE_COMPASS_CONFIG_RB else scss.config.PROJECT_ROOT
# add compass builtins to scss load path
add_to_scss_path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pipeline_compass', 'compass'))
