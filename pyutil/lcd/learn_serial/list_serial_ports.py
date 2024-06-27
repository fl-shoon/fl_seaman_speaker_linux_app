from subprocess import run

def run_main():
    import serial.tools.list_ports # type: ignore
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    print (myports)

try:
    import serial.tools.list_ports # type: ignore
except ModuleNotFoundError:
    run(f"sudo python -m pip install pyserial --break-system-packages", shell=True)
finally:
    run_main()