export interface DietMateUser {
  id: string;
  name: string;
  email: string;
}

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface AccountProgress {
  profile_completed: boolean;
  preferences_completed: boolean;
  has_meal_plan: boolean;
}

export interface AuthResult {
  user: DietMateUser;
  progress: AccountProgress;
}
