import numpy as np

def stochastic_gradient_descent(X, y, learning_rate=0.01, epochs=1000):
    """
    Perform Stochastic Gradient Descent for linear regression.

    Parameters:
    - X: Feature matrix (n_samples, n_features)
    - y: Target vector (n_samples,)
    - learning_rate: Step size for weight updates
    - epochs: Number of full passes over the dataset

    Returns:
    - weights: Learned weight vector (n_features,)
    """
    n_samples, n_features = X.shape
    weights = np.zeros(n_features)

    for epoch in range(epochs):
        for i in range(n_samples):
            prediction = np.dot(X[i], weights)
            error = prediction - y[i]
            gradient = error * X[i]
            weights -= learning_rate * gradient

    return weights

if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(0)

    # Generate synthetic linear data
    X = 2 * np.random.rand(100, 1)
    y = 4 + 3 * X + np.random.randn(100, 1)

    # Add bias term (x0 = 1) to features
    X_b = np.c_[np.ones((X.shape[0], 1)), X]

    # Flatten y to 1D
    y = y.ravel()

    # Set hyperparameters
    learning_rate = 0.01
    epochs = 1000

    # Train model
    weights = stochastic_gradient_descent(X_b, y, learning_rate, epochs)

    # Output learned weights
    print(f"Weights: {weights}")
