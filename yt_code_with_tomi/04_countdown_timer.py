import time


def countdown(seconds):
    while seconds:
        # calculate the mins and seconds from the total seconds
        mins, secs = divmod(seconds, 60)
        # output format
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        # wait the second
        time.sleep(1)
        # decrement the total seconds
        seconds -= 1

    print('Timer completed!')


t = input('Enter the time in seconds: ')

countdown(int(t))
