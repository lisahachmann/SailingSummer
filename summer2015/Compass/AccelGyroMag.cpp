/*
Provided to you by Emlid Ltd (c) 2014.
twitter.com/emlidtech || www.emlid.com || info@emlid.com

Example: Read accelerometer, gyroscope and magnetometer values from
MPU9250 inertial measurement unit over SPI on Raspberry Pi + Navio.

Navio's onboard MPU9250 is connected to the SPI bus on Raspberry Pi
and can be read through /dev/spidev0.1

To run this example navigate to the directory containing it and run following commands:
make
./AccelGyroMag
*/

#include <math.h>
//#include <time.h>
#include "Navio/C++/Navio/MPU9250.h"

#define PI 3.14159265

//=============================================================================

int main()
{
	//-------------------------------------------------------------------------

	MPU9250 imu;
	imu.initialize();
/* test code
	if(imu.testConnection()){
	printf("true");
	}
	else{
	printf("false");
	}*/

	float ax, ay, az, gx, gy, gz, mx, my, mz, pitch, roll, realX, realY, heading, cx, cy, cz;
//	FILE * pFile;
//	pFile = fopen("AGMOUTPUT.txt","w");
    //-------------------------------------------------------------------------

        imu.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);
	//WEIRDASS AXES - SEE DATASHEET
	//	cx = gy;
	//	cy = gx;
	//	cz = -gz;
	//adjust for tilt
	//pitch = cy * (PI / 180);
	//roll = cx * (PI / 180);

	//realX =  cx*cos(pitch) + cz*sin(pitch);
	//realY =  cx*sin(roll)*sin(pitch) + cy*cos(roll) - cz*sin(roll)*sin(pitch);

	//Calculate heading
	//heading = (180 / PI) * atan2(realY, realX);
	//printf("Heading: %+07.3f", heading);
/*
	// print to file
//	fprintf(pFile,"Heading: %+07.3f\n", heading);
//	fprintf(pFile,"Acc: %+07.3f %+07.3f %+07.3f ",  ax, ay, az);
	fprintf(pFile,"Gyr: %+07.3f %+07.3f %+07.3f",  gx, gy, gz);
	fprintf(pFile,"Mag: %+07.3f %+07.3f %+07.3f\n",  mx, my, mz);
	fflush(pFile);
*/
	//Nice Pretty Terminal output/
	printf("Acc: %+07.3f %07.3f %+07.3f ", ax, ay, az);
	printf("Gyr: %+07.3f %+07.3f %+07.3f ", gx, gy, gz);
	printf("Mag: %+07.3f %+07.3f %+07.3f\n", mx, my, mz);
	fflush(stdout);
}
