from pipeline.compilers import CompilerBase
from django.utils.encoding import smart_str
from django.conf import settings
from datetime import datetime
import os


def get_attr_from_file(filename, attr):
    with open(filename) as fd:
        for line in fd:
            if line.startswith(attr):
                return line[:-1].split('=')[1].strip(' ').strip("'").strip('"')
    return ''


class CompassCompiler(CompilerBase):
    output_extension = 'css'

    def __init__(self, *args, **kwargs):
        super(CompassCompiler, self).__init__(*args, **kwargs)
        self.include_paths = []
        try:
            compass_project_path = os.path.abspath(os.path.join(settings.PIPELINE_COMPASS_CONFIG_RB, os.pardir))
        except AttributeError:
            self.css_path = ""
            self.images_path = ""
        else:
            self.include_paths.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pipeline_compass', 'compass'))
            self.include_paths.append(os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'sass_dir')))
            self.css_path = os.path.abspath(os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'css_dir')))
            self.images_path = os.path.abspath(os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'images_dir')))
            self.generated_images_path = os.path.abspath(os.path.join(compass_project_path, get_attr_from_file(settings.PIPELINE_COMPASS_CONFIG_RB, 'generated_images_dir')))

    def match_file(self, filename):
        return filename.endswith(('.scss', '.sass'))

    def output_path(self, filename):
        if self.css_path:
            self.raw_path = os.path.join(self.css_path, '.'.join((os.path.splitext(os.path.basename(filename))[0], self.output_extension)))
            for p in settings.STATICFILES_DIRS:
                if self.raw_path.startswith(os.path.abspath(p)):
                    return self.raw_path.replace(os.path.abspath(p), "", 1).lstrip('/')
        filename = os.path.splitext(filename)
        self.raw_path = '.'.join((filename[0], self.output_extension))
        return self.raw_path

    def save_file(self, path, content):
        return open(path, 'w').write(smart_str(content))

    def is_outdated(self, infile, outfile):
        try:
            return datetime.fromtimestamp(os.path.getmtime(infile)) > datetime.fromtimestamp(os.path.getmtime(outfile))
        except OSError:
            return True
