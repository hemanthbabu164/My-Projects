# Interactive To-Do List App

A modern, feature-rich to-do list application built with Flask, SQLite, and vanilla JavaScript. This app includes task categorization, priority levels, due dates, reminders, and advanced filtering capabilities.

## Features

### Core Functionality
- ✅ **Add, edit, delete tasks** with rich descriptions
- ✅ **Mark tasks as complete/incomplete** with visual feedback
- ✅ **Task categorization** with custom colors
- ✅ **Priority levels** (High, Medium, Low) with color coding
- ✅ **Due dates** with overdue detection
- ✅ **Reminders** with browser notifications
- ✅ **Search and filter** by keyword, category, priority, or status
- ✅ **Sorting** by date, priority, or due date

### Advanced Features
- 📊 **Dashboard statistics** (total, pending, completed, overdue tasks)
- 🎨 **Modern, responsive UI** with smooth animations
- 🔔 **Browser notifications** for reminders
- 💾 **Local storage backup** for offline capability
- ⌨️ **Keyboard shortcuts** (Ctrl+N for new task, Esc to close modals)
- 📱 **Mobile-friendly** responsive design

## Tech Stack

- **Backend**: Flask + SQLAlchemy + SQLite
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Styling**: Modern CSS with gradients and animations
- **Icons**: Font Awesome 6
- **Database**: SQLite (easily upgradeable to PostgreSQL/MySQL)

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps

1. **Clone or download the project**
   ```bash
   cd todo-list
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   - Navigate to `http://localhost:5000`
   - The app will automatically create the database and default categories

## Usage Guide

### Getting Started
1. **Create Categories**: Start by adding custom categories (e.g., Work, Personal, Urgent)
2. **Add Tasks**: Click "Add Task" to create your first task with title, description, category, priority, and due date
3. **Set Reminders**: Add reminder times to get browser notifications
4. **Filter & Search**: Use the search bar and filters to find specific tasks
5. **Track Progress**: Monitor your productivity with the dashboard statistics

### Keyboard Shortcuts
- `Ctrl + N`: Add new task
- `Escape`: Close open modals
- `Enter`: Submit forms

### Browser Notifications
- Allow notifications when prompted for reminder alerts
- Notifications appear 1 minute before the reminder time
- Click notifications to jump to the specific task

## Database Schema

### Tasks Table
- `id`: Primary key
- `title`: Task title (required)
- `description`: Detailed description
- `completed`: Boolean completion status
- `priority`: high/medium/low
- `due_date`: Optional due date
- `reminder_time`: Optional reminder datetime
- `created_at`: Creation timestamp
- `updated_at`: Last modification timestamp
- `category_id`: Foreign key to categories

### Categories Table
- `id`: Primary key
- `name`: Category name (unique)
- `color`: Hex color code for UI

## API Endpoints

### Tasks
- `GET /api/tasks` - List all tasks (with filtering)
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task
- `PATCH /api/tasks/<id>/toggle` - Toggle completion status

### Categories
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create new category
- `DELETE /api/categories/<id>` - Delete category

### Statistics
- `GET /api/stats` - Get dashboard statistics

## Customization

### Adding New Priority Levels
1. Update the priority options in `app.py` (Task model)
2. Add corresponding CSS classes in `static/style.css`
3. Update the frontend form in `templates/index.html`

### Changing the Color Scheme
1. Modify CSS variables in `static/style.css`
2. Update gradient backgrounds and accent colors
3. Customize category default colors in `app.py`

### Database Migration
To use PostgreSQL or MySQL instead of SQLite:
1. Install the appropriate database driver
2. Update the `SQLALCHEMY_DATABASE_URI` in `app.py`
3. Run the app to create tables automatically

## Offline Support

The app includes basic offline functionality:
- **Local Storage**: Tasks and categories are automatically saved to browser localStorage
- **Offline Browsing**: View and interact with cached data when offline
- **Auto-Sync**: Changes sync back to the server when connection is restored

## Future Enhancements

### Suggested Features
- 📅 **Calendar View**: Monthly/weekly calendar display
- 👥 **User Authentication**: Multi-user support with login
- 🔄 **Recurring Tasks**: Repeat daily/weekly/monthly tasks
- 📎 **File Attachments**: Add files to tasks
- 🏷️ **Tags System**: Multiple tags per task
- 📱 **Mobile App**: Native iOS/Android apps
- 🔗 **Team Collaboration**: Share tasks with team members
- 📈 **Analytics**: Productivity reports and insights

### Technical Improvements
- **REST API Documentation**: Add OpenAPI/Swagger docs
- **Unit Tests**: Comprehensive test coverage
- **Docker Support**: Containerization for easy deployment
- **CI/CD Pipeline**: Automated testing and deployment
- **Performance Optimization**: Database indexing and caching

## Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

2. **Database errors**
   - Delete `todo.db` file and restart the app to recreate the database

3. **Notifications not working**
   - Ensure you've allowed notifications in your browser
   - Check browser notification settings

4. **Styling issues**
   - Clear browser cache and refresh
   - Check browser developer tools for CSS errors

## Contributing

Feel free to contribute to this project by:
1. Reporting bugs or requesting features
2. Submitting pull requests with improvements
3. Adding new themes or UI enhancements
4. Writing documentation or tutorials

## License

This project is open source and available under the MIT License.

---

**Happy task managing! 🎯**
