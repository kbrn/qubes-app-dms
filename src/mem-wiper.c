#include <malloc.h>
#include <string.h>
//Try malloc'ing 1GB segments, then writing NULs to them, until malloc fails, then reducing size until success, and repeating
//FIXME: Ideally one would turn off vm overcommit in Dom0 first...

int main(){
	unsigned int chunk_size = 1024*1024*1024;

	while(1){
		char *chunk = (char*) malloc(chunk_size);
		if(chunk == NULL){
			//then we're (almost) all out of memory; die if at quantum
			if(chunk_size == 4096){
				return 0;
			}
			else{
				chunk_size /= 2;
				continue;
			}
		}


		memset(chunk, '\0', chunk_size); //actually write to the memory
		//FIXME ensure this call isn't optimized away
	}
}
