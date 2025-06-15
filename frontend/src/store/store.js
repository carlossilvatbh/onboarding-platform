import { configureStore } from '@reduxjs/toolkit';

// Slices (will be created as needed)
const authSlice = {
  name: 'auth',
  initialState: {
    isAuthenticated: false,
    user: null,
    token: null,
    loading: false,
    error: null,
  },
  reducers: {
    loginStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    loginSuccess: (state, action) => {
      state.loading = false;
      state.isAuthenticated = true;
      state.user = action.payload.user;
      state.token = action.payload.token;
      state.error = null;
    },
    loginFailure: (state, action) => {
      state.loading = false;
      state.isAuthenticated = false;
      state.user = null;
      state.token = null;
      state.error = action.payload;
    },
    logout: (state) => {
      state.isAuthenticated = false;
      state.user = null;
      state.token = null;
      state.error = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
};

// Create a simple reducer function
const authReducer = (state = authSlice.initialState, action) => {
  switch (action.type) {
    case 'auth/loginStart':
      return { ...state, loading: true, error: null };
    case 'auth/loginSuccess':
      return {
        ...state,
        loading: false,
        isAuthenticated: true,
        user: action.payload.user,
        token: action.payload.token,
        error: null,
      };
    case 'auth/loginFailure':
      return {
        ...state,
        loading: false,
        isAuthenticated: false,
        user: null,
        token: null,
        error: action.payload,
      };
    case 'auth/logout':
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        token: null,
        error: null,
      };
    case 'auth/clearError':
      return { ...state, error: null };
    default:
      return state;
  }
};

export const store = configureStore({
  reducer: {
    auth: authReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

// Action creators
export const loginStart = () => ({ type: 'auth/loginStart' });
export const loginSuccess = (payload) => ({ type: 'auth/loginSuccess', payload });
export const loginFailure = (error) => ({ type: 'auth/loginFailure', payload: error });
export const logout = () => ({ type: 'auth/logout' });
export const clearError = () => ({ type: 'auth/clearError' });

export default store;

