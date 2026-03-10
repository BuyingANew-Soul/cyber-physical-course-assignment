import os
import launch
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_controller import WebotsController
from webots_ros2_driver.utils import controller_url_prefix


def generate_launch_description():
    package_dir = get_package_share_directory('my_package')
    robot_description_path = os.path.join(
        package_dir, 'resource', 'my_robot.urdf'
    )

    # controller_url_prefix() is mandatory — it detects whether
    # to use TCP (Docker/WSL) or IPC (native Linux) automatically
    # and sets the correct protocol prefix.
    # On Linux with host network mode it returns: ipc://
    # On Docker bridge / WSL / Mac it returns:    tcp://<host>:1234/
    webots_host = os.environ.get('WEBOTS_HOST', 'localhost')

    my_robot_driver = WebotsController(
        robot_name='my_robot',
        parameters=[
            {'robot_description': robot_description_path},
        ],

    )

    return LaunchDescription([
        my_robot_driver,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=my_robot_driver,
                on_exit=[launch.actions.EmitEvent(
                    event=launch.events.Shutdown()
                )],
            )
        ),
    ])