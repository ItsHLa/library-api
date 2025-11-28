# Library RESTful API 

## 📚 Project Overview
A RESTful API for a library management system with user authentication, book management, comment functionality, and role-based access control.

## 🚀 Features

### 🔐 Authentication System
- **Sign Up** - User registration with JWT authentication
- **Login** - User login with JWT token generation  
- **Logout** - Token invalidation system
- **JWT Implementation** - Custom JWT token management

### 📚 Book Management
- **CRUD Operations** - Create, Read, Update, Delete books
- **Manual Pagination** - Custom implemented pagination for books list
- **Advanced Search & Filter** - Comprehensive filtering and search capabilities

### 💬 Comment System
- **Add Comments** - Users can comment on books
- **Reply to Comments** - Users can reply to existing comments
- **Get Comments** - Retrieve all comments for a specific book

### 🏷️ Categories
- **Search Categories** - Search functionality for categories API

## 🛡️ Role-Based Access Control (RBAC)

### 👤 User Role
- View books and categories
- Add/edit own comments and replies
- Search and filter books

### 👑 Admin Role
- All user permissions
- CRUD operations on books
- Manage categories
- User management capabilities
  
## 🔐 Authentication Implementation

### Custome JWT Features
- Custom token generation and validation
- Token expiration management
- Secure token storage and verification
- Manual signature verification
- Token blacklist for logout functionality


## 📊 Search & Filter Capabilities

### 🔍 Search Fields
- **title** - Book titles
- **description** - Book descriptions  
- **categories__name** - Category names
- **authors__first_name** - Author first names
- **authors__last_name** - Author last names

### 🎯 Filter Options
- **author-id** - Filter by specific author ID
- **author-names** - Filter by author names
- **category-id** - Filter by category ID
- **category-names** - Filter by category names

## 🛠️ Technical Implementation

### Manual JWT Authentication
- Custom token generation algorithm
- Manual signature creation and verification
- Token payload structure management
- Expiration time handling

### Manual Pagination
- Custom pagination logic
- Offset and limit calculation
- Page metadata generation
- Total records counting

### RBAC Implementation
- Permission checks on APIS
- Flexible role management system


---

*This project implements a complete RESTful API for library management with custom JWT authentication, manual pagination, advanced search/filtering, and comprehensive role-based access control.*
