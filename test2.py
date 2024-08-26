import requests
import matplotlib.pyplot as plt
from datetime import datetime
import time
from collections import deque

MAX_SAMPLES = 30

timestamps = deque(maxlen=MAX_SAMPLES)
execution_times = deque(maxlen=MAX_SAMPLES)

def test_api():
    try:
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            return response.elapsed.total_seconds() * 1000
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def update_graph(x_data, y_data, avg_ping):
    plt.clf()
    plt.plot(x_data, y_data, marker='o', linestyle='-', color='b', label='Ping (ms)')
    plt.axhline(y=avg_ping, color='r', linestyle='--', label=f'Average Ping: {avg_ping:.2f} ms')
    plt.xlabel('Time')
    plt.ylabel('Execution Time (ms)')
    plt.title('API Response Time')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.draw()
    plt.pause(1)

def calculate_average_ping(execution_times):
    if len(execution_times) > 0:
        return sum(execution_times) / len(execution_times)
    else:
        return 0

if __name__ == "__main__":
    plt.ion()
    plt.figure(figsize=(10, 6))

    while True:
        start_time = time.time()
        execution_time = test_api()
        end_time = time.time()

        if execution_time is not None:
            timestamp = datetime.now().strftime('%H:%M:%S')
            timestamps.append(timestamp)
            execution_times.append(execution_time)
            avg_ping = calculate_average_ping(execution_times)
            update_graph(timestamps, execution_times, avg_ping)

        time.sleep(0.1)

    plt.ioff()
    plt.show()
