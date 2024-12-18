import cv2 as cv
import math

def on_trackbar(val): # Cuando hay un cambio, que no haga nada. Ahora estamos pidiendo siempre el valor. Podriamos pasarle una funcion que cambie la imagen. 
    pass

def convert_to_color(frame, color): # Convert frame's color to parameter color 
    return cv.cvtColor(frame, color)

def get_trackbar_value(trackbar_name, window_name): # Get tackbar value to change image threshold
    return cv.getTrackbarPos(trackbar_name, window_name) + 1 # No puede ser 0, porque crashea

def denoise(frame, method, radius): # Method to eliminate noise
    kernel = cv.getStructuringElement(method, (radius, radius)) 
    opening = cv.morphologyEx(frame, cv.MORPH_OPEN, kernel) # Erosión - dilatación, elimina ruido true (puntos blancos)
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel) # Dilatación - erosión, elimina ruido false (puntos negros)
    return closing

def filter_contours_by_area(contours, min_area, max_area):
    filtered_contours = []
    for contour in contours:
        area = cv.contourArea(contour)
        if min_area <= area <= max_area:
            filtered_contours.append(contour)
    return filtered_contours

cap = cv.VideoCapture(1)
cv.namedWindow('img1') # Create Window
cv.createTrackbar('threshold', 'img1', 80, 255, on_trackbar) # Create trackbar for threshold
cv.createTrackbar('denoise', 'img1', 7, 50, on_trackbar) # Create trackbar for denoise
cv.createTrackbar('minArea', 'img1', 450, 10000, on_trackbar) # Create trackbars for area
cv.createTrackbar('maxArea', 'img1', 95000, 99999, on_trackbar) # Create trackbars for area

saved_contours = []
biggest_contour = None

while True:     
    ret, frame = cap.read()
    grey_frame = convert_to_color(frame, color=cv.COLOR_BGR2GRAY) # Convert frame to gray
    
    threshold_value = get_trackbar_value('threshold', 'img1') # Grab trackbar value for threshold
    kernel_radius = get_trackbar_value('denoise', 'img1') # Grab trackbar value for denoise
    min_area = get_trackbar_value('minArea', 'img1')
    max_area = get_trackbar_value('maxArea', 'img1')

    
    ret1, thresh1 = cv.threshold(grey_frame, threshold_value, 255, cv.THRESH_BINARY) # Apply threshold with trackbar value
    denoise_frame = denoise(thresh1, cv.MORPH_ELLIPSE, kernel_radius) # Apply denoise
    cv.imshow('grey_frame', denoise_frame)
    contours, hierarchy = cv.findContours(denoise_frame, cv.RETR_TREE, cv.CHAIN_APPROX_NONE) # Draw contours
    filtered_contours = filter_contours_by_area(contours, min_area, max_area)

    predicted_labels = []

    for contour in filtered_contours:   
        cv.drawContours(frame, [contour], -1, (0, 0, 255), 5) 

        # Calcular momentos del contorno
        M = cv.moments(contour)

        # Calcular centroide
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            # Dibujar el centroide
            cv.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
 
    cv.imshow('img1', frame) # Show image

    if cv.waitKey(1) == ord('z'): # Waits () amount of time, if the key 'z' is pressed, it stops the loop
        break

cap.release()
cv.destroyAllWindows()