import cv2
import math

def on_trackbar(val): # Cuando hay un cambio, que no haga nada. Ahora estamos pidiendo siempre el valor. Podriamos pasarle una funcion que cambie la imagen. 
    pass

def convert_to_color(frame, color): # Convert frame's color to parameter color 
    return cv2.cvtColor(frame, color)

def get_trackbar_value(trackbar_name, window_name): # Get tackbar value to change image threshold
    return cv2.getTrackbarPos(trackbar_name, window_name) + 1 # No puede ser 0, porque crashea

def denoise(frame, method, radius): # Method to eliminate noise
    kernel = cv2.getStructuringElement(method, (radius, radius)) 
    opening = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel) # Erosión - dilatación, elimina ruido true (puntos blancos)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel) # Dilatación - erosión, elimina ruido false (puntos negros)
    return closing

def filter_contours_by_area(contours, min_area, max_area):
    filtered_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area <= area <= max_area:
            filtered_contours.append(contour)
    return filtered_contours

cap = cv2.VideoCapture(0) # Use laptop camara
cv2.namedWindow('img1') # Create Window
cv2.createTrackbar('threshold', 'img1', 80, 255, on_trackbar) # Create trackbar for threshold
cv2.createTrackbar('denoise', 'img1', 7, 50, on_trackbar) # Create trackbar for denoise
cv2.createTrackbar('minArea', 'img1', 450, 10000, on_trackbar) # Create trackbars for area
cv2.createTrackbar('maxArea', 'img1', 95000, 99999, on_trackbar)

saved_contours = []
biggest_contour = None

while True:     
    ret, frame = cap.read()
    flip_frame = cv2.flip(frame, 1) # Flip image so its correct
    grey_frame = convert_to_color(frame=flip_frame, color=cv2.COLOR_BGR2GRAY) # Convert frame to gray
    
    threshold_value = get_trackbar_value('threshold', 'img1') # Grab trackbar value for threshold
    kernel_radius = get_trackbar_value('denoise', 'img1') # Grab trackbar value for denoise
    min_area = get_trackbar_value('minArea', 'img1')
    max_area = get_trackbar_value('maxArea', 'img1')

    
    ret1, thresh1 = cv2.threshold(grey_frame, threshold_value, 255, cv2.THRESH_BINARY) # Apply threshold with trackbar value
    denoise_frame = denoise(thresh1, cv2.MORPH_ELLIPSE, kernel_radius) # Apply denoise
    cv2.imshow('grey_frame', denoise_frame)
    contours, hierarchy = cv2.findContours(denoise_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # Draw contours
    filtered_contours = filter_contours_by_area(contours, min_area, max_area)

    predicted_labels = []

    for contour in filtered_contours:   
        cv2.drawContours(flip_frame, [contour], -1, (0, 0, 255), 5) # If it doesnt match any shape, paint contour in red
 
    cv2.imshow('img1', flip_frame) # Show image

    if cv2.waitKey(1) == ord('z'): # Waits () amount of time, if the key 'z' is pressed, it stops the loop
        break

cap.release()
cv2.destroyAllWindows()