import cv2, time, pandas
import winsound
from datetime import datetime

first_frame = None
video = cv2.VideoCapture(0)
status_list = [None,None]
times = []
df = pandas.DataFrame(columns = ['Start','End'])
flag = False;

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))	

while True:
	check, frame = video.read()
	status = 0
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray,(21,21),0)

	if first_frame is None:
		first_frame = gray
		continue

	delta_frame = cv2.absdiff(first_frame,gray)
	thresh_delta = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
	thresh_delta = cv2.dilate(thresh_delta,None,iterations=2)
	(_,cnts,_) = cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	var = False
	for contour in cnts:
		if cv2.contourArea(contour) < 10000:
			continue
		var = True
		status = 1
		(x,y,w,h) = cv2.boundingRect(contour)
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)

	if var:
		out.write(frame)
		winsound.Beep(2500,100)
	
	status_list.append(status)
	if status_list[-1] == 1 and status_list[-2] == 0:
		times.append(datetime.now())
	if status_list[-1] == 0 and status_list[-2] == 1:
		times.append(datetime.now())

	cv2.imshow('Gray Frame',gray)
	cv2.imshow('Delta Frame',delta_frame)
	cv2.imshow('Threshold Frame',thresh_delta)
	cv2.imshow('Color Frame',frame)

	key = cv2.waitKey(1)
	if key == ord('q'):
		if status == 1:
			times.append(datetime.now())
		break

print(status_list)
print(times)

for x in range(0,len(times),2):
	df = df.append({'Start':times[x],'End':times[x+1]},ignore_index=True)

df.to_csv('Times.csv')

video.release()
out.release()
cv2.destroyAllWindows()