import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'leonardo_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='davinci',
    maintainer_email='davinci@todo.todo',
    description='Bringup launch files, configuration, URDF description and ESP32 bridge',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'esp32_bridge_node = leonardo_bringup.esp32_bridge_node:main',
        ],
    },
)
