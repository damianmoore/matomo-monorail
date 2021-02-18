from setuptools import setup


setup(
   name='matomo_monorail',
   version='0.1.6',
   description='Improve Matomo analytics with server-side traffic using Django',
   author='Damian Moore',
   author_email='damian@epixstudios.co.uk',
   packages=['matomo_monorail', 'matomo_monorail.management', 'matomo_monorail.management.commands', 'matomo_monorail.migrations'],
   install_requires=['django', 'requests'],
)
