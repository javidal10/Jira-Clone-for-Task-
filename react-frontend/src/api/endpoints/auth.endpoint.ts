import { api } from '../api';
import { AuthUser, LoginCredentials, PublicUser, RegisterCredentials, jwtAuthUser, updateAuthUser } from '../apiTypes';

export const extendedApi = api.injectEndpoints({
  endpoints: (builder) => ({
    authUser: builder.query<AuthUser, void>({
      query: () => ({ url: `user/get_authenticated_user/` }),
      providesTags: ['AuthUser'],
    }),
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
      query: (body) => ({
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
  useAuthUserQuery, 
  useUpdateAuthUserMutation, 
  usePublicUserQuery, 
  useLoginMutation, 
  useRegisterMutation } = extendedApi;

// selectors
export const selectAuthUser = () =>
  extendedApi.useAuthUserQuery(undefined, {
    selectFromResult: ({ data }) => 
      ({ authUser: data }),
  });
