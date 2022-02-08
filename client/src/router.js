import Home from './pages/Home';
import Usage from './pages/Usage';
import About from './pages/About';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import Profile from './pages/Profile';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  { path: '/', component: Home, name: 'home' },
  { path: '/usage', component: Usage, name: 'usage' },
  { path: '/about', component: About, name: 'about' },
  { path: '/signin', component: SignIn, name: 'signin' },
  { path: '/signup', component: SignUp, name: 'signup' },
  { path: '/profile', component: Profile, name: 'profile' }
];

const router = createRouter({
  routes,
  history: createWebHistory()
});

export default router;
