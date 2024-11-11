BUILDROOT_DIR := ../..
COMPILER := $(BUILDROOT_DIR)/output/host/bin/i686-buildroot-linux-gnu-gcc

all:
	$(COMPILER) -o sched_profiler sched_profiler.c -lpthread -Wall

clean:
	rm sched_profiler
