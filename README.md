[README.md](https://github.com/user-attachments/files/21708687/README.md)
# ROS 2机械臂控制系统部署与使用指南

## 项目概述

本项目是一个基于ROS 2的6自由度机械臂控制系统，集成了MoveIt2运动规划框架和CAN总线通信，实现机械臂的路径规划和实时控制。

### 主要功能
- 基于MoveIt2的运动规划
- CAN总线硬件通信
- 多种机械臂配置支持（arm1, arm2, arm3, arm5）
- 实时轨迹执行与速度控制
- 可视化界面（RViz2）

## 系统要求

### 硬件要求
- Ubuntu 22.04 LTS 操作系统
- USB-CAN适配器（支持ZLGCAN系列）
- 6自由度机械臂硬件
- 至少4GB RAM
- 10GB可用磁盘空间

### 软件依赖
- ROS 2 Humble Hawksbill
- MoveIt2
- Python 3.10+
- CMake 3.22+
- GCC/G++ 编译器

## 环境安装

### 1. 安装ROS 2 Humble

```bash
# 设置locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# 添加ROS 2 apt源
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 安装ROS 2
sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop
sudo apt install ros-humble-ros-base
sudo apt install ros-dev-tools
```

### 2. 安装MoveIt2

```bash
sudo apt install ros-humble-moveit
sudo apt install ros-humble-moveit-configs-utils
sudo apt install ros-humble-moveit-ros-move-group
sudo apt install ros-humble-moveit-kinematics
sudo apt install ros-humble-moveit-ros-visualization
sudo apt install ros-humble-moveit-setup-assistant
```

### 3. 安装其他依赖

```bash
# 控制器相关
sudo apt install ros-humble-ros2-control
sudo apt install ros-humble-ros2-controllers
sudo apt install ros-humble-joint-state-publisher
sudo apt install ros-humble-joint-state-publisher-gui
sudo apt install ros-humble-robot-state-publisher

# 可视化工具
sudo apt install ros-humble-rviz2
sudo apt install ros-humble-xacro

# Python依赖
pip3 install transforms3d
```

## 项目部署

### 1. 创建工作空间

```bash
mkdir -p ~/ros2_ws
cd ~/ros2_ws
```

### 2. 复制项目文件

将提供的src目录复制到工作空间：

```bash
cp -r /path/to/your/src ~/ros2_ws/
```

### 3. 配置CAN驱动

```bash
# 复制CAN库文件到系统目录
sudo cp ~/ros2_ws/src/demo/lib/libcontrolcan.so /usr/lib/
sudo ldconfig

# 设置USB设备权限
sudo chmod 666 /dev/ttyUSB*
# 或创建udev规则
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="04e8", MODE="0666"' | sudo tee /etc/udev/rules.d/99-usbcan.rules
sudo udevadm control --reload-rules
```

### 4. 编译项目

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install

# 如果遇到问题，可以尝试分包编译
colcon build --packages-select ti5_urdf
colcon build --packages-select arm1 arm2 arm3 arm5
colcon build --packages-select demo
```

### 5. 设置环境变量

```bash
# 添加到~/.bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## 使用指南

### 1. 启动机械臂仿真

选择一个机械臂配置（以arm1为例）：

```bash
# 终端1：启动MoveIt演示
ros2 launch arm1 demo.launch.py

# 或者分步启动
# 终端1：启动move_group
ros2 launch arm1 move_group.launch.py

# 终端2：启动RViz可视化
ros2 launch arm1 moveit_rviz.launch.py
```

### 2. 启动硬件控制节点

```bash
# 终端3：启动CAN通信节点
ros2 run demo demo

# 如果需要调试输出
ros2 run demo demo --ros-args --log-level debug
```

### 3. 运行Python控制脚本（可选）

如果要使用Python控制接口：

```bash
# 先确保脚本可执行
chmod +x ~/ros2_ws/move_a_b_round.py

# 运行脚本
python3 ~/ros2_ws/move_a_b_round.py
```

### 4. 在RViz中进行路径规划

1. 在RViz窗口中，找到MotionPlanning插件
2. 在"Planning"标签页中：
   - 使用交互式标记设置目标位置
   - 点击"Plan"按钮生成路径
   - 点击"Execute"按钮执行路径
3. 机械臂将通过CAN总线接收命令并执行动作

## 系统架构说明

### 节点通信流程

```
RViz GUI -> MoveIt Planning -> /display_planned_path topic -> demo节点 -> CAN总线 -> 机械臂硬件
```

### 主要话题

- `/display_planned_path`: 规划的轨迹信息
- `/joint_states`: 关节状态反馈
- `/move_group/status`: 规划状态
- `/joy`: 手柄控制输入（可选）

### CAN通信协议

- 波特率：1Mbps
- CAN ID分配：1-6对应6个关节
- 命令类型：
  - 0x08: 读取位置
  - 0x1E: 设置目标位置
  - 0x24: 设置正向速度限制
  - 0x25: 设置负向速度限制

## 常见问题解决

### 1. CAN设备无法打开

```bash
# 检查设备连接
lsusb | grep CAN

# 检查权限
ls -l /dev/ttyUSB*

# 重新加载驱动
sudo modprobe can
sudo modprobe can-raw
```

### 2. 编译错误

```bash
# 清理之前的编译
cd ~/ros2_ws
rm -rf build install log

# 检查依赖
rosdep install --from-paths src --ignore-src -r -y

# 重新编译
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release
```

### 3. 运行时找不到节点

```bash
# 确保source了工作空间
source ~/ros2_ws/install/setup.bash

# 检查包是否正确安装
ros2 pkg list | grep demo
ros2 pkg list | grep arm1
```

### 4. RViz无法显示机器人模型

```bash
# 检查URDF是否正确加载
ros2 param get /robot_state_publisher robot_description

# 检查TF树
ros2 run tf2_tools view_frames
```

## 安全注意事项

⚠️ **重要安全提示**：

1. **紧急停止**：确保硬件有物理急停按钮
2. **速度限制**：首次运行时使用低速模式（修改default_velocity_scaling_factor）
3. **碰撞检测**：在实际运行前在仿真中充分测试
4. **工作空间**：确保机械臂周围有足够的安全空间
5. **权限控制**：限制CAN设备的访问权限

## 性能优化

### 1. 实时性优化

```bash
# 设置实时优先级
sudo chrt -f 50 ros2 run demo demo

# 设置CPU亲和性
taskset -c 0-3 ros2 run demo demo
```

### 2. 通信优化

编辑`~/.ros2/config/default_dds.xml`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<dds>
    <profiles>
        <transport_descriptors>
            <transport_descriptor>
                <transport_id>CustomUDPv4</transport_id>
                <type>UDPv4</type>
                <sendBufferSize>1048576</sendBufferSize>
                <receiveBufferSize>1048576</receiveBufferSize>
            </transport_descriptor>
        </transport_descriptors>
    </profiles>
</dds>
```

## 日志和调试

### 查看日志

```bash
# 实时查看所有节点日志
ros2 run rqt_console rqt_console

# 查看特定节点日志
ros2 topic echo /rosout
```

### 调试CAN通信

```bash
# 监控CAN总线
candump can0

# 发送测试命令
cansend can0 001#0800000000000000
```

## 维护和更新

### 定期维护

1. 每周检查日志文件大小
2. 每月更新系统依赖
3. 定期备份配置文件
4. 检查硬件连接状态

### 系统更新

```bash
# 更新ROS包
sudo apt update
sudo apt upgrade ros-humble-*

# 重新编译项目
cd ~/ros2_ws
colcon build --cmake-clean-cache
```

## 联系支持

- 项目维护者：zx
- 邮箱：2290787180@qq.com
- 问题反馈：请提供日志文件和系统配置信息

## 许可证

本项目采用BSD许可证，详见各package.xml文件。

---

*文档版本：1.0*  
*最后更新：2024年*
