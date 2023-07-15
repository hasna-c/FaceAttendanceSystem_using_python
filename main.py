import os.path
import subprocess
from datetime import datetime
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1200x520+350+100")

        self.log_button_window = util.get_button(self.window, 'Login', 'green', self.log)
        self.log_button_window.place(x=900, y=220)
        self.reg_button_window = util.get_button(self.window, 'Register new user', 'grey', self.reg, fg='black')
        self.reg_button_window.place(x=900, y=300)

        self.cam = util.get_img_label(self.window)
        self.cam.place(x=5, y=0, width=850, height=580)

        self.add_cam(self.cam)
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_cam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        self._label = label
        self.process_cam()

    def process_cam(self):
        ret, frame = self.cap.read()
        self.most_recent_cap_arr = frame
        img_ = cv2.cvtColor(self.most_recent_cap_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_cap_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_cap_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_cam)

    def log(self):
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_cap_arr)

        output_bytes = subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path])
        output_str = output_bytes.decode('utf-8')


        name = output_str.split(',')[1].strip().replace('\r', '').replace('\n', '')

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Ops...', 'Unknown user. Please register a new user or try again')
        else:
            util.msg_box('Welcome back!', 'Welcome, {}.'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.now()))
                f.close()

        os.remove(unknown_img_path)

    def reg(self):
        self.reg_new_user = tk.Toplevel(self.window)
        self.reg_new_user.geometry("1200x520+250+90")
        self.reg_new_user_button = util.get_button(self.reg_new_user, 'Accept', 'green', self.accept_new_reg)
        self.reg_new_user_button.place(x=900, y=220)
        self.try_again_reg_new_user = util.get_button(self.reg_new_user, 'Try again!', 'Red', self.try_again_new_reg)
        self.try_again_reg_new_user.place(x=900, y=300)
        self.capture = util.get_img_label(self.reg_new_user)
        self.capture.place(x=5, y=0, width=850, height=580)

        self.add_img_to_label(self.capture)
        self.entry_text_new_user = util.get_entry_text(self.reg_new_user)
        self.entry_text_new_user.place(x=900, y=120)

        self.text_label_reg_new_user = util.get_text_label(self.reg_new_user, 'Please,\n enter new username :')
        self.text_label_reg_new_user.place(x=900, y=60)



    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_cap_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.reg_new_user_capture = self.most_recent_cap_arr.copy()


    def start(self):
        self.window.mainloop()

    def accept_new_reg(self):
        name = self.entry_text_new_user.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.reg_new_user_capture)
        util.msg_box('Registration successful!', 'The user has been registered successfully!')

        self.reg_new_user.destroy()

    def try_again_new_reg(self):
        self.reg_new_user.destroy()


if __name__ == "__main__":
    app = App()
    app.start()
