import cv2
from ultralytics import YOLO
yolo = YOLO('yolov8s.pt')
videoCap = cv2.VideoCapture(0)
def getColours(cls_num):
    base_colors = [(255, 0, 0), (0, 25
    color_index = cls_num % len(base_c
    increments = [(1, -2, 1), (-2, 1,
    color = [base_colors[color_index][
    (cls_num // len(base_colors)) % 25
    return tuple(color)
while True:
    ret, frame = videoCap.read()
    if not ret:
        continue
    results = yolo.track(frame, stream
    for result in results:
        classes_names = result.names
        for box in result.boxes:
            if box.conf[0] > 0.4:
                [x1, y1, x2, y2] = box
                x1, y1, x2, y2 = int(x

                cls = int(box.cls[0])

                class_name = classes_n
                colour = getColours(cl
                cv2.rectangle(frame, (
                cv2.putText(frame, f'{
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q
        break

videoCap.release()
cv2.destroyAllWindows()