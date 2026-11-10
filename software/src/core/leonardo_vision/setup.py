"""Package setup configuration for leonardo_vision."""

from setuptools import find_packages, setup

package_name = 'leonardo_vision'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='davinci',
    maintainer_email='davinci@robotics.local',
    description='Computer vision and homography engine for Leonardo robot',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'vision_node = leonardo_vision.vision_node:main',
            'homography_node = leonardo_vision.homography_node:main',
            'calibration_node = leonardo_vision.calibration_node:main',
        ],
    },
)
