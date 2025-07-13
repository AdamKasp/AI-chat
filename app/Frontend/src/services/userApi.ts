import { UserCreateRequest, UserResponse, UserListResponse, UserDeleteResponse } from '../types/user';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8008';

export const userApi = {
  // Get all users with pagination
  getUsers: async (limit: number = 100, offset: number = 0): Promise<UserListResponse> => {
    const response = await fetch(`${API_BASE_URL}/users?limit=${limit}&offset=${offset}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  // Get specific user by ID
  getUser: async (userId: string): Promise<UserResponse> => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  // Create new user
  createUser: async (userData: UserCreateRequest): Promise<UserResponse> => {
    const response = await fetch(`${API_BASE_URL}/users`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  // Delete user by ID
  deleteUser: async (userId: string): Promise<UserDeleteResponse> => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  },
};