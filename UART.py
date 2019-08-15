import sensor, image, time
from machine import UART

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=2)

threshold = [54, 99, -48, 13, 22, 52]

print("Thresholds are", threshold)


def write_uart(cx):
    global uart

    #if uart.any():
    #    print("$$$", uart.readline())

    #print("working fine")

    uart.write("%s\n" % (cx))
    print("UART sending " + "%s\n" % (cx))

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs([threshold], pixels_threshold=200, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        write_uart(blob.cx())

    #time.sleep(1000)

    #if blob.cx() < 75:
        #print("MOVE FORWARD")

    #if blob.cx() > 225:
        #print("MOVE BACK")
