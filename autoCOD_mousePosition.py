import win32gui,  pynput

def get_mousePos():
    cod_window = win32gui.FindWindow(None, 'Call of Dragons')
    rect = win32gui.GetWindowRect(cod_window)
    xo = rect[0]
    yo = rect[1]
    def on_click(x, y, button, pressed):
        if pressed and button == pynput.mouse.Button.left:
            print("Mouse Position:", [x-xo, y-yo])
        if pressed and button == pynput.mouse.Button.right:
            listener.stop()
            k = input("press close to exit") 
    with pynput.mouse.Listener(on_click=on_click) as listener:
        listener.join()
    
get_mousePos() 