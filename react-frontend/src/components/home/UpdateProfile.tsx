import { FieldError, FieldValues, useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { AuthUser } from '../../api/apiTypes';
import { useUpdateAuthUserMutation } from '../../api/endpoints/auth.endpoint';
import InputWithValidation from '../util/InputWithValidation';

function UpdateProfile({ user: u }: { user: AuthUser }) {
  const [updateAuthUser] = useUpdateAuthUserMutation();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting: loading },
  } = useForm();

  const handleUpdate = async (form: FieldValues) => {
    if (
      !u ||
      (form.email === u.email)
    )
      return;
    await updateAuthUser(form);
    toast('Updated profile!');
  };
  return (
    <>
      <div className='flex w-[16.5rem] flex-col gap-4'>
        <InputWithValidation
          label='Email'
          placeholder='email'
          defaultValue={u.email}
          register={register('email', {
            required: { value: true, message: 'username must not be empty' },
          })}
          error={errors.email as FieldError}
          readOnly
          darkEnabled
        />
        <InputWithValidation
          label='Photo Url'
          placeholder='profile picture'
          defaultValue={'https://gravatar.com/avatar/b0d4e76057989c6f790446653db8b11f?s=400&d=robohash&r=x'}
          register={register('profileUrl')}
          darkEnabled
        />
      </div>
      <button onClick={handleSubmit(handleUpdate)} className='btn mt-10 w-full'>
        {loading ? 'saving ...' : 'Save Changes'}
      </button>
    </>
  );
}

export default UpdateProfile;
