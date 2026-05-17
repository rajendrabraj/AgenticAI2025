from sklearn.metrics import mean_absolute_percentage_error

y_test = [100, 200, 300]
predictions = [90, 210, 330]

mape = mean_absolute_percentage_error(y_test, predictions)

print(mape)
print(mape * 100)
print(f"MAPE: {mape * 100:.2f}%")