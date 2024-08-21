# Gold Silver Billing

![Homepage](/screenshots/app.png)

## Mission

Our goal is to simplify the process of calculating gold prices for jewelers and customers alike. We aim to provide a user-friendly, accurate, and efficient tool for gold price calculations. By ensuring transparency and trust in every transaction, we help users make informed decisions and streamline their billing processes.

## Features

- **Real-time Price Calculation:** Provides immediate and accurate estimates for gold prices based on user inputs.
- **Transaction History:** Maintains a detailed log of all transactions for easy tracking and reference.
- **Multi-Level Authentication:** Implements secure login with distinct roles for different user types (e.g., admin, manager, customer).
- **User-Friendly Interface:** Designed with an intuitive layout for easy navigation and use.
- **Customizable Charges:** Allows users to adjust service charges, taxes, and other fees according to their needs.
- **Responsive Design:** Ensures the application is fully functional on various devices, including desktops, tablets, and smartphones.
- **Secure Data Handling:** Protects sensitive information with robust security measures.
- **Business Customization:** Provides options for tailoring the application to specific business requirements, including currency settings and theme preferences.

## Demo

Explore the live demo of the application on the following platforms:

- [Railway (Server 1)](https://goldsilverbilling-production.up.railway.app/)
- [Render (Server 2)](https://goldsilverbilling.onrender.com/)

## Building and Running the Docker Container

To get the application up and running using Docker, follow these steps:

1. **Build the Docker Image:**

    ```bash
    docker build -t goldsilverbilling .
    ```

    This command creates a Docker image named `goldsilverbilling` based on the Dockerfile in the project directory.

2. **Run the Docker Container:**

    ```bash
    docker run -p 5000:5000 goldsilverbilling
    ```

    This command runs a container from the `goldsilverbilling` image and maps port 5000 of the container to port 5000 on your host machine.

## Screenshots

Here are some screenshots of the application:

### Homepage

![Homepage](/screenshots/homepage.png)

### Admin Dashboard

![Admin Dashboard](/screenshots/admin_dashboard.png)

### Gold Calculator

![Gold Calculator](/screenshots/gold_calculator.png)

### System Settings

![System Settings](/screenshots/system_setting.png)

### Transaction History

![Transaction History](/screenshots/transaction_history.png)

## Planned Improvements

We are continually working on enhancing the application. Here are some planned improvements:

| Improvement            | Type                  | Details                                                                                   | Status |
|------------------------|-----------------------|-------------------------------------------------------------------------------------------|--------|
| **User Authentication**    | Security              | Implement a robust login system to secure sensitive data and restrict access based on user roles.       | ✅ |
| **Data Persistence**       | Functionality         | Ensure historical data is stored and easily retrievable for future reference.                            | ✅ |
| **Multi-Currency Support** | Functionality         | Introduce support for multiple currencies to allow users to perform conversions and calculations in different currencies. | ✅ |
| **Responsive Design**      | User Experience       | Enhance the design and layout for improved usability on mobile and tablet devices.                     | ✅ |
| **Error Handling**         | Functionality         | Implement comprehensive validation and error messaging to improve user experience and data integrity.    | ✅ |
| **API Integration**        | Integration           | Integrate external APIs to fetch real-time gold and silver prices.                                           | :x:    |
| **Advanced Analytics**     | Functionality         | Develop features to generate detailed reports and visualizations based on transaction data.                | :x:    |
| **Multi-Language Support** | User Experience       | Add support for multiple languages to cater to a wider audience and enhance accessibility.                | :x:    |

## Author

- [@codeperfectplus](https://github.com/codeperfectplus)

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

We'd like to acknowledge the following tools and libraries that have been instrumental in developing this project:

- [Python](https://www.python.org/) - The programming language used for the backend.
- [Flask](https://flask.palletsprojects.com/) - The web framework used for building the application.
- [Font Awesome](https://fontawesome.com/) - For icons and graphical elements.
- [Bootstrap](https://getbootstrap.com/) - For responsive design and styling.
- [Render](https://render.com/) - For hosting the application on the web.
- [Railway](https://railway.app/) - For additional hosting services.

## Contact

For any questions, feedback, or suggestions, please reach out to us at [codeperfectplus@gmail.com](mailto:codeperfectplus@gmail.com).

---
