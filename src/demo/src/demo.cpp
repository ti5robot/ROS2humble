#include <rclcpp/rclcpp.hpp>
#include <iostream>
#include <std_msgs/msg/string.hpp>
#include <moveit_msgs/msg/display_trajectory.hpp>
#include <iostream>
#include <cstdint>
#include "controlcan.h"

double next_position[6] = {0};
double ori_position[6] = {0};
int now_position[6] = {0};

using std::placeholders::_1;


double findMax(double arr[], int size) 
{
	double max = abs(arr[0]); 
	
	for (int i = 1; i < size-2; i++) 
	{
		if (abs(arr[i]) > abs(max))  
			max = abs(arr[i]); 
        }	
	return max;
}

bool init_can()
{
	VCI_BOARD_INFO pInfo, pInfo1[50];
    	
	int nDeviceType = 4;
	int nDeviceInd =0;
	int nCANInd = 0;


    	DWORD dwRel;
    	VCI_INIT_CONFIG vic;
    	dwRel = VCI_OpenDevice(nDeviceType, nDeviceInd, 0);
    	if (dwRel != 1)
	{
		std::cout << "open-fail:" << dwRel << std::endl;
		return FALSE;
    	}
    	else
		std::cout << "open success:1";

    	vic.AccCode = 0x80000008;
    	vic.AccMask = 0xFFFFFFFF;
    	vic.Filter = 1;
    	vic.Timing0 = 0x00;
    	vic.Timing1 = 0x14;
    	vic.Mode = 0;
    	
	dwRel = VCI_InitCAN(nDeviceType, nDeviceInd, nCANInd, &vic);
    	if (dwRel != 1)
    	{
       
		std::cout << "init-fail:" << dwRel << std::endl;
        	VCI_CloseDevice(nDeviceType, nDeviceInd);
        	return FALSE;
    	}
    	else
		std::cout << "initsuccess:" << dwRel << std::endl;

    	if (VCI_StartCAN(VCI_USBCAN2, 0, 0) != 1)
    	{
        	std::cout << "start-fail:" << dwRel << std::endl;
        	VCI_CloseDevice(VCI_USBCAN2, 0);
        	return FALSE;
    	}
    	else
		std::cout << "startsuccess:1" << std::endl;
	
	return true;
	
}


int32_t convertHexArrayToDecimal(const std::uint8_t hexArray[4])
{
	std::int32_t result=0;
	for(int i=0;i<4;i++)
		result=(result << 8) | hexArray[i];
	if(result>0x7FFFFFFF)
		result -= 0x100000000;

	return result;
}


void toIntArray(int number, int *res, int size)
{
	unsigned int unsignedNumber = static_cast<unsigned int>(number);
	
	for (int i = 0; i < size; ++i)
	{
		res[i] = unsignedNumber & 0xFF; 
		unsignedNumber >>= 8;           
	}
}


int32_t sendSimpleCanCommand(uint8_t numOfActuator, uint8_t *canIdList, uint8_t *commandList)
{
	VCI_CAN_OBJ send[1];
    	send[0].SendType = 0;
    	send[0].RemoteFlag = 0;
    	send[0].ExternFlag = 0;
    	send[0].DataLen = 1;
 	
    	for (int i = 0; i < numOfActuator; i++)
	{
		send[0].ID=canIdList[i];
		send[0].Data[0] = commandList[i];

        	if (VCI_Transmit(VCI_USBCAN2, 0, 0, send, 1) == 1)
        	{
            		VCI_CAN_OBJ rec[3000];
            		int ind = 0,reclen=0,cnt=2;

            		while((reclen = VCI_Receive(VCI_USBCAN2, 0, ind, rec, 3000, 100)) <= 0 && cnt)  cnt--;
			if(cnt==0) std::cout<<"ops! ID "<<send[0].ID<<" failed after try 2 times"<<std::endl;
			else
			{
				for (int j = 0; j < reclen; j++)
                		{
					std::uint8_t hexArray[4] = {rec[j].Data[4], rec[j].Data[3], rec[j].Data[2], rec[j].Data[1]};
                    			std::int32_t decimal = convertHexArrayToDecimal(hexArray);
			                std::cout << "ID: " << send[0].ID<<"   data: "<<decimal << std::endl;
				}
			}
		}
		else
			break;
	}
}



void sendCanCommand(uint8_t numOfActuator, uint8_t *canIdList, uint8_t *commandList, uint32_t *parameterList)
{
    	VCI_CAN_OBJ send[1];
    	send[0].SendType = 0;
    	send[0].RemoteFlag = 0;
    	send[0].ExternFlag = 0;
    	send[0].DataLen = 5;
	int num=0;
	for (int i = 0; i < numOfActuator; i++)
    	{
		std::cout<<"i i i i:  "<<i<<"   num num num:  "<< num++ <<"   numOfActuator:  "<<numOfActuator<<"   zxzx"<<std::endl;
		send[0].ID = canIdList[i];
		std::cout<<"ID ID ID ID ID:  "<<send[0].ID<<std::endl;
		send[0].Data[0] = commandList[i]; 
        	int res[4],cnt=2,reclen=0;
        	toIntArray(parameterList[i], res, 4);

		for (int j = 1; j < 5; j++)
			send[0].Data[j] = res[j - 1];

		while(reclen = VCI_Transmit(VCI_USBCAN2,0,0,send,1) <= 0 && cnt) cnt--;
		if(cnt == 0) std::cout<<"ops! ID: "<<send[0].ID<<" failed after try 2 times."<<std::endl;
		else
		{
			std::cout<<"ID:  "<<send[0].ID<<std::endl;
			for(int c=0;c<send[0].DataLen;c++)
				//printf("");
				printf("   %02X",send[0].Data[c]);
			std::cout<<std::endl;
		}
	}
}




