"""Couple of useful utility scripts for working with embedded things."""
from subprocess import check_output

def get_mcu():
    """Gets the MCU name. Assumes that we have mbed cli installed and a board
    attached."""
    res = check_output(['mbed', 'detect'])
    res = [x.decode('ascii') for x in res.split()]
    try:
        idx = res.index('Detected')
        return res[idx + 1].strip().replace('"', '')
    except ValueError:
        raise RuntimeError("Couldn't find attached MCU board through mbed cli")
    except IndexError:
        raise RuntimeError("Couldn't find attached MCU board through mbed cli")


if __name__ == '__main__':
    print(get_mcu())
