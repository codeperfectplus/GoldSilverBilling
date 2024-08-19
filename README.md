# Gold Silver Billing

![Homepage](/images/app.png)

## Our Mission

Our mission is to simplify the process of calculating gold prices for jewellers and customers alike. We aim to provide a user-friendly tool that allows for accurate and efficient calculations, ensuring transparency and trust in every transaction.

## Features

- Real-time Price Calculation
- Transaction History
- Multi Level Authentication
- User-friendly Interface
- Customizable Charges
- Responsive Design
- Secure Data Handling
- Business Customization

## Demo

Demo is live on the the belows servers.

- [Railway(Server 2)](https://goldsilverbilling-production.up.railway.app/)
- [Render(Server 1)](https://goldsilverbilling.onrender.com/)

## Building and Running the Docker Container

1. **Build the Docker image:**

```bash
docker build -t goldsilverbilling .
```

2. **Run the Docker container:**

```bash
docker run -p 5000:5000 goldsilverbilling
```


## Product Screenshots

### Homepage

![Homepage](/images/homepage.png)

### Admin Dashboard

![Admin Dashboard](/images/admin_dashboard.png)

### Gold Calculator

![Gold Calculator](/images/gold_calculator.png)

### System Settings

![System Settings](/images/system_setting.png)
   
### Transaction History

![Transaction History](/images/transaction_history.png)

## Improvements

| Improvement            | Type                  | Details                                                                                   | Implemented |
|------------------------|-----------------------|-------------------------------------------------------------------------------------------|--------------|
| User Authentication    | Security              | Add a login system to secure sensitive data.                                              | &#x2611;           |
| Data Persistence       | Functionality         | Store historical data for future reference.                                               | &#x2611;           |
| Multi-Currency Support | Functionality         | Allow conversions for different currencies.                                               | &#x2611;           |
| Responsive Design      | User Experience       | Enhance mobile usability by optimizing the layout and design for smaller screens.         | &#x2611;           |
| Error Handling         | Functionality         | Implement robust validation and error messages for user inputs to improve user experience. |&#x2611;           |
| API Integration        | Integration           | Fetch real-time gold/silver prices from external APIs.                                    | :x:           |
| Advanced Analytics     | Functionality         | Provide reports or graphs based on past transactions for better insights.                 | :x:           |
| Multi-Language Support | User Experience       | Cater to a broader audience by including multiple languages for the user interface.       | :x:           |


## Author

- [@codeperfectplus](https://github.com/codeperfectplus)

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- [Font Awesome](https://fontawesome.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Render](https://render.com/)
- [Railway](https://railway.app/)

## Contact

For any queries or feedback, please feel free to reach out to us at [codeperfectplus@gmail.com](mailto:codeperfectplus@gmail.com).

---