import pandas as pd
import numpy as np
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Embedding, Flatten
from tensorflow.keras.optimizers import Adam

df_all = pd.read_csv('data_classif_person.csv', sep=';')


# Create X_all and Y_all as np arrays
X_all = np.array(df_all['Embedding'].tolist())
y_all = np.array(df_all['Person'].tolist())

print(len(X_all))
print(len(y_all))

#neural network


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2, random_state=42)

# Define the neural network
model = Sequential()
model.add(Dense(64, activation="relu", input_shape=(X_all.shape[1],)))  # Input layer
model.add(Dropout(0.5))  # Regularization
model.add(Dense(32, activation="relu"))  # Hidden layer
model.add(Dense(1, activation="sigmoid"))  # Output layer for binary classification

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss="binary_crossentropy", metrics=["accuracy"])

# Train the model
history = model.fit(X_train, y_train, epochs=14, batch_size=4, validation_data=(X_test, y_test), verbose=1)

# Evaluate the model
y_pred = (model.predict(X_test) > 0.5).astype("int32")
print("\nClassification Report:")
class_nn = classification_report(y_test, y_pred)
print(class_nn)