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

This project uses Docker Compose for easy setup and development.

### Prerequisites

- Docker Desktop (or Docker Engine) installed and running.

### Running with Docker Compose

1.  **Build and start the services:**
    Navigate to the root directory of the project (where `docker-compose.yml` is located) and run:
    ```bash
    docker-compose up --build
    ```
    This command will:
    *   Build the Docker images for the backend and frontend.
    *   Start the PostgreSQL database, backend, and frontend services.

2.  **Run Django Migrations (first time setup):**
    Once the services are up, you need to run Django migrations to set up the database schema. Open a new terminal in the project root and execute:
    ```bash
    docker-compose exec backend python manage.py migrate
    ```
    This command runs the `migrate` command inside the `backend` container.

3.  **Access the applications:**
    *   **Frontend:** http://localhost:3000
    *   **Backend API:** http://localhost:8000

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
