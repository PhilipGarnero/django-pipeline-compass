Django Pipeline Compass
=======================

django-pipeline-compass is a compiler for [django-pipeline](https://github.com/cyberdelia/django-pipeline). Making it really easy to use scss and compass with out requiring the compass gem.

To install it :

    pip install -e git+https://github.com/PhilipGarnero/django-pipeline-compass.git#egg=django-pipeline-compass

And add it as a compiler to pipeline in your django `settings.py`.  
You can choose between official C libsass compiler (reliable) and pyScss module (lightweight)

	PIPELINE_COMPILERS = (
 		'pipeline_compass.libsass_compiler.LibSassCompassCompiler',
 		'pipeline_compass.pyscss_compiler.PyScssCompassCompiler',
	)

Specify the path of the config.rb used by compass.  
	PIPELINE_COMPASS_CONFIG_RB = "/path/to/config.rb"


The compass compatibility still has to be tested.

To suggest a feature or report a bug with the compilation:  
<https://github.com/vbabiy/django-pipeline-compass/issues>
