#! /usr/bin/env python3

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node, SetParameter
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource
import os


def gps():
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("ublox_gps"), "launch/ublox_gps_node-launch.py")
        ),
    )


def ntrip():
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("ntrip_client"), "ntrip_client_launch.py")
        ),
        launch_arguments={
            "host": "148.149.0.87",
            "port": "10000",
            "mountpoint": "NETWORK_SOLUTION_RTCM3-GG",
            "authenticate": "true",
            "username": "Actor",
            "password": "igvcntrip2025",
        }.items(),
    )


def lidar_driver():
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("velodyne_driver"), "launch/velodyne_driver_node-VLP16-launch.py")
        )
    )


def lidar():
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("velodyne_pointcloud"), "launch/velodyne_transform_node-VLP16-launch.py"
            )
        )
    )
    

def imu_6_axis_LSM6DSOX():
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("imu_serial_to_ros_publisher"), "launch/imu_publisher.launch.py")
        ),
        launch_arguments={
            "serial_port": "/dev/tty_LSM6DSOX",
            "frame_id": "imu_link",
            "topic": "/imu/LSM6DSOX_data",
        }.items(),
    )


def rosboard():
    return Node(
        package="rosboard",
        executable="rosboard_node",
        name="rosboard_node",
        respawn=True,
        output="screen",
    )


def generate_launch_description():

    return LaunchDescription(
        [
            # gps(),
            # ntrip(),
            lidar_driver(),
            lidar(),
            imu_6_axis_LSM6DSOX(),
            rosboard(),
        ]
    )
