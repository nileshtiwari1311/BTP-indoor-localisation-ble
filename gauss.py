from sklearn import gaussian_process
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel
import random
import numpy as np
import matplotlib.pyplot as plt

my_list = []
x_list = []

for i in range(0,30) :
	my_list.append(-1.0*random.randrange(8958000, 9555556)/100000)
	x_list.append(i+1)

my_list.sort()

y = np.array(my_list)
Y = y.reshape(-1, 1)
x = np.array(x_list)
X = x.reshape(-1, 1)

fig = plt.figure()
plt.subplot(1, 2, 1)
plt.plot(X, Y)

kernel = ConstantKernel() + Matern(length_scale=2, nu=3/2) + WhiteKernel(noise_level=1)

gp = gaussian_process.GaussianProcessRegressor(kernel=kernel)
gp.fit(X, Y)

#GaussianProcessRegressor(alpha=1e-10, copy_X_train=True, kernel=1**2 + Matern(length_scale=2, nu=1.5) + WhiteKernel(noise_level=1), n_restarts_optimizer=0, normalize_y=False, optimizer='fmin_l_bfgs_b', random_state=None)
x_pred = np.linspace(10, 20).reshape(-1,1)
y_pred, sigma = gp.predict(x_pred, return_std=True)

print(y_pred)
plt.subplot(1, 2, 2)
plt.plot(x_pred, y_pred)
plt.show()