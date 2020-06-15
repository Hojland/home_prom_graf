from src import microbit
import time


offset = 580


def read():
    read = float(microbit.cmd('print(pin2.read_analog())'))
    return max(0, read - offset)


def read_loudest(read_span: int, read_time: int):
    start_time = running_time()
    loudest_read = 0
    noiselevel = []
    while running_time() - start_time < read_time:
        current_noiselevel = read()
        noiselevel.append(current_noiselevel)
        if current_noiselevel > loudest_read:
            loudest_read = current_noiselevel
        microbit.sleep(read_span)
    avg_noiselevel = sum(noiselevel) / len(noiselevel)
    return loudest_read, avg_noiselevel


def running_time():
    return time.time()


def wait_for_double_clap(timeout=1000, spread=500, sensitivity=75):
    sensitivity = 105 - sensitivity

    clap_one_time = None

    start_time = running_time()
    while running_time() - start_time < timeout:
        if read() > sensitivity:
            while read() > sensitivity:
                pass
            microbit.sleep(100)
            if clap_one_time is not None and running_time() - clap_one_time < spread:
                return True
            else:
                clap_one_time = running_time()

    return False

def wait_for_clap(timeout=1000, sensitivity=75):
    sensitivity = 105 - sensitivity

    start_time = running_time()
    while running_time() - start_time < timeout:
        #if int(running_time() - start_time) % 2 == 0:
        sound_level = read()
        if sound_level > sensitivity:
            print(sound_level)
            return True

    return False

if __name__ == "__main__":
    loudest_noise, avg_noiselevel = read_loudest(read_span=1, read_time=10)
    print(f"Loudest noise: {loudest_noise}/nAverage noiselevel: {avg_noiselevel}")