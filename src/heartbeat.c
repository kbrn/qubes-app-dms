#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/select.h>

int main(void)
{
    char buf[1024] = {0};
    int len = 1023;
    int fd = 0;

    fd = open("/proc/self/fd/0", O_RDONLY);

    while(1){
        fd_set set;
        struct timeval timeout;
        int rv;
        int bytesread = 0;
        timeout.tv_sec = 0;
        timeout.tv_usec = 1000000;
        FD_ZERO(&set);
        FD_SET(fd, &set);

        rv = select(fd + 1, &set, NULL, NULL, &timeout);
        if(rv == -1){
            perror("select");
        }
        else if(rv == 0){
            printf("timeout\n");
        }
        else{
            bytesread = read(fd, buf, len);
            buf[1023] = '\0';
            printf("%s", buf);
            if(bytesread <= 0){
                break;
            }
        }
        fflush(NULL);
    }
}
