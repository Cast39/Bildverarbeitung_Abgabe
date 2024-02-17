from time import perf_counter_ns

start = perf_counter_ns()
import threaded_main_routine
stop = perf_counter_ns()
print("current runtime [ms]: ", (stop-start)/(10**6))
print("for 1000 if 100 in-images [min]: ", (stop-start)/(60*(10**8)))

###runs
# [17.02.2024]02:00 :  15 sek / 100 Bilder - old main_routine
# [17.02.2024]03:00 :  7,774 sek / 100 Bilder - first threaded(8) run (16core system)
# [17.02.2024]03:00 :  8,714 sek / 100 Bilder - try threaded(16) (16core system)
# [17.02.2024]03:00 :  8,426 sek / 100 Bilder - try threaded(12) (16core system)
# [17.02.2024]03:00 :  7,358 sek / 100 Bilder - try threaded(6) (16core system)
# [17.02.2024]03:00 :  6,748 sek / 100 Bilder - try threaded(4) (16core system) <- sweetspot
# [17.02.2024]03:00 :  7,834 sek / 100 Bilder - try threaded(2) (16core system)
# [17.02.2024]03:00 :  49,335 sek / 1000 Bilder - try threaded(4) (16core system)