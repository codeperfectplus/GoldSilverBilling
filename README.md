# Gold Silver Billing

![Homepage](/images/homepage.png)

## Our Mission

Our mission is to simplify the process of calculating gold prices for jewellers and customers alike. We aim to provide a user-friendly tool that allows for accurate and efficient calculations, ensuring transparency and trust in every transaction.

## Demo

- Demo is live on the [Render](https://goldsilverbilling.onrender.com/)

## Building and Running the Docker Container

1. **Build the Docker image:**

```bash
docker build -t goldsilverbilling .
```

2. **Run the Docker container:**

```bash
sudo docker run -p 5000:5000 goldsilverbilling
```


## Product Screenshots

![Gold Calculator](/images/gold_calculator.png)

![Gold Home Page](/images/bill_page.png)
   

## Improvements

- User Authentication: Add a login system to secure sensitive data.
- Data Persistence: Store historical data for future reference.
- API Integration: Fetch real-time gold/silver prices.
- Multi-Currency Support: Allow conversions for different currencies.
- Responsive Design: Enhance mobile usability.
- Advanced Analytics: Provide reports or graphs based on past transactions.
- Multi-Language Support: Cater to a broader audience by including multiple languages.
- Error Handling: Implement robust validation and error messages for user inputs.
