import matplotlib.pyplot as plt
import numpy as np

xData = np.linspace(0, 4*np.pi, 100)
xData2 = np.linspace(0, 2*np.pi, 100)
yData1 = np.cos(xData)
yData2 = 2*np.sin(xData)
fig = plt.figure()
# subplot1 = fig.add_subplot('111')
# plt.plot(xData, yData1, figure=fig)
subplot1 = fig.add_subplot(211)
plt.plot(xData, yData1, figure=fig)
subplot2 = fig.add_subplot(212)
plt.plot(xData2, yData2, figure=fig)

plt.show()