# Quick Booking API

This project is a Django-based API for a booking system that allows users to book rentals, leave reviews, and manage various related entities such as rentals and bookings. The API supports features such as user authentication, search and filtering, review management, and more.

## Features

### User Authentication and Management

- **User Registration and Login**: Users can register for a new account and log in to their existing accounts using username and password authentication.
- **User Profiles**: Each user has a profile where they can view and manage their personal information.
- **Permissions**: Different roles (e.g., Admin, Moderator, User) have different permissions, allowing for role-based access control throughout the application.

### Rental Management

- **Create, Update, Delete Rentals**: Authenticated users can create new rental listings, update existing ones, and delete rentals they own.
- **View Rentals**: All users, including anonymous ones, can view available rental listings. Users can filter rentals based on various criteria such as price, location, and amenities.

### Booking Management

- **Create Bookings**: Authenticated users can book rentals for specific dates. The system checks for availability and prevents double booking.
- **Update and Cancel Bookings**: Users can update their bookings or cancel them if needed. Certain conditions apply, such as cancellation deadlines.
- **Booking Statuses**: Each booking has a status (Pending, Confirmed, Cancelled, Completed), which helps in managing the booking lifecycle.

### Review System

- **Submit Reviews**: Users who have completed a booking can leave a review for the rental. Reviews can include a rating and a comment.
- **Update and Delete Reviews**: Users can update their own reviews or delete them if needed. Moderators can also manage reviews.
- **Review Visibility**: Reviews are tied to completed bookings to ensure authenticity and relevance.

### Search and Filtering

- **Advanced Search**: Users can search for rentals using various filters such as price range, location, number of rooms, property type, and tags.
- **Search History**: The system tracks search queries, allowing users to view their search history and see popular searches.

### Rating and Review Aggregation

- **Average Rating Calculation**: The system calculates the average rating for each rental based on user reviews, providing a quick overview of rental quality.
- **Review Count**: Each rental displays the total number of reviews, helping users gauge popularity and reliability.

### Admin Interface

- **Manage Rentals, Bookings, and Reviews**: Admins can view and manage all rentals, bookings, and reviews in the system.
- **User Management**: Admins can manage user accounts, including updating user information and handling permissions.
- **Dashboard**: The admin dashboard provides an overview of the system's activity, including recent bookings, new reviews, and user statistics.

### Notifications

- **Booking Notifications**: Users receive notifications for booking confirmations, updates, and cancellations.
- **Review Notifications**: Users are notified when they receive a new review or when their review is responded to.

### Security

- **Role-Based Access Control**: Different user roles have specific permissions, ensuring that users can only access and modify resources they are authorized to.
- **Data Validation and Error Handling**: The system includes robust data validation and error handling to ensure data integrity and provide clear feedback to users.

### Performance and Scalability

- **Pagination and Sorting**: All listing views (rentals, bookings, reviews) support pagination and sorting to efficiently handle large datasets.
- **Caching**: Certain views and data are cached to improve performance and reduce load on the server.

### Documentation and Testing

- **API Documentation**: Comprehensive API documentation is provided, detailing all available endpoints, request parameters, and responses.
- **Automated Testing**: The system includes a suite of automated tests to ensure code quality and reliability.

These features collectively provide a comprehensive and robust platform for managing rentals, bookings, and reviews, catering to both end-users and administrators.