class Listener : public rclcpp::Node
{
public:
	Listener(std::string name) : Node(name)
	{
		// rclcpp::Subscriber client_sub = nh.subscribe("/move_group/display_planned_path", 1000, &Listener::callback, &listener);
		subscription_ = this->create_subscription<moveit_msgs::msg::DisplayTrajectory>(
				"display_planned_path",1000,std::bind(&Listener::callback,this,std::placeholders::_1));
	}
	void callback(const moveit_msgs::msg::DisplayTrajectory::ConstPtr &msg)
	{        
		uint8_t canidlist[10]={1,2,3,4,5,6};
		uint8_t cmd_pos[10]={30,30,30,30,30,30},cmd_v_p[10]={36,36,36,36,36,36},cmd_v_n[10]={37,37,37,37,37,37};
		uint32_t para_v_p[10],para_v_n[10],para_pos[10];
		
		int n = msg->trajectory[0].joint_trajectory.points.size();
		double cn[6];
        
		int tmp0=100,tmp1=-100;
	
		for(int i=0;i<6;i++)
		{
			para_v_p[i]=tmp0;
			para_v_n[i]=tmp1;
		}
		sendCanCommand(6,canidlist,cmd_v_p,para_v_p);
		usleep(100);
		sendCanCommand(6,canidlist,cmd_v_n,para_v_n);
		usleep(100);

		for(int i=0;i<6;i++)
		{
			ori_position[i] = msg->trajectory[0].joint_trajectory.points[0].positions[i]*57.3;
			next_position[i] = msg->trajectory[0].joint_trajectory.points[n-1].positions[i] *57.3;
			now_position[i] = (msg->trajectory[0].joint_trajectory.points[n-1].positions[i]) *57.3*101*65536/360;
			cn[i] = next_position[i] - ori_position[i];
			para_pos[i] = static_cast<uint32_t>(now_position[i]);
	       	}
	
		double maxVal = findMax(cn, 6);
		std::cout<<"~~~~~~"<<maxVal<<std::endl;
		double periodTime =maxVal/100;
		double status=1;
		if (0.3<periodTime<0.5)
	 		periodTime *=2;
		else if(0.001<periodTime<0.3)
			periodTime *=3;
		std::cout<<"TTTTTTT"<<periodTime<<std::endl;

		int maxSpeed[6];
		for(int i=0;i<6;i++)
			maxSpeed[i]=abs((cn[i]/periodTime)*10100/360);
		std::cout<<"##"<<maxSpeed[0]<<"##"<<maxSpeed[1]<<"##"<<maxSpeed[2]<<"##"<<maxSpeed[3]<<"##"<<maxSpeed[4]<<std::endl;

		sendCanCommand(6, canidlist, cmd_pos, para_pos);


		for (int j=5; j<105; j++)
		{
			double acceleration_ratio = (j - 5) / 100.0;

			for(int i=0;i<6;i++)
			{
				para_v_p[i] = acceleration_ratio * maxSpeed[i];
				para_v_n[i] = -1 * para_v_p[i];
			}

			sendCanCommand(6,canidlist,cmd_v_p,para_v_p);
			usleep(10);
			sendCanCommand(6,canidlist,cmd_v_n,para_v_n);
			usleep(10);
			usleep(5000 * status);
		}
	
		if(periodTime >= 0.55)
			usleep(periodTime*1000000-550000*status);
	
		for (int j = 105; j > 5; j--)
		{
			double deceleration_ratio = (105 - j) / 100.0;
			for(int i=0;i<6;i++)
			{
				para_v_p[i] = j * maxSpeed[i] / 100;
				para_v_n[i] = -1 * para_v_p[i];
			}
	
			sendCanCommand(6,canidlist,cmd_v_p,para_v_p);
			usleep(10);
			sendCanCommand(6,canidlist,cmd_v_n,para_v_n);
			usleep(10);
			usleep(5000 * status * deceleration_ratio);
		}
		std::cout<<"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"<<std::endl;
	}
private:
	rclcpp::Subscription<moveit_msgs::msg::DisplayTrajectory>::SharedPtr subscription_;
    
};



void move_up()
{
	int tmp0=500,tmp1=-500;
	uint32_t para_v_p[10]={tmp0,tmp0,tmp0,tmp0,tmp0,tmp0},para_v_n[10]={tmp1,tmp1,tmp1,tmp1,tmp1,tmp1};
	uint8_t canidlist[6]={1,2,3,4,5,6};
	uint8_t cmd_v_p[6]={36,36,36,36,36,36},cmd_v_n[6]={37,37,37,37,37,37},cmd_pos[6]={30,30,30,30,30,30};
	
	sendCanCommand(6,canidlist,cmd_v_p,para_v_p);
	usleep(50);
	sendCanCommand(6,canidlist,cmd_v_n,para_v_n);
	usleep(50);

	uint32_t para_pos[10]={0,0,0,0,0,0};
	sendCanCommand(6,canidlist,cmd_pos,para_pos);

	usleep(5000);
}


int main(int argc, char **argv)
{
	rclcpp::init(argc, argv);
	auto node = std::make_shared<Listener>("listener");
    	rclcpp::Rate loop_rate(500);
	//rclcpp::Rate loop_rate_slow(2);

    	init_can(); 
	move_up();
	
	while (rclcpp::ok())
	{
        	rclcpp::spin(node);
        	loop_rate.sleep();
        	//uint8_t canidlist[10]={1,2,3,4,5,6},cmd[10]={8,8,8,8,8,8};
        	//sendSimpleCanCommand(6,canidlist,cmd);
	}
    	return 0;
}
