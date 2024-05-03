import { lazy, Suspense as S, useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import IconBtn from '../util/IconBtn';
import Avatar from '../util/Avatar';
import { setTheme, Theme } from '../../utils';
import { APIERROR } from '../../api/apiTypes';
import axiosDf from '../../api/axios';
import toast from 'react-hot-toast';
import { useAppSelector } from '../../store/hooks';
import { selectAuthUser } from '../../api/endpoints/auth.endpoint';
const Profile = lazy(() => import('./Profile'));

interface Props {
  theme: Theme;
  toggleTheme: () => void;
}

function Sidebar(props: Props) {
  const {
    theme: { mode },
    toggleTheme,
  } = props;
  const authUser = useAppSelector(selectAuthUser);
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  if (!authUser) return <Navigate to='/login' />;

  const handleToggle = () => {
    toggleTheme();
    setTheme(mode);
  };

  const handleLogOut = async () => {
    await logOut();
    toast('Logged out!');
    navigate('/login');
  };
  return (
    <div className='flex min-h-screen shrink-0'>
      <div className='flex w-14 flex-col items-center justify-between bg-primary py-6'>
        <div className='flex flex-col gap-y-8'>
          <button title='Go to Home' onClick={() => navigate('/project')} className='w-8'>
            <img className='h-8 w-12' src='/assets/jira.svg' alt='jira-clone' />
          </button>
          <input
            checked={mode === 'dark'}
            type='checkbox'
            onChange={handleToggle}
            className='btn-toggle'
            title='Toggle theme'
          />
        </div>
        <div className='flex flex-col gap-6'>
          {authUser && (
            <>
              <Avatar
                title='Profile'
                src={'https://gravatar.com/avatar/b0d4e76057989c6f790446653db8b11f?s=400&d=robohash&r=x'}
                name={authUser.email}
                onClick={() => setIsOpen((p) => !p)}
                className='h-9 w-9 border-[1px] hover:border-green-500'
              />
              <IconBtn onClick={handleLogOut} icon='charm:sign-out' title='Log Out' />
            </>
          )}
        </div>
      </div>
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: isOpen ? 320 : 0 }}
        transition={{ type: 'tween' }}
      >
        {authUser && (
          <S>
            <Profile authUser={authUser} />
          </S>
        )}
      </motion.div>
    </div>
  );
}

export default Sidebar;

async function logOut() {
  const result = await axiosDf.post('user/logout');
  return result.data;
}
