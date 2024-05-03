import { useAppSelector } from '../../store/hooks';
import { RootState } from '../../store/store';
import { api } from '../api';
import { AuthUser, LoginCredentials, PublicUser, RegisterCredentials, jwtAuthUser, updateAuthUser } from '../apiTypes';

export const extendedApi = api.injectEndpoints({
  endpoints: (builder) => ({
    publicUser: builder.query<PublicUser, number>({
      query: (id) => ({ url: `user/${id}` }),
    }),
    updateAuthUser: builder.mutation<AuthUser, updateAuthUser>({
      query: (body) => ({
        url: 'user/update_auth_user/',
        method: 'PUT',
        body,
      }),
      invalidatesTags: ['AuthUser'],
    }),
    login: builder.mutation<jwtAuthUser, LoginCredentials>({
      query: (body) => (
        {
        url: 'user/login/',
        method: 'POST',
        body: body,
      }),
    }),
    register: builder.mutation<void, RegisterCredentials>({
      query: (credentials) => ({
        url: 'user/register/',
        method: 'POST',
        body: credentials,
      }),
    }),
  }),
  overrideExisting: false,
});

export const {
  endpoints,
  useUpdateAuthUserMutation, 
  usePublicUserQuery, 
  useLoginMutation, 
  useRegisterMutation } = extendedApi;

// selectors
export const selectAuthUser = () => useAppSelector((state: RootState) => state.auth.user);

