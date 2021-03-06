from time import time
import os

def check_file(time_between_recheck = 10):
    current_time = time()
    timefile = "timefile.txt"
    update = False
    if not os.path.isfile(timefile):
        update = True
        with open(timefile, "w") as f:
            f.write(str(current_time))
    else:
        with open(timefile, "r") as f:
            last_check_time = float(f.read())
            if (current_time - last_check_time) > time_between_recheck:
                update = True
                with open(timefile, "w") as f:
                    f.write(str(current_time))
    return update







if __name__ == "__main__":
    check_file()