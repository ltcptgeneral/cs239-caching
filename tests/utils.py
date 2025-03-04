def print_report(hits, request_times, real_time):

    hits_count = sum(hits)
    miss_count = len(hits) - hits_count

    hits_time = 0
    miss_time = 0
    for i in range(len(request_times)):
        if hits[i]:
            hits_time += request_times[i]
        else:
            miss_time += request_times[i]
    total_time = hits_time + miss_time

    print(f"hits: {hits_count} misses: {miss_count} ratio: { hits_count / (hits_count + miss_count)}")
    print(f"average response time (ms)           : {total_time / len(request_times)}")
    if hits_count > 0:
        print(f"average cache hit response time (ms) : {hits_time / hits_count}")
    else :
        print(f"average cache hit response time (ms) : N/A")
    if miss_count > 0:
        print(f"average cache miss response time (ms): {miss_time / miss_count}")
    else:
        print(f"average cache miss response time (ms): N/A")
    print(f"cache throughput (requests / s)      : { len(request_times) / total_time * 1000}")
    print(f"real throughput  (requests / s)      : { len(request_times) / (real_time)}")