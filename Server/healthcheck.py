import psutil as hc
from sys import platform
from datetime import date
import datetime
import time
import socket
import os


def sec2hour(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return f"{hh}:{mm}:{ss}"


output = []

# CPU info
def CPU_INFO(
    cpu_count=True, cpu_percentage=True, cpu_freq=True, cpu_interval=1, cpu_stat=False
):
    """
    CPU Information:
    Gives the output in a list of CPU information.
    All Boolean values
    """
    if cpu_count is True:
        output.append("cpu count: {}".format(hc.cpu_count()))
    if cpu_percentage is True:
        output.append("cpu percentage: {}%".format(hc.cpu_percent(cpu_interval)))
    if cpu_freq is True:
        output.append("cpu frequency: {} Mhz".format(hc.cpu_freq()[0]))
    if cpu_stat is True:
        output.append("cpu stats: {}".format(hc.cpu_stats()))


def MEM_INFO(
    mem_tot=True, mem_avail=True, mem_per_used=True, mem_used=True, out_in="GB"
):

    # Mem info
    all_mem = hc.virtual_memory()
    if out_in == "GB":
        if mem_tot is True:
            output.append("Total Memory: {} GB".format(all_mem[0] >> 30))
        if mem_avail is True:
            output.append("Memory Available: {} GB".format(all_mem[1] >> 30))
        if mem_per_used is True:
            output.append("Memory Used in %: {} %".format(all_mem[2]))
        if mem_used is True:
            output.append("Memory Used: {} GB".format(all_mem[3] >> 30))
    elif out_in == "MB":
        if mem_tot is True:
            output.append("Total Memory: {} GB".format(all_mem[0] >> 20))
        if mem_avail is True:
            output.append("Memory Available: {} GB".format(all_mem[1] >> 20))
        if mem_per_used is True:
            output.append("Memory Used in %: {} %".format(all_mem[2]))
        if mem_used is True:
            output.append("Memory Used: {} GB".format(all_mem[3] >> 20))


def DISK_INFO():
    for part in hc.disk_partitions(all=True):
        usage = hc.disk_usage(part.mountpoint)
        output.append(f'Disk: {part.mountpoint}')
        output.append(f'Total: {usage.total >> 30}GB')
        output.append(f'Used: {usage.used >> 30}GB')
        output.append(f'Free: {usage.free >> 30}GB')
        output.append(f'Percentage: {usage.percent}%')
        print(part.fstype)

def DIR_INFO():

    for dirpath, dirnames, filenames, in os.walk('/'):
        total_size = 0

        for path in dirnames:
            try:
                full_path = os.path.join(dirpath, path)
                full_size = os.path.getsize(os.path.join(dirpath, path))

                total_size += os.path.getsize(os.path.join(dirpath, path))
            except Exception as ex:
                print(ex)
        output.append(f'Total Size of path {os.path.join(dirpath, path)}: {total_size}')


def NETWORK_STAT(net_bytes=True, net_connections=False, net_nic=True):
    # Network

    if net_bytes is True:
        net_stat = hc.net_io_counters()

        output.append(f"Bytes Sent: {net_stat[0] >> 20}Mb")
        output.append(f"Bytes Received: {net_stat[1] >> 20}Mb")
        output.append(f"Packets Sent: {net_stat[2]}")
        output.append(f"Packets Received: {net_stat[3]}")

    if net_connections is True:
        connections = hc.net_connections()
        for conn in connections:

            if conn[4]:

                ip, port = conn[4]
                try:
                    host = socket.gethostbyaddr(ip)[0]
                except Exception as ex:
                    host = ip + " No host found"

                output.append(f"Host: {host}")
                output.append(f"        IP: {ip}")
                output.append(f"        Port: {port}")
                output.append(f"        Status: {conn[5]}")
                if conn[6]:
                    process = hc.Process(conn[6])
                    process_name = process.name()
                    output.append(f"        Process: {process_name}")

    if net_nic is True:
        net_stats = hc.net_if_stats()

        # output.append(net_stats)
        for key, value in net_stats.items():

            output.append(f"NIC {key} isup: {value[0]}")
            if value[0] is True:
                output.append(f"NIC {key} duplex: {value[1]}")
                output.append(f"NIC {key} speed: {value[2]}MB")


def SENSORS(
    battery=True, temperature=True, uptime=True, user_info=True, process_info=False
):

    if temperature is True:
        # Sensors
        if platform == "linux":
            try:
                temp = hc.sensors_temperatures(fahrenheit=False)
                output.append(temp)
            except Exception as ex:
                output.append(ex)

    if battery is True:
        try:
            battery = hc.sensors_battery()
            output.append(f"Percent left: {battery[0]}%")
            output.append(f"Power Supply: {battery[2]}")
        except Exception as ex:
            output.append(ex)
        try:
            if not battery[2]:
                try:
                    time_left = sec2hour(battery[1])
                    output.append(f"Time left: {time_left}")
                except Exception as ex:
                    output.append(ex)
        except Exception as ex:
            output.append(ex)

    if uptime is True:
        # Boot time
        try:
            fmt = "%Y-%m-%d %H:%M:%S"
            boot = hc.boot_time()
            time_now = datetime.datetime.now().timestamp()
            days = "%d"
            delta = time_now - boot
            delta_days = int(datetime.datetime.fromtimestamp(delta).strftime(days))
            output.append(f"Uptime: {delta_days} day(s)")
        except Exception as ex:
            output.append(ex)

    if user_info is True:
        # users
        try:
            users = hc.users()
        except Exception as ex:
            output.append(ex)

        try:
            for user in users:
                output.append(f"Username: {user[0]}")
                output.append(f"Terminal: {user[1]}")
                output.append(f"Host: {user[2]}")
                fmt = "%Y-%m-%d %H:%M:%S"
                login_time = datetime.datetime.fromtimestamp(user[3]).strftime(fmt)
                output.append(f"Login time: {login_time}")
                output.append(f"PID: {user[4]}")
        except Exception as ex:
            output.append(ex)

    if process_info is True:
        # process
        for proc in hc.process_iter():
            # print(proc.connections())
            try:
                output.append(f"Processname: {proc.name()}")
                output.append(f"    PID: {proc._pid}")
                output.append(
                    f"    CPU: {proc.cpu_percent(interval=1)/ hc.cpu_count():.2f}%"
                )
                output.append(f"    Memory: {proc.memory_percent():.2f} %")
                if proc.connections():
                    connections = proc.connections()
                    for conn in connections:
                        if conn[4]:
                            ip, port = conn[4]
                            output.append(f"    Connection IP: {ip}")
                            output.append(f"    Connection Port: {port}")
            except Exception as ex:
                output.append(ex)

def clear_output():
    output.clear()

def get_health_check():
    clear_output()
    output.append('HEALTH CHECK')
    CPU_INFO()
    MEM_INFO()
    DISK_INFO()
    NETWORK_STAT()
    SENSORS()
    return output


def get_cpu_info():
    clear_output()
    output.append('CPU INFO')
    CPU_INFO(cpu_stat=True)
    return output


def get_mem_info():
    clear_output()
    output.append('MEM INFO')
    MEM_INFO()
    return output


def get_disk_info():
    clear_output()
    output.append('DISK INFO')
    DISK_INFO()
    return output


def get_network_info():
    clear_output()
    output.append('NETWORK INFO')
    NETWORK_STAT()
    return output


def get_connections():
    clear_output()
    output.append('CONNECTIONS')
    NETWORK_STAT(net_bytes=False, net_connections=True, net_nic=False)
    return output


def get_sensor_info():
    clear_output()
    output.append('SENSER INFO')
    SENSORS()
    return output


def get_processes():
    clear_output()
    output.append('PROCESSES')
    SENSORS(
        battery=False,
        temperature=False,
        uptime=False,
        user_info=False,
        process_info=True,
    )

    return output

def get_dir_info():
    clear_output()
    DIR_INFO()
    output.append('DIR INFO')
    return output

if __name__ == "__main__":
    print(get_dir_info())
# for out in output:
#     print(out)
