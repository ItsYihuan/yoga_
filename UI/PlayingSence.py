import tkinter as tk
import pyttsx3
from PIL import Image, ImageTk
import threading
import time
import tools.VideoPath as VideoPath
from tools.VideoPlayer import VideoPlayer
from yoga_toolkit.yogaPose import *
from yoga_toolkit.mat_data import *

""" Ture if the yoga mat is connected. """
use_mat = False#True
if(use_mat):
	from yoga_toolkit.yogamat import get_heatmap



class StartPlay(tk.Frame):
	def __init__(self, master, name, vs):
		super().__init__(master)
		self.master = master
		self.is_running = False
		self.is_paused = False
		self.cnt_frame = 0		
		self.txt_tmp = ""
		self.img_path = VideoPath.Yoga_Tips[name]
		
		tk.Label(self, text=name, font=('Comic Sans MS', 30, 'bold'), fg='#B15BFF').place(x=500, y=15)
		""" hint """
		self.hint_text = tk.StringVar()
		tk.Label(self, textvariable=self.hint_text, font=('微軟正黑體', 16), fg='#B15BFF').place(x=50, y=680)
		icon = Image.open('data/image/return.jpg').resize((50, 50))
		iconimage = ImageTk.PhotoImage(icon)
		return_btn = tk.Button(self, text='Return', image=iconimage, command=self.stop)
		return_btn.photo = iconimage
		return_btn.place(x=1150, y=10)

		self.width, self.height = 600, 500

		""" yoga mat data"""
		self.yoga_mat_data = mat_data()
		self.heatmap_frame = None

		""" image """
		self.canvas_img = tk.Canvas(self, width=self.width, height=self.height)
		self.canvas_img.place(x=20, y=100)
		self.img_thread = threading.Thread(target=self.change_image, daemon=True)

		""" get_mat_data """
		self.get_mat_data_thread = threading.Thread(target=self.get_mat_data, daemon=True)

		""" webcam """
		self.canvas_cam = tk.Canvas(self, width=self.width, height=self.height)
		self.canvas_cam.place(x=650, y=100)
		self.vs = vs
		self.web_thread = threading.Thread(target=self.cap_update, daemon=True)

		""" counting """
		self.count = tk.StringVar()
		tk.Label(self, textvariable=self.count, font=('Comic Sans MS', 50, 'bold'), fg='#F00078', bg='#D0D0D0').place(x=1180, y=100)
		self.counting_thread = threading.Thread(target=self.counting, daemon=True)

		""" detect model"""
		self.model = YogaPose(VideoPath.Yoga_Model[name])
		self.model.initialDetect()

		""" audio """
		self.engine = pyttsx3.init()
		self.engine.setProperty('rate', 150)
		self.voice_thread = threading.Thread(target=self.voice, daemon=True)

		""" heatmap """
		""" Turn off the comment below if the yoga mat is connected. """
		if(use_mat):
			w, h = self.width, 150
			self.canvas_heatmap = tk.Canvas(self, width=w, height=h)
			self.canvas_heatmap.place(x=650, y=620)
			self.heatmap_thread = threading.Thread(target=self.heatmap_display, daemon=True)

		self.cap_start()

	def change_image(self):
		"""
		This is a function used to change the image to give user a hint.
		"""
		while self.is_running:
			img = self.img_path
			try:
				back_img = Image.open(img).resize((self.width, self.height))
				back_img = ImageTk.PhotoImage(back_img)
				self.canvas_img.create_image(0, 0, anchor='nw', image=back_img)
				self.canvas_img.image = back_img
			except:
				pass

			time.sleep(2)

	def get_mat_data(self):
		if(use_mat):
			while self.is_running:
				self.heatmap_frame, self.yoga_mat_data = get_heatmap()
				cv2.imshow("heatmap", self.heatmap_frame)
				print(self.yoga_mat_data)
				if cv2.waitKey(1) == ord('q'):
					break

	def heatmap_display(self):
		if(use_mat):
			while self.is_running:
				photo_image = ImageTk.PhotoImage(Image.fromarray(self.heatmap_frame))
				self.canvas_heatmap.create_image(0, 0, anchor='nw', image=photo_image)
				self.canvas_heatmap.image = photo_image
				self.canvas_heatmap.update()

	def counting(self):
		"""
		This is a function used for countdown while pratice.
		"""
		self.count.set(30)
		cnt_tmp = int(self.count.get())
		while cnt_tmp > -1:
			self.count.set(cnt_tmp)
			time.sleep(1)
			if cnt_tmp == 0:
				self.is_paused = False
				result = tk.messagebox.showinfo("Time's up", "comment here...")
				if result == "ok":
					self.count.set("")
					self.cnt_frame = 0
					self.stop()
			cnt_tmp -= 1

	def cap_start(self):
		"""
		This is a function used to start all the threads while switch to the playing sence.
		"""
		self.is_running = True
		self.web_thread.start()
		if(use_mat):
			self.get_mat_data_thread.start()
			self.heatmap_thread.start()
		self.voice_thread.start()
		self.img_thread.start()

	def cap_update(self):
		"""
		This is a function used to update the frame of the camera.
		"""
		while self.is_running:
			frame = self.vs.frame
			if frame is not None:
				try:
					frame = cv2.resize(frame, (self.width, self.height))
					frame = self.model.detect(frame, self.width, self.height, False, self.yoga_mat_data)
					frame = cv2.flip(frame, 180)
					photo_image = ImageTk.PhotoImage(Image.fromarray(frame))
					self.canvas_cam.create_image(0, 0, anchor='nw', image=photo_image)
					self.canvas_cam.image = photo_image
					self.canvas_cam.update()
					self.txt_tmp = self.model.tips
					self.img_path = self.model.imagePath
					
				except:
					print('cap stop')

	def voice(self):
		"""
		This is a function used to do text-to-speech opartion.
		"""
		while self.is_running:
			if not self.is_paused:
				if self.cnt_frame > 2:
						self.hint_text.set("請維持動作30秒，開始計時")
						self.counting_thread.start()
						self.is_paused = True
						self.cnt_frame = -1
				elif self.hint_text.get() == "" and self.cnt_frame != -1:
					self.hint_text.set('開始偵測...')
				elif self.count.get() == "0":
					self.hint_text.set("練習結束，休息30秒")
				else:
					self.hint_text.set(self.txt_tmp)

				if self.hint_text.get() == "動作正確" and self.cnt_frame != -1:
					self.cnt_frame += 1
				try:
					result = self.hint_text.get()
					self.engine.say(result)
					self.engine.runAndWait()
				except:
					# print('speech stop')
					pass
			else:
				self.hint_text.set("")
			time.sleep(2)

	def stop(self):
		self.is_running = False

		from UI.Menu import Menu
		self.master.switch_frame(Menu, vs=self.vs)
