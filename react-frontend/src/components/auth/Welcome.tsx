import { FieldValues, useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import SS from '../util/SpinningCircle';
import Form from './Form';
import { useLoginMutation, useRegisterMutation } from '../../api/endpoints/auth.endpoint';

interface Props {
  type: 'LOGIN' | 'REGISTER';
}

const Welcome = (props: Props) => {
  const isLogin = props.type === 'LOGIN';
  const {
    register,
    formState: { errors, isSubmitting: loading, isSubmitSuccessful: success },
    handleSubmit,
  } = useForm();

  const [logInUser] = useLoginMutation();
  const [registerNewUser] = useRegisterMutation();

  const logIn = async (body: FieldValues) => {
    try {
      await logInUser({email: body.email, pwd: body.pwd});
    } catch (error) {
      console.log('error', error);
    }
  };

  const registerUser = async (body: FieldValues) => {
    try {
      await registerNewUser({email: body.email, pwd: body.pwd});
    } catch (error) {
      console.log('error', error);
    }
  };

  const isLoading = loading && !success;

  return (
    <div className='bg-jira-gradient flex h-fit min-h-screen w-full flex-col items-center'>
      <div className='mx-auto my-16 w-11/12 max-w-[40rem] tracking-wide text-white'>
        <h1 className='text-center text-xl font-medium sm:text-2xl lg:text-4xl lg:font-semibold'>
          The #1 software development tool used by agile teams
        </h1>
      </div>
      <div className='mb-12 w-11/12 max-w-[24rem]'>
        <div className={`h-[40vh] place-items-center ${isLoading ? 'grid' : 'hidden'}`}>
          <SS />
        </div>
        <div className={`w-full rounded-md bg-white py-12 px-6 ${isLoading ? 'hidden' : 'block'}`}>
          <h2 className='text-center text-3xl font-medium text-gray-800'>
            {isLogin ? 'Welcome back' : 'Get Started'}
          </h2>
          <h3 className='mb-5 text-center text-[15px] text-gray-600'>Free for testing</h3>
          <Form
            type={isLogin ? 'LOGIN' : 'SIGNUP'}
            onSubmit={isLogin ? logIn : registerUser}
            {...{ errors, handleSubmit, register, loading }}
          />
          <div className='flex items-center'>
            <hr className='grow border-t-[.5px] border-gray-400' />
            <span className='my-3 block w-fit bg-white px-2 text-center'>OR</span>
            <hr className='grow border-t-[.5px] border-gray-400' />
          </div>
          <Link to={isLogin ? '/register' : '/login'}>
            <span className='block text-center text-blue-600 hover:underline'>
              {isLogin ? 'Join now' : 'Log In'}
            </span>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Welcome;