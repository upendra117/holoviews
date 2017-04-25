#!/usr/bin/env python

import sys, os, glob
from shutil import copyfile
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup_args = {}
install_requires = ['param>=1.5.1,<2.0', 'numpy>=1.0']
extras_require={}

# Notebook dependencies of IPython 3
extras_require['notebook-dependencies'] = ['ipython', 'pyzmq', 'jinja2', 'tornado',
                                           'jsonschema',  'notebook', 'pygments']
# IPython Notebook + matplotlib + Lancet
extras_require['recommended'] = (extras_require['notebook-dependencies']
                                 + ['matplotlib', 'lancet-ioam'])
# Additional, useful third-party packages
extras_require['extras'] = (['pandas', 'seaborn', 'bokeh>=0.12.6']
                            + extras_require['recommended'])
# Everything including cyordereddict (optimization) and nosetests
extras_require['all'] = (extras_require['recommended']
                         + extras_require['extras']
                         + ['cyordereddict', 'nose'])

setup_args.update(dict(
    name='holoviews',
    version="1.8dev4",
    include_package_data=True,
    install_requires = install_requires,
    extras_require = extras_require,
    description='Stop plotting your data - annotate your data and let it visualize itself.',
    long_description=open('README.rst').read() if os.path.isfile('README.rst') else 'Consult README.rst',
    author= "Jean-Luc Stevens and Philipp Rudiger",
    author_email= "holoviews@gmail.com",
    maintainer= "IOAM",
    maintainer_email= "holoviews@gmail.com",
    platforms=['Windows', 'Mac OS X', 'Linux'],
    license='BSD',
    url='http://ioam.github.com/holoviews/',
    entry_points={
          'console_scripts': [
              'holoviews = holoviews.util.command:main'
          ]},
    packages = ["holoviews",
                "holoviews.core",
                "holoviews.core.data",
                "holoviews.element",
                "holoviews.interface",
                "holoviews.ipython",
                "holoviews.util",
                "holoviews.operation",
                "holoviews.plotting",
                "holoviews.plotting.mpl",
                "holoviews.plotting.bokeh",
                "holoviews.plotting.plotly",
                "holoviews.plotting.widgets"],
    package_data={'holoviews.ipython': ['*.html'],
                  'holoviews.plotting.mpl': ['*.mplstyle', '*.jinja', '*.js'],
                  'holoviews.plotting.bokeh': ['*.js', '*.css'],
                  'holoviews.plotting.plotly': ['*.js'],
                  'holoviews.plotting.widgets': ['*.jinja', '*.js', '*.css']},
    classifiers = [
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries"]
))

def check_pseudo_package(path):
    """
    Verifies that a fake subpackage path for assets (notebooks, svgs,
    pngs etc) both exists and is populated with files.
    """
    if not os.path.isdir(path):
        raise Exception("Please make sure pseudo-package %s exists." % path)
    else:
        assets = os.listdir(path)
        if len(assets) == 0:
            raise Exception("Please make sure pseudo-package %s is populated." % path)


def package_assets():
    """
    Generates pseudo-packages for all assets including notebooks,
    image and data files and for tests.
    """
    if not os.path.isdir('holoviews/assets'):
        os.mkdir('holoviews/assets')
    for asset in [g for ext in ('png', 'svg', 'rst') for g in glob.glob('./doc/*/*.%s' % ext)]:
        copyfile(asset, os.path.join('./holoviews/assets', os.path.basename(asset)))

    if not os.path.isdir('holoviews/notebooks'):
        os.mkdir('holoviews/notebooks')
    for nb in [g for ext in ('ipynb', 'npy') for g in glob.glob('./doc/*/*.%s' % ext)]:
        copyfile(nb, os.path.join('holoviews/notebooks/', os.path.basename(nb)))

    if not os.path.isdir('holoviews/tests'):
        os.mkdir('holoviews/tests')
    for nb in glob.glob('./tests/*.py'):
        copyfile(nb, os.path.join('holoviews/tests/', os.path.basename(nb)))

    setup_args['packages'] += ['holoviews.assets', 'holoviews.notebooks', 'holoviews.tests']
    setup_args['package_data']['holoviews.notebooks'] = ['*.ipynb', '*.npy']
    setup_args['package_data']['holoviews.assets'] = ['*.png', '*.svg', '*.rst']

    check_pseudo_package(os.path.join('.', 'holoviews', 'tests'))
    check_pseudo_package(os.path.join('.', 'holoviews', 'assets'))
    check_pseudo_package(os.path.join('.', 'holoviews', 'notebooks'))


if __name__=="__main__":

    if not 'develop' in sys.argv:
        package_assets()

    if ('upload' in sys.argv) or ('sdist' in sys.argv):
        import holoviews
        holoviews.__version__.verify(setup_args['version'])

    if 'install' in sys.argv:
        header = "HOLOVIEWS INSTALLATION INFORMATION"
        bars = "="*len(header)

        extras = '\n'.join('holoviews[%s]' % e for e in setup_args['extras_require'])

        print("%s\n%s\n%s" % (bars, header, bars))

        print("\nHoloViews supports the following installation types:\n")
        print("%s\n" % extras)
        print("Users should consider using one of these options.\n")
        print("By default only a core installation is performed and ")
        print("only the minimal set of dependencies are fetched.\n\n")
        print("For more information please visit http://holoviews.org/install.html\n")
        print(bars+'\n')

    setup(**setup_args)
