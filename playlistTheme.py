class playlistTheme():

	def __init__(self, genre, activity = None):
		self._genre = genre
		self._targetTempo = int(input('Target tempo (bpm): '))
		self._targetDuration = int(input('Target duration (sec): '))
		self._targetLoudness = int(input('Target loudness (dB): '))
		self._targetLiveness = int(input('Target liveness (0-1): '))
		self._targetSpeechiness = int(input('Lyric concentration (0-1): '))
		self._targetAcousticness = int(input('Target acousticness (0-1)): '))
		self._targetEnergy = int(input('Target energy (0-1): '))
		self._targetDanceability = int(input('Party factor!!! (0-1)? '))

	def setParty(self):
		self._targetTempo = 120
		self._targetDuration = 180
		self._targetLoudness = 0
		self._targetLiveness = 0.2
		self._targetSpeechiness = 0.5
		self._targetAcousticness = 0.2
		self._targetEnergy = 0.8
		self._targetDanceability = 1

	def setStudy(self):
		self._targetTempo = 75
		self._targetDuration = 360
		self._targetLoudness = -30
		self._targetLiveness = 0.2
		self._targetSpeechiness = 0
		self._targetAcousticness = 0.3
		self._targetEnergy = 0.2
		self._targetDanceability = 0.1

	def setChill(self):
		self._targetTempo = 80
		self._targetDuration = 360
		self._targetLoudness = 0
		self._targetLiveness = 0.5
		self._targetSpeechiness = 0.5
		self._targetAcousticness = 0.5
		self._targetEnergy = 0.5
		self._targetDanceability = 0.2

	def setWorkout(self):
		self._targetTempo = 170
		self._targetDuration = 240
		self._targetLoudness = 1
		self._targetLiveness = 0.5
		self._targetSpeechiness = 0.7
		self._targetAcousticness = 0
		self._targetEnergy = 1
		self._targetDanceability = 0.7