#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>

//  SCHED_NORMAL	0
//  SCHED_FIFO		1
//  SCHED_RR		2
//  SCHED_BATCH		3
#define  SCHED_IDLE		5
//  SCHED_DEADLINE	6
#define SCHED_LOW_IDLE 7

char *buffer;
int tam_buffer;
int num_threads;
int posicao = 0;
sem_t semaforo_buffer;
// int *thread_schedule_count;

void* add_buffer(void* args){
	
	char letraThread = *((char*)args);
	while(1){

		sem_wait(&semaforo_buffer);
		
		if(posicao >= tam_buffer){
			sem_post(&semaforo_buffer);
			break;
		}

		buffer[posicao] = letraThread;
		printf("%c\n", letraThread);
		posicao++;

		sem_post(&semaforo_buffer);
	}
	return NULL;
}


void print_sched(int policy)
{
	int priority_min, priority_max;

	switch(policy){
		case SCHED_LOW_IDLE://7
			printf("SCHED_LOW_IDLE");
			break;
		case SCHED_FIFO://1
			printf("SCHED_FIFO");
			break;
		case SCHED_RR://2
			printf("SCHED_RR");
			break;
		case SCHED_IDLE://5
			printf("SCHED_IDLE");
			break;
		default:
			printf("unknown\n");
	}
	priority_min = sched_get_priority_min(policy);
	priority_max = sched_get_priority_max(policy);
	printf(" PRI_MIN: %d PRI_MAX: %d\n\n", priority_min, priority_max);
}



//  SCHED_NORMAL	0
//  SCHED_FIFO		1
//  SCHED_RR		2
//  SCHED_BATCH		3
//  SCHED_IDLE		5
//  SCHED_DEADLINE	6
int setpriority(pthread_t *thr, int newpolicy, int newpriority)
{
	int policy, ret;
	struct sched_param param;

	if (newpriority > sched_get_priority_max(newpolicy) || newpriority < sched_get_priority_min(newpolicy)){
		printf("Invalid priority: MIN: %d, MAX: %d", sched_get_priority_min(newpolicy), sched_get_priority_max(newpolicy));

		return -1;
	}

	pthread_getschedparam(*thr, &policy, &param);
	printf("current: ");
	print_sched(policy);

	param.sched_priority = newpriority;
	ret = pthread_setschedparam(*thr, newpolicy, &param);
	if (ret != 0)
		perror("perror(): ");

	pthread_getschedparam(*thr, &policy, &param);
	printf("new: ");
	print_sched(policy);

	return 0;
}

int main(int argc, char** argv){
	if(argc < 4){
		printf("Error: usage = ./sched_profiler <tamanho_buffer> <num_threads> <policy>\n\n");
		return -1;
	}

	tam_buffer = atoi(argv[1]);
	num_threads = atoi(argv[2]);
	int policy = atoi(argv[3]);

	buffer = (char*)malloc(tam_buffer * sizeof(char));

	char letras[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'};
	pthread_t threads[num_threads];

	sem_init(&semaforo_buffer, 0, 1);


	for(int i = 0; i<num_threads; i++){
		pthread_create(&threads[i], NULL, add_buffer, &letras[i]);
		setpriority(&threads[i], policy, 0);
	}

	for(int i = 0; i<num_threads; i++){
		pthread_join(threads[i], NULL);
	}

	printf("\nfinalizou\n");
	
	free(buffer);
	sem_destroy(&semaforo_buffer);
	return 0;
}
