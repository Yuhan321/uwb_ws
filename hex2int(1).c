#include <stdio.h>

int main()
{
   char data[]="mc 00 00000663 000005a3 00000512 000004cb 095f c1 0 a0:0\r\n";

    int aid, tid, range[4], lnum, seq, user;
	int rangetime;
	char c, type;
	int n = sscanf(data,"m%c %x %x %x %x %x %x %x %x %c%d:%d", &type, &user, &range[0], &range[1], &range[2], &range[3], &lnum, &seq, &rangetime, &c, &tid, &aid);
	printf("user=0x%02x\nrange[0]=%d(mm)\nrange[1]=%d(mm)\nrange[2]=%d(mm)\nrange[3]=%d(mm)\r\n",user,range[0], range[1], range[2], range[3]);
  
   return 0;
}