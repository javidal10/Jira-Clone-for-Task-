import { api } from '../api';
import { Comment, CreateComment, DeleteComment, getComments } from '../apiTypes';

export const extendedApi = api.injectEndpoints({
  endpoints: (builder) => ({
    cmts: builder.query<Comment[], getComments>({
      query: ({ issueId, projectId }) => ({
        url: `issues/${issueId}/get_comments?projectId=${projectId}`, // Updated endpoint
      }),
      providesTags: ['Comments'],
    }),
    createCmt: builder.mutation<void, CreateComment>({
      query: (body) => ({ url: 'comment/create_comment/', method: 'POST', body }), // Updated endpoint
      invalidatesTags: ['Comments'],
    }),
    deleteCmt: builder.mutation<void, DeleteComment>({
      query: ({ id, ...body }) => ({
        url: `comment/${id}/delete_comment/`, // Updated endpoint
        method: 'DELETE',
        body,
      }),
      invalidatesTags: ['Comments'],
    }),
  }),
  overrideExisting: false,
});

export const { useCmtsQuery, useCreateCmtMutation, useDeleteCmtMutation } = extendedApi;
