import pyautogui

# Set the path of the image to be clicked
image_path1 = 'img1.png'
image_path2 = 'img2.png'
image_path3 = 'img3.png'

# Set the confidence level for the image recognition (0.0 to 1.0)
confidence = 0.9

while True:
    location = pyautogui.locateOnScreen(image_path1, confidence=confidence)
    
    if location is not None:
        center = pyautogui.center(location)
        pyautogui.click(center)


    location = pyautogui.locateOnScreen(image_path2, confidence=confidence)
    
    if location is not None:
        center = pyautogui.center(location)
        pyautogui.click(center)

    
    location = pyautogui.locateOnScreen(image_path3, confidence=confidence)
    
    if location is not None:
        center = pyautogui.center(location)
        pyautogui.click(center)
