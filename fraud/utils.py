from sklearn.ensemble import IsolationForest


def perform_fraud_detection(df, template_name):

    # Create an Isolation Forest instance
    clf = IsolationForest(n_estimators=100, contamination=0.05)

    # Fit the Isolation Forest model to the data
    clf.fit(df)

    # Predict the labels for the data
    labels = clf.predict(df)

    # Identify the outliers
    outliers = labels == -1

    # Count the number of outliers
    n_outliers = sum(outliers)

    # Get the fraudulent transactions
    fraudulent_transactions = df[outliers]

    # Convert the fraudulent transactions to HTML
    try:
        fraudulent_transactions_html = fraudulent_transactions.to_html(
        classes='table table-dark table-bordered table-striped', index=False)
    except Exception as e:
        print('Problem in Table is : ', e)

    # Return the pie chart and the fraudulent transactions HTML
    return fraudulent_transactions_html, n_outliers, len(df) - n_outliers
