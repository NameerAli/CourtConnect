# CourtConnect

CourtConnect is a comprehensive platform designed to facilitate court bookings, online payments, tournament management, and more. The project is divided into a **Django REST API backend** and a **Next.js frontend** for a seamless and efficient user experience.

---

## Features

- ✅ Court Booking System: Reserve courts with ease.
- ✅ Online Payments: Secure integration with payment gateways.
- 🔄 Tournament Management: Organize and manage tournaments.
- 🔄 Leaderboard System: Track player rankings and match history.
- 🔄 Mobile App Integration: Coming soon for iOS and Android platforms.

---

## Getting Started

### Prerequisites

- Python 3.x
- Node.js & npm
- PostgreSQL (or your preferred database)

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate    # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file for environment variables (sample variables below):
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgres://user:password@localhost:5432/courtconnect_db
   PAYMENT_API_KEY=your-payment-api-key
   ```

5. Run migrations and start the server:
   ```
   python manage.py migrate
   python manage.py runserver
   ```

---

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Create a `.env.local` file in the frontend root with environment variables such as:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   NEXT_PUBLIC_STRIPE_KEY=your-stripe-public-key
   ```

4. Start the development server:
   ```
   npm run dev
   ```

---

## Roadmap

| Feature               | Status      |
|-----------------------|-------------|
| Court Booking System   | 🔄 In Progress |
| Online Payments       | 🔄 In Progress |
| Tournament Management  | 🔄 In Progress |
| Leaderboard System    | 🔄 Planned  |
| Mobile App Integration | 🔄 Planned  |

Features marked with 🔄 are actively being developed or planned for upcoming releases.

---

## Contributing

We welcome contributions to enhance CourtConnect!  
To contribute:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to your branch (`git push origin feature-name`).
5. Open a Pull Request.

Before working on bigger changes, please open an issue to discuss your ideas.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact & Support

For any questions or support, please open an issue in the repository or contact the maintainer directly.

---

Thank you for using CourtConnect! We’re excited to have you on board to help improve and expand this platform.
