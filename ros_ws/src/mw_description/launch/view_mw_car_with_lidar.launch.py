# Copyright (c) 2022, Stogl Robotics Consulting UG (haftungsbeschränkt) (template)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Author: Dr. Denis
#

import os

from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import LifecycleNode
from launch.launch_description_sources import AnyLaunchDescriptionSource


def generate_launch_description():
    # Declare arguments
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "description_package",
            default_value="mw_description",
            description="Description package of the mw. Usually the argument is not set, \
        it enables use of a custom description.",
        )
    )

    # Initialize Arguments
    description_package = LaunchConfiguration("description_package")

    # Get URDF via xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare(description_package), "urdf", "mw.urdf.xacro"]
            )
        ]
    )

    robot_description = {"robot_description": robot_description_content}

    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare(description_package), "rviz", "mw.rviz"]
    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )
    foxglove_bridge = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('foxglove_bridge'),
                'launch/foxglove_bridge_launch.xml'))
    )

    share_dir = get_package_share_directory('mw_description')
    parameter_file = LaunchConfiguration('params_file')

    params_declare = DeclareLaunchArgument('params_file',
                                           default_value=os.path.join(
                                               share_dir, 'config', 'ydlidar.yaml'),
                                           description='FPath to the ROS2 parameters file to use.')
    
    lidar_node = LifecycleNode(package='ydlidar',
                                executable='ydlidar_node',
                                name='ydlidar_node',
                                output='screen',
                                emulate_tty=True,
                                parameters=[parameter_file],
                                namespace='/',
                                )

    return LaunchDescription(
        declared_arguments
        + [
            joint_state_publisher_node,
            robot_state_publisher_node,
            params_declare,
            lidar_node,
            # rviz_node,
            foxglove_bridge,
        ]
    )
