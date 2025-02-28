import psutil
import platform
import shutil
import os

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

def get_disk_usage():
    total, used, free = shutil.disk_usage("/")
    return {
        "total": round(total / (1024 ** 3), 2),
        "used": round(used / (1024 ** 3), 2),
        "free": round(free / (1024 ** 3), 2),
        "percent_used": round((used / total) * 100, 2)
    }

def get_battery_status():
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery:
            return {
                "percentage": battery.percent,
                "plugged_in": battery.power_plugged
            }
    return None

def get_system_temperature():
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            return temps["coretemp"][0].current  # Temperature in Celsius
    return None

def get_system_info():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "processor": platform.processor(),
        "architecture": platform.architecture()[0]
    }

def display_health_report():
    print("🔍 System Health Report\n")
    
    system_info = get_system_info()
    print(f"🖥 OS: {system_info['os']} {system_info['os_version']}")
    print(f"🔧 Processor: {system_info['processor']}")
    print(f"🏗 Architecture: {system_info['architecture']}\n")

    print(f"⚙ CPU Usage: {get_cpu_usage()}%")
    print(f"💾 Memory Usage: {get_memory_usage()}%")

    disk_usage = get_disk_usage()
    print(f"📂 Disk Usage: {disk_usage['used']} GB used out of {disk_usage['total']} GB ({disk_usage['percent_used']}%)")

    battery_status = get_battery_status()
    if battery_status:
        print(f"🔋 Battery: {battery_status['percentage']}% {'(Plugged In)' if battery_status['plugged_in'] else '(Not Charging)'}")
    else:
        print("🔋 Battery: Not available")

    temp = get_system_temperature()
    if temp:
        print(f"🌡 Temperature: {temp}°C")
    else:
        print("🌡 Temperature: Not available")

    print("\n✅ Health check completed!")

if __name__ == "__main__":
    display_health_report()
