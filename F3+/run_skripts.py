import subprocess
import time


scripts = ["script1.py", "script2.py", "script3.py"]

# Запускаем скрипты последовательно
total_start_time = time.time()
for script in scripts:
    print(f"Executing {script}...")
    start_time = time.time()
    subprocess.run(["python3", script])
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{script} executed in {elapsed_time} seconds\n")

total_end_time = time.time()
total_elapsed_time = total_end_time - total_start_time
print(f"Total execution time: {total_elapsed_time} seconds")
