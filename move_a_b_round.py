#!/usr/bin/env python


import sys
import copy
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped,Quaternion
from sensor_msgs.msg import Joy
import moveit2
#from moveit_msgs.srv import GetPlanningScene,GetPlanningSceneRequest
#from moveit_py.move_group_interface import MoveGroupInterface
#from moveit_py.planning_scene_interface import PlanningSceneInterface

def all_close(goal, actual, tolerance):
    all_equal = True
    if type(goal) is list:
        for index in range(len(goal)):
            if abs(actual[index] - goal[index]) > tolerance:
                return False
    
    elif type(goal) is geometry_msgs.msg.PoseStamped:
        return all_close(goal.pose, actual.pose, tolerance)

    elif type(goal) is geometry_msgs.msg.Pose:
        return all_close(pose_to_list(goal), pose_to_list(actual), tolerance)

    return True

class MoveGroupPythonIntefaceTutorial(object):
    def __init__(self):
    	rcl.init_argument(sys.argv)
    	moveit2.init_node("move_group_python_interface_tutorial")
    	self.group=moveit2.MoveGroupCommander(node = "armgroup")
    	self.display_trajectory_publisher = rospy.Publisher('/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=20)
        self.joy_subscriber = rcl.Subscriber("/joy",Joy,Joy,self.callback)
        #super(MoveGroupPythonIntefaceTutorial, self).__init__()

        #moveit_commander.roscpp_initialize(sys.argv)
        #rospy.init_node('move_group_python_interface_tutorial',
        #                anonymous=True)
        self.x=0
        self.y=0
        self.z=0.69
        self.roll=0
        self.pitch=0
        self.yaw=0
        self.ms=1
        # self.ww=1
        ## Instantiate a `RobotCommander`_ object. This object is the outer-level interface to
        ## the robot:
        #robot = moveit_commander.RobotCommander()
        #scene = moveit_commander.PlanningSceneInterface()

        #group_name = "armgroup"
        #group = moveit_commander.MoveGroupCommander(group_name)

        #display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
        #                                           moveit_msgs.msg.DisplayTrajectory,
        #                                           queue_size=20)

        #rospy.init_node("listenerjoy",anonymous=True)
        #rospy.Subscriber("/joy",Joy,self.callback)

        planning_frame = group.get_planning_frame()
        print("============ Reference frame: %s\n", planning_frame)

        # We can also print the name of the end-effector link for this group:
        eef_link = group.get_end_effector_link()
        print("============ End effector: %s\n",eef_link)

        # We can get a list of all the groups in the robot:
        group_names = robot.get_group_names()
        print("============ Robot Groups: %s\n", robot.get_group_names())

        # Sometimes for debugging it is useful to print the entire state of the
        # robot:
        print("============ Printing robot state\n")
        print("robot_current_state:  %s\n",robot.get_current_state())


        # Misc variables
        self.box_name = ''
        self.robot = robot
        self.scene = scene
        self.group = group
        self.display_trajectory_publisher = display_trajectory_publisher
        self.planning_frame = planning_frame
        self.eef_link = eef_link
        self.group_names = group_names

    def callback(self,data):
        self.go_to_pose_goal(data)
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.buttons)

    def listener(self):
        rospy.spin()

    def go_to_joint_state(self):
        group = self.group
        joint_goal = group.get_current_joint_values()
        joint_goal[2] = joint_goal[2]+0.1
        print(str(joint_goal[0]))
        joint_goal[1] = -pi/4-0.8
        joint_goal[0] = 0.1
        joint_goal[3] = 3.14
        joint_goal[4] = 0
        joint_goal[5] = 1.53
        # parameters if you have already set the pose or joint target for the group
        group.go(joint_goal, wait=True)

        group.stop()
        current_joints = self.group.get_current_joint_values()


    def go_to_joint_statei_3(self):
        group = self.group
        # We can get the joint values from the group and adjust some of the values:
        joint_goal = group.get_current_joint_values()
        joint_goal[0] = 0.5
        joint_goal[1] = -pi/4
        joint_goal[2] = 1.4
        joint_goal[3] = -pi/2-0.4
        joint_goal[4] = -1.6
        joint_goal[5] = pi/3+0.6
        group.go(joint_goal, wait=True)
    
        joint_goal = group.get_current_joint_values()
        joint_goal[0] = 0
        joint_goal[1] = -pi/4-0.5
        joint_goal[2] = 1.4
        joint_goal[3] = -pi/2-0.4
        joint_goal[4] = -1.6
        joint_goal[5] = pi/3+0.6
        group.go(joint_goal, wait=True)

        joint_goal[0] = -0.8
        joint_goal[1] = -pi/4
        joint_goal[2] = 1.4
        joint_goal[3] = -pi/2-0.4
        joint_goal[4] = -1.6
        joint_goal[5] = pi/3+0.6
        group.go(joint_goal, wait=True)


        joint_goal[0] = -1.6
        joint_goal[1] = -pi/4-0.5
        joint_goal[2] = 1.4
        joint_goal[3] = -pi/2-0.4
        joint_goal[4] = -1.6
        joint_goal[5] = pi/3+0.6
        group.go(joint_goal, wait=True)

        joint_goal[0] = -2.4
        joint_goal[1] = -pi/4
        joint_goal[2] = 1.4
        joint_goal[3] = -pi/2-0.4
        joint_goal[4] = -1.6
        joint_goal[5] = pi/3+0.6
        group.go(joint_goal, wait=True)

        joint_goal[0] = 0
        joint_goal[1] = -pi/4-0.5
        joint_goal[2] = 1.4
        joint_goal[3] = -pi/2-0.4
        joint_goal[4] = -1.6
        joint_goal[5] = pi/3+0.6
        group.go(joint_goal, wait=True)

        joint_goal[0] = 1.0
        joint_goal[1] = -pi/4
        joint_goal[2] = 1.4
        joint_goal[3] = -pi/2-0.4
        joint_goal[4] = -1.6
        joint_goal[5] = pi/3+0.6
        group.go(joint_goal, wait=True)

        joint_goal[0] = 1.5
        joint_goal[1] = -pi/4-0.8
        joint_goal[2] = 1.4
        joint_goal[3] = -pi/2-0.4
        joint_goal[4] = -1.6
        joint_goal[5] = pi/3+0.6
        group.go(joint_goal, wait=True)

        group.stop()

    def go_to_pose_goal(self,data):
        group = self.group
        pose_goal = geometry_msgs.msg.Pose()
        pose_goal.orientation.w = 1.0
        #pose_goal.position.x = self.x+0.01
        #self.x+=0.01

        rpylist=group.get_current_rpy()

        if data.buttons[0]==1:
            self.x+=0.05*self.ms
        elif data.buttons[2]==1:
            self.x-=0.05*self.ms
        elif data.buttons[1]==1:
            self.y+=0.05*self.ms
        elif data.buttons[3]==1:
            self.y-=0.05*self.ms
        elif data.buttons[5]==1:
            self.z+=0.05*self.ms
        elif data.buttons[7]==1:
            self.z-=0.05*self.ms

        elif data.axes[0]==1:
            self.roll=rpylist[0]+0.2*self.ms
        elif data.axes[0]==-1:
            self.roll = rpylist[0]-0.2*self.ms
        elif data.axes[1]==1:
            self.pitch = rpylist[1]+0.2*self.ms
        elif data.axes[1]==-1:
            self.pitch = rpylist[1]-0.2*self.ms
        elif data.buttons[4]==1:
            self.yaw = rpylist[2]+0.2*self.ms
        elif data.buttons[6]==1:
            self.yaw = rpylist[2]-0.2*self.ms
        elif data.buttons[8]==1:
            self.ms+=1
        elif data.buttons[9]==1:
            self.ms-=1
        print("speed mode is :"+str(self.ms))
        pose_goal.position.y = self.y
        pose_goal.position.x = self.x
    
        pose_goal.position.z = self.z


        if self.yaw!=0 or self.pitch!=0 or self.roll!=0:
            quaternion = quaternion_from_euler(self.roll, self.pitch, self.yaw)
            pose_goal.orientation.x = quaternion[0]
            pose_goal.orientation.y = quaternion[1]
            pose_goal.orientation.z = quaternion[2]
            pose_goal.orientation.w = quaternion[3]

        #pose_goal.orientation.x = self.xx
        #pose_goal.orientation.y = self.yy
        #pose_goal.orientation.z = self.zz
        #pose_goal.orientation.w = self.ww
        print(str(self.x)+"+"+str(self.y)+"+"+str(self.z))
        print(group.get_current_rpy())
        group.set_pose_target(pose_goal)
        #plan = group.go(wait=True)
        plan = group.go()
        print('511')


        current_pose = self.group.get_current_pose().pose
        #return all_close(pose_goal, current_pose, 0.01)

    def go_to_pose_goal2(self):
        group = self.group

        #rpylist = [1.5473580717554953, -0.1037770361431429, -0.09370694102821339]
        rpylist=[1.7953519056985934, -0.21404165682755383, -2.1171445214112166]
        pose_goal = geometry_msgs.msg.Pose()

        quaternion = quaternion_from_euler(rpylist[0], rpylist[1], rpylist[2])
        #quaternion = quaternion_from_euler(self.roll, self.pitch, self.yaw)
        pose_goal.orientation.x = 0
        pose_goal.orientation.y = 0
        pose_goal.orientation.z = 0
        pose_goal.orientation.w = 0.99999

        pose_goal.position.x = 0.0282
        pose_goal.position.y = -0.033
        pose_goal.position.z = 0.5846

        group.set_pose_target(pose_goal)
        plan = group.go(wait=True)
        #plan = group.go(wait=True)
        # Calling `stop()` ensures that there is no residual movement

        print("time sleep 30")
        time.sleep(3)

        rpylist=[1.3527112565294774, 0.056359609476655796, -1.4608491470929768]
        pose_goal = geometry_msgs.msg.Pose()

        quaternion = quaternion_from_euler(rpylist[0], rpylist[1], rpylist[2])
        #quaternion = quaternion_from_euler(self.roll, self.pitch, self.yaw)
        pose_goal.orientation.x = 0
        pose_goal.orientation.y = 0
        pose_goal.orientation.z = 0
        pose_goal.orientation.w = 0.99999
    
        pose_goal.position.x = -0.031
        pose_goal.position.y = -0.2297
        pose_goal.position.z = 0.5194

        group.set_pose_target(pose_goal)
        plan = group.go(wait=True)
        time.sleep(2)    
        #plan = group.go(wait=True)

        rpylist=[1.3527112565294774, 0.056359609476655796, -1.4608491470929768]
        pose_goal = geometry_msgs.msg.Pose()

        quaternion = quaternion_from_euler(rpylist[0], rpylist[1], rpylist[2])
        #quaternion = quaternion_from_euler(self.roll, self.pitch, self.yaw)
        pose_goal.orientation.x = 0
        pose_goal.orientation.y = 0
        pose_goal.orientation.z = 0
        pose_goal.orientation.w = 0.99999

        pose_goal.position.x = -0.0917
        pose_goal.position.y = -0.3073
        pose_goal.position.z = 0.3701

        group.set_pose_target(pose_goal)
        plan = group.go(wait=True)
        time.sleep(2)
        #plan = group.go(wait=True)
        # Calling `stop()` ensures that there is no residual movement
  
        rpylist=[1.3527112565294774, 0.056359609476655796, -1.4608491470929768]
        pose_goal = geometry_msgs.msg.Pose()

        quaternion = quaternion_from_euler(rpylist[0], rpylist[1], rpylist[2])
        #quaternion = quaternion_from_euler(self.roll, self.pitch, self.yaw)
        pose_goal.orientation.x = 0
        pose_goal.orientation.y = 0
        pose_goal.orientation.z = 0
        pose_goal.orientation.w = 0.99999

        pose_goal.position.x = 0.2291
        pose_goal.position.y = 0.1166
        pose_goal.position.z = 0.2399

        group.set_pose_target(pose_goal)
        plan = group.go(wait=True)
        time.sleep(2)
        #plan = group.go(wait=True)
        # Calling `stop()` ensures that there is no residual movement

        rpylist=[1.3527112565294774, 0.056359609476655796, -1.4608491470929768]
        pose_goal = geometry_msgs.msg.Pose()

        quaternion = quaternion_from_euler(rpylist[0], rpylist[1], rpylist[2])
        #quaternion = quaternion_from_euler(self.roll, self.pitch, self.yaw)
        pose_goal.orientation.x = 0  
        pose_goal.orientation.y = 0 
        pose_goal.orientation.z = 0
        pose_goal.orientation.w = 0.9999999

        pose_goal.position.x = 0.2995
        pose_goal.position.y = -0.1071
        pose_goal.position.z = 0.3920

        group.set_pose_target(pose_goal)
        plan = group.go(wait=True)
        time.sleep(2)
        #plan = group.go(wait=True)
        # Calling `stop()` ensures that there is no residual movement

        rpylist=[1.353136448240024, 0.05670685433449488, -1.4607289026864196]
        pose_goal = geometry_msgs.msg.Pose()

        quaternion = quaternion_from_euler(rpylist[0], rpylist[1], rpylist[2])
        #quaternion = quaternion_from_euler(self.roll, self.pitch, self.yaw)
        pose_goal.orientation.x = 0
        pose_goal.orientation.y = 0
        pose_goal.orientation.z = 0
        pose_goal.orientation.w = 0.999999

        pose_goal.position.x = 0.2291
        pose_goal.position.y = 0.1166
        pose_goal.position.z = 0.2399

        group.set_pose_target(pose_goal)
        plan = group.go(wait=True)
        #plan = group.go(wait=True)
        # Calling `stop()` ensures that there is no residual movement
        time.sleep(2)

        rpylist=[1.8960701732477212e-05, 2.223636698306995e-05, 0.0001329310945526553]
        pose_goal = geometry_msgs.msg.Pose()

        quaternion = quaternion_from_euler(rpylist[0], rpylist[1], rpylist[2])
        #quaternion = quaternion_from_euler(self.roll, self.pitch, self.yaw)
        pose_goal.orientation.x = 0
        pose_goal.orientation.y = 0
        pose_goal.orientation.z = 0
        pose_goal.orientation.w = 0.999999

        pose_goal.position.x = 0
        pose_goal.position.y = -0.0001
        pose_goal.position.z = 0.6029

        group.set_pose_target(pose_goal)
        plan = group.go(wait=True)
        #plan = group.go(wait=True)
        # Calling `stop()` ensures that there is no residual movement

        group.stop()
        group.clear_pose_targets()

        current_pose = self.group.get_current_pose().pose
        return all_close(pose_goal, current_pose, 0.01)

    def plan_cartesian_path(self, scale=1):
        group = self.group

        waypoints = []

        wpose = group.get_current_pose().pose
        wpose.position.z -= scale * 0.1  # First move up (z)
        wpose.position.y += scale * 0.2  # and sideways (y)
        waypoints.append(copy.deepcopy(wpose))

        wpose.position.x += scale * 0.1  # Second move forward/backwards in (x)
        waypoints.append(copy.deepcopy(wpose))

        wpose.position.y -= scale * 0.1  # Third move sideways (y)
        waypoints.append(copy.deepcopy(wpose))

        (plan, fraction) = group.compute_cartesian_path(
                                       waypoints,   # waypoints to follow
                                       0.01,        # eef_step
                                       0.0)         # jump_threshold

    # Note: We are just planning, not asking move_group to actually move the robot yet:
        return plan, fraction

    def display_trajectory(self, plan):
        robot = self.robot
        display_trajectory_publisher = self.display_trajectory_publisher

        display_trajectory = moveit_msgs.msg.DisplayTrajectory()
        display_trajectory.trajectory_start = robot.get_current_state()
        display_trajectory.trajectory.append(plan)
        display_trajectory_publisher.publish(display_trajectory);

    def execute_plan(self, plan):
        group = self.group
        group.execute(plan, wait=True)

    def wait_for_state_update(self, box_is_known=False, box_is_attached=False, timeout=4):
        box_name = self.box_name
        scene = self.scene
        start = rospy.get_time()
        seconds = rospy.get_time()
        while (seconds - start < timeout) and not rospy.is_shutdown():
          # Test if the box is in attached objects
          attached_objects = scene.get_attached_objects([box_name])
          is_attached = len(attached_objects.keys()) > 0

        # Test if the box is in the scene.
        # Note that attaching the box will remove it from known_objects
        is_known = box_name in scene.get_known_object_names()

        # Test if we are in the expected state
        if (box_is_attached == is_attached) and (box_is_known == is_known):
            return True

        # Sleep so that we give other threads time on the processor
        rospy.sleep(0.01)
        seconds = rospy.get_time()

        # If we exited the while loop without returning then we timed out
        return False

    def add_box(self, timeout=4):
        box_name = self.box_name
        scene = self.scene

        box_pose = geometry_msgs.msg.PoseStamped()
        box_pose.header.frame_id = "panda_leftfinger"
        box_pose.pose.orientation.w = 1.0
        box_name = "box"
        scene.add_box(box_name, box_pose, size=(0.1, 0.1, 0.1))

        self.box_name=box_name
        return self.wait_for_state_update(box_is_known=True, timeout=timeout)


    def attach_box(self, timeout=4):
        box_name = self.box_name
        robot = self.robot
        scene = self.scene
        eef_link = self.eef_link
        group_names = self.group_names

        grasping_group = 'hand'
        touch_links = robot.get_link_names(group=grasping_group)
        scene.attach_box(eef_link, box_name, touch_links=touch_links)

        # We wait for the planning scene to update.
        return self.wait_for_state_update(box_is_attached=True, box_is_known=False, timeout=timeout)

    def detach_box(self, timeout=4):
        # Copy class variables to local variables to make the web tutorials more clear.
        # In practice, you should use the class variables directly unless you have a good
        # reason not to.
        box_name = self.box_name
        scene = self.scene
        eef_link = self.eef_link

        scene.remove_attached_object(eef_link, name=box_name)

        return self.wait_for_state_update(box_is_known=True, box_is_attached=False, timeout=timeout)

    def remove_box(self, timeout=4):
        box_name = self.box_name
        scene = self.scene

        scene.remove_world_object(box_name)

        # We wait for the planning scene to update.
        return self.wait_for_state_update(box_is_attached=False, box_is_known=False, timeout=timeout)


def main():
    try:
        print("============ Press `Enter` to begin the tutorial by setting up the moveit_commander (press ctrl-d to exit) ...")
        tutorial = MoveGroupPythonIntefaceTutorial()



        tutorial.go_to_pose_goal2()
        #tutorial.listener()

        time.sleep(1)

    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
  #main()
    while True:
        main()

