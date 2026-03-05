import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    
     #获取默认的urdf路径
    urdf_packages_path=get_package_share_directory('show_dog')
    default_urdf_path=os.path.join(urdf_packages_path,'urdf','dog.urdf')
    #default_rviz2_config_path=os.path.join(urdf_packages_path,'config','display_robot_model.rviz')
    default_world_path=os.path.join(urdf_packages_path,'world','world.world')
    #获取一个urdf的参数方便修改
    action_dclare_arg_model_path=launch.actions.DeclareLaunchArgument(
        name='model',default_value=str(default_urdf_path),description="加载的模型路径"
    )
     #获取文件路径获取内容转换为参数值
    substitutions_command_result=launch.substitutions.Command(['cat ',
          launch.substitutions.LaunchConfiguration('model')]
     )
    
    robort_description_value=launch_ros.parameter_descriptions.ParameterValue(
        substitutions_command_result,
        value_type=str
    )
    
    action_robot_state_publisher=launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description':robort_description_value}]
    )

    action_gazebo_node=launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            [get_package_share_directory('gazebo_ros'),'/launch','/gazebo.launch.py']
        ),
        launch_arguments=[('world',default_world_path),('verbose','true')]
    )

    action_spawn_entity=launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic','/robot_description',
            '-entity','robot_dog'
        ]
    )

    return launch.LaunchDescription([
           action_dclare_arg_model_path,
           action_robot_state_publisher,
           action_gazebo_node,
           action_spawn_entity
    ])