import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API_BASE = `${BACKEND_URL}/api`;

// Get auth token from localStorage
const getAuthToken = () => {
  return localStorage.getItem('token');
};

// API client with auth
const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const api = {
  // Auth
  register: (data) => apiClient.post('/auth/register', data),
  login: (data) => apiClient.post('/auth/login', data),
  
  // Lessons
  getLessons: (params) => apiClient.get('/lessons', { params }),
  getLesson: (id) => apiClient.get(`/lessons/${id}`),
  createLesson: (data) => apiClient.post('/lessons', data),
  updateLesson: (id, data) => apiClient.put(`/lessons/${id}`, data),
  deleteLesson: (id) => apiClient.delete(`/lessons/${id}`),
  
  // Quizzes
  getQuiz: (lessonId) => apiClient.get(`/quiz/${lessonId}`),
  submitQuiz: (data) => apiClient.post('/quiz/submit', data),
  
  // Progress
  getProgress: (userId) => apiClient.get(`/progress/${userId}`),
  updateProgress: (data) => apiClient.post('/progress/update', data),
  
  // Inquiries
  createInquiry: (data) => apiClient.post('/inquiries', data),
  getInquiries: (params) => apiClient.get('/admin/inquiries', { params }),
  updateInquiry: (id, data) => apiClient.put(`/admin/inquiries/${id}`, data),
  
  // Stats
  getStats: () => apiClient.get('/stats'),
  
  // Certificates
  generateCertificate: (data) => apiClient.post('/certificates/generate', data, {
    responseType: 'blob'
  }),

  // Stripe Payments
  getStripePublishableKey: () => apiClient.get('/stripe/publishable-key'),
  createCheckoutSession: (data) => apiClient.post('/stripe/create-checkout', data),
  getCheckoutStatus: (sessionId) => apiClient.get(`/stripe/checkout-status/${sessionId}`),
};

export default api;
