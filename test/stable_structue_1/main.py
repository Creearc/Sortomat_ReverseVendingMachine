import time

from components import get_data
from components import get_frame
from components import frame_processing
from components import object_detection
from components import data_processing
from components import frame_draw_debug
from components import send_data

from config import settings, data

get_frame_component        = get_frame.Get_frame(settings)
frame_processing_component = frame_processing.Frame_processing(settings)
object_detection_component = object_detection.Object_detection(settings)
data_processing_component  = data_processing.Data_processing(settings)
frame_draw_debug_component = frame_draw_debug.Frame_draw_debug(settings)
send_data_component        = send_data.Send_data(settings)

while not data['stop']:
    try:
        data = get_data.run(data)

        frame, data = get_frame_component.run(data)
        if frame is None:
            time.sleep(0.1)
            continue
        
        data = frame_processing_component.run(frame, data)
        data = object_detection_component.run(frame, data)
        data = data_processing_component.run(data)
        data = frame_draw_debug_component.run(data)
        send_data_component.run(data)
    except Exception as e:
        print(e)
    
