"""
中介者模式：
	定义分发器，绑定每个采集器
	采集器采集完成后，直接执行相关函数，
	而实际的函数逻辑在分发器中完成
"""


class BaseMock:
	"""
	模拟器基类
	"""
	__mock_list = []

	def __init__(self):
		pass


class BaseDistributor:
	"""
	分发器基类
	"""
	def notify(self, sender, event: str):
		raise NotImplementedError("Not Implemented!")


class Distributor(BaseDistributor):
	"""
	分发器: 执行采集器采集到数据后的动作
		- 通过mqtt发送
		- 通过orm保存数据
	"""
	def __init__(self):
		"""
		初始化所有采集器，并绑定当前分发器
		"""
		self.collector1 = Collector1(self)
		self.collector2 = Collector2(self)
		#...

		pass


	def notify(self, sender, event: str):
		"""
		# 分发器处理逻辑
		:paras sender: 采集器
		:paras event: 动作->(sendmqttmsg, savedata)
		"""
		if isinstance(sender, type(self.collector2)):
			print(f"c2, sender:{sender.__dict__}, event:{event}")


class BaseCollection:
	"""
	采集器基类
	:paras distributor: 绑定分发器
	"""
	__distributor = None # 绑定分发器
	def __init__(self, distributor: Distributor = None):
		# 未绑定__distributor且初始化未传值
		if self.__distributor is None and distributor is None:
			raise ValueError("Not set distributor!!!")
		# 初始化__distributor
		elif self.__distributor is None and distributor is not None:
			self.__distributor = distributor
		# 绑定
		elif self.__distributor is not None and distributor is not None:
			raise ValueError(f"Distributor Exist: {self.__distributor}")
		else:
			print(f"Current distributor:{self.__distributor}")

	def sendmqtt(self):
		self.__distributor.notify(self, "sendmqtt")

	def savedata(self):
		self.__distributor.notify(self, "savedata")



class Collector1(BaseCollection):
	def __init__(self, distributor: Distributor = None):
		super(Collector1, self).__init__(distributor)


class Collector2(BaseCollection):
	def __init__(self, distributor: Distributor = None):
		super(Collector2, self).__init__(distributor)


db = Distributor()
c0 = Collector1()
c1 = Collector1(db)
c2 = Collector2(db)
c1.sendmqtt()
c1.savedata()
c2.sendmqtt()
c2.savedata()
