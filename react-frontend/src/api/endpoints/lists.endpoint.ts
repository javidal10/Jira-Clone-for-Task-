import { api } from '../api';
import type { CreateList, DeleteList, List, ReorderList, UpdateList } from '../apiTypes';

export const extendedApi = api.injectEndpoints({
  endpoints: (builder) => ({
    lists: builder.query<List[], number>({
      query: (projectId) => ({
        url: `list/${projectId}/get_lists_in_project/`, // Updated endpoint
      }),
      providesTags: ['Lists'],
    }),
    createList: builder.mutation<List, CreateList>({
      query: (body) => ({ url: 'list/create_list/', method: 'POST', body }), // Updated endpoint
      invalidatesTags: ['Lists'],
    }),
    updateList: builder.mutation<List, UpdateList>({
      query: ({ listId, body }) => ({
        url: `list/${listId}/update_list/`, // Updated endpoint
        method: 'PUT',
        body,
      }),
      invalidatesTags: ['Lists'],
    }),
    deleteList: builder.mutation<List, DeleteList>({
      query: ({ listId, projectId }) => ({
        url: `list/${listId}/delete_list/`, // Updated endpoint
        method: 'DELETE',
        body: { projectId },
      }),
      invalidatesTags: ['Lists'],
    }),
    reorderLists: builder.mutation<void, ReorderList>({
      query: (body) => ({
        url: 'list/reorder_lists/', // Updated endpoint
        method: 'PUT',
        body,
      }),
      invalidatesTags: ['Lists'],
      async onQueryStarted({ order, newOrder, projectId }, { dispatch }) {
        dispatch(
          extendedApi.util.updateQueryData('lists', projectId, (oldLists) =>
            updateListOrderLocally(oldLists, { s: order - 1, d: newOrder - 1 })
          )
        );
      },
    }),
  }),
  overrideExisting: false,
});

export const {
  useListsQuery,
  useCreateListMutation,
  useUpdateListMutation,
  useDeleteListMutation,
  useReorderListsMutation,
} = extendedApi;

// selector
export const selectLists = (projectId: number) =>
  extendedApi.useListsQuery(projectId, {
    selectFromResult: ({ data }) => ({ lists: data }),
  });

// helpers
function updateListOrderLocally(array: List[], { s, d }: { s: number; d: number }) {
  const source = array.slice(0);
  const draggedIssue = source.splice(s, 1)[0]; // remove dragged item from its source list
  source.splice(d, 0, draggedIssue); // insert dragged item into target list
  return source;
}
