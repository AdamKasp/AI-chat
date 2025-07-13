export interface UserCreateRequest {
  login: string;
}

export interface UserResponse {
  id: string;
  login: string;
  created_at: string;
  updated_at: string | null;
}

export interface UserListResponse {
  users: UserResponse[];
  total: number;
  limit: number;
}

export interface UserDeleteResponse {
  message: string;
}