import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import pickle 

nexmp = 10000 #number of examples
vlen = 30  #vector length

X = []
y = []

for n in range(int(nexmp/5)):
    X.append(np.random.choice([0,1], vlen, [0.5, 0.5]))
    X.append(np.random.choice([0,1], vlen, [0.80, 0.20]))
    X.append(np.random.choice([0,1], vlen, [0.20, 0.80]))
    X.append(np.random.choice([0,1], vlen, [0.05, 0.95]))
    X.append(np.random.choice([0,1], vlen, [0.95, 0.05]))

for x in X:
    z = 0
    for bit in x:
        if bit == 0:
            z += 1
    y.append(z)

X = [x.tolist() for x in X]

X_train, X_test, y_train, y_test = train_test_split(X, y)

mlp = MLPRegressor(hidden_layer_sizes=(50,50), max_iter=300)
mlp.fit(X_train, y_train)

#print('prova:', mlp.predict([X_test[0]]))
pred_test = mlp.predict(X_test)

print([(pred_test[i], y_test[i]) for i in range(len(y_test))])
print(mlp.score(X_test, y_test))

with open('mlp_zeromax.pickle', 'bw') as mlpfile:
    pickle.dump(mlp, mlpfile)
