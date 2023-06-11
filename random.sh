#!/bin/sh
# Generate random points

SEED=5207364
NUM=100
# generate random points in a unit square
gawk 'BEGIN {
	srand('${SEED}');
	for (i = 0; i < '${NUM}'; ++i)
		print rand(), rand(), i;
}' > randsq.dat
NUM=100
# generate random points on the circumference of a unit circle
gawk 'BEGIN {
	srand('${SEED}');
	for (i = 0; i < '${NUM}'; ++i) {
	    	phi = rand()*2*atan2(0, -1);
		print cos(phi), sin(phi), i;
	}
}' > randcirc.dat

