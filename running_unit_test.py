import running as r
import math

#get_second unit test
second_test1 = r.get_seconds(0)
second_test2 = r.get_seconds(60)
if second_test1 == 1500 and second_test2 == 500:
    print('get_seconds functioning correctly')
else:
    print(f'get_seconds failed answer: {second_test1}, {second_test2}')
