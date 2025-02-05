from setuptools import setup

setup(
    name='hasspy',
    version='0.1.0',
    packages=['hasspy', 'hasspy.components', 'hasspy.components.core'],
    install_requires=[
        'PyYAML'
    ],
    author='Makku',
    author_email='pypi@makku.uk',
    description='A Python library for creating Home Assistant automations.',
    github='https://github.com/MakkuMikan/hass-py',
    license='MIT',
    keywords='homeassistant home assistant automation',
)