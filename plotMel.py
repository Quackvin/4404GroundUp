import matplotlib.pyplot as plt
import math

def f2mel(x):
	return 2595*math.log((1+x/700),10)

x = range(10000)
y = [f2mel(i) for i in x]

plt.plot(x,y)
plt.title('Frequency to Mel Scale Conversion')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Mel Scale (mels)')
plt.gca().set_ylim(ymin=0)
plt.gca().set_xlim(0,10000)
plt.show()