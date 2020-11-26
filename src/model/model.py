
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

def train(data, train_pct, depth = 3, **kwargs):
	dates = data['MEASUREMENT_TIME'].apply(lambda x: int(x[-12:-10]) * 24 * 60 + int(x[-9:-7]) * 60 + int(x[-6:-4]))
	# train-test split w/train_pct
	X_train, X_test, y_train, y_test = train_test_split(dates, data['VALUE'], train_size=train_pct)
	# use model params in kwargs 
	mdl = GradientBoostingClassifier(max_depth = depth)
	mdl.fit([[i] for i in X_train], y_train)

	return mdl


              
