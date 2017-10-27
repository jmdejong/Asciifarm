from setuptools import setup, find_packages

setup(
    name='asciifarm',
    version='0.1.1',
    description="Troido's tilde.town ASCII Farm",
    long_description="TODO",
    author="Troido",
    author_email='troido@tilde.town',
    url='https://github.com/jmdejong/Asciifarm',
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('charmaps', ['asciifarm/charmaps/default.json', 'asciifarm/charmaps/fullwidth.json']),
    ],
    entry_points={
        'console_scripts': [
            'asciifarm = asciifarm.playgame:main',
            'hostfarm = asciifarm.hostfarms:main',
            # TODO: troido, if you want just one asciifarm command, change 
            # this to asccifarm and remove the previous two lines -wangofett, 2017-10-27
            'testasciifarm = asciifarm.__main__:main',
        ],
    },
    install_requires=[
        # TODO: Put other requirements here -wangofett, 2017-10-26
    ],
    tests_require=[
        # TODO: put tests requirements here -wangofett, 2017-10-26
    ],
    license='GPLv3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
