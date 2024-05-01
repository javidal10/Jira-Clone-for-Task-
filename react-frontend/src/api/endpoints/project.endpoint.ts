import { api } from '../api';
import type { CreateProject, EditProject, LeaveProject, Project } from '../apiTypes';

export const extendedApi = api.injectEndpoints({
  endpoints: (builder) => ({
    projects: builder.query<Project[], number>({
      query: () => ({ url: `projects/` }),
      providesTags: ['Project'],
    }),
    project: builder.query<Project, number>({
      query: (projectId) => ({
        url: `projects/${projectId}/`, // Updated endpoint
      }),
      providesTags: ['Project'],
    }),
    createProject: builder.mutation<Project, CreateProject>({
      query: (body) => ({ url: 'projects/', method: 'POST', body }), // Updated endpoint
      invalidatesTags: ['Project'],
    }),
    deleteProject: builder.mutation<void, number>({
      query: (projectId) => ({
        url: `projects/${projectId}/delete_project/`, // Updated endpoint
        method: 'DELETE',
      }),
      invalidatesTags: ['Project'],
    }),
    leaveProject: builder.mutation<void, LeaveProject>({
      query: ({ projectId, ...body }) => ({
        url: `projects/${projectId}/leave_project/`, // Updated endpoint
        method: 'DELETE',
        body,
      }),
      invalidatesTags: ['Project'],
    }),
    updateProject: builder.mutation<void, EditProject>({
      query: (body) => ({ url: `projects/${body.id}/update_project/`, method: 'PUT', body }), // Updated endpoint
      invalidatesTags: ['Project'],
      async onQueryStarted({ id, ...newData }, { dispatch }) {
        dispatch(
          extendedApi.util.updateQueryData('project', id, (oldData) => ({
            ...oldData,
            ...newData,
          }))
        );
      },
    }),
  }),
  overrideExisting: false,
});

export const {
  useProjectsQuery,
  useProjectQuery,
  useCreateProjectMutation,
  useUpdateProjectMutation,
  useLeaveProjectMutation,
  useDeleteProjectMutation,
} = extendedApi;

// selectors
export const selectCurrentProject = (projectId: number) =>
  extendedApi.useProjectQuery(projectId, {
    selectFromResult: ({ data }) => ({ project: data }),
  });
