from time import perf_counter_ns

start = perf_counter_ns()
import main_routine
stop = perf_counter_ns()
print("current runtime [ms]: ", (stop-start)/(10**6))