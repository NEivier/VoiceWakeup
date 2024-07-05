import cv2

def play_video(video_path):

	# 创建一个videocapture对象
	cap=cv2.VideoCapture(video_path)
	
	# 获取视频的宽和高
	video_width = int (cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	video_height =int (cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	# 计算宽高比
	#video_ratio=video_width/video_height

	# 创建窗口，并设置全屏且处于中央
	cv2.namedWindow('smile',cv2.WINDOW_NORMAL)
	# 获取屏幕的宽和高
	# screen_width = cv2.getWindowProperty('screen',cv2.WND_PROP_FULLSCREEN_WIDTH)
	# screen_height = cv2.getWindowProperty('screen',cv2.WND_PROP_FULLSCREEN_HEIGHT)
	# 计算宽高比
	# screen_ratio= screen_width/screen_height
	
	# if video_ratio > screen_ratio:
	#	new_height = screen_height
	#	new_width = int (new_height*video_ratio)
	# else:
	#	new_width = screen_width
	#	new_height = int (new_width / video_ratio)
			
	#调整视频窗户的尺寸
	# cv2.resizeWindow('screen',new_width,new_height)
	cv2.setWindowProperty('smile',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

	# 获取视频的帧频
	fps = cap.get(cv2.CAP_PROP_FPS)
	# i = 0
	while(cap.isOpened()):
		#逐帧读取视频
		ret,frame = cap.read()
		if ret == True:
			# 窗口大小
			src = cv2.resize(frame,(video_width ,video_height),interpolation=cv2.INTER_CUBIC) 
			#
			cv2.imshow('smile',src)
			# i=i+1
			# print(i)
			#按q 退出
			if cv2.waitKey(int(1000/fps)) & 0xFF ==ord('q'):
				break
		else:
			break
	#释放资源
	cap.release()
	cv2.destroyAllWindows()
if __name__=='__main__':
	play_video('video_smile/smile2.mp4')
	
 
