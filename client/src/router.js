import Home from './pages/Home';
import Usage from './pages/Usage';
import About from './pages/About';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import Profile from './pages/Profile';
import AccountDeletion from './pages/AccountDeletion';
import AccountUpdate from './pages/AccountUpdate';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  { path: '/', component: Home, name: 'home' },
  { path: '/usage', component: Usage, name: 'usage' },
  { path: '/about', component: About, name: 'about' },
  { path: '/login', component: Login, name: 'login' },
  { path: '/signup', component: SignUp, name: 'signup' },
  { path: '/profile', component: Profile, name: 'profile' },
  {
    path: '/account_deletion',
    component: AccountDeletion,
    name: 'account_deletion'
  },
  { path: '/update', component: AccountUpdate, name: 'update' }
];

const router = createRouter({
  routes,
  history: createWebHistory()
});

export default router;
