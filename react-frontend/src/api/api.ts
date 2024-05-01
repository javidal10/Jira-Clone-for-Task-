import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const api = createApi({
	reducerPath: 'jiraApiReducer',
	baseQuery: fetchBaseQuery({
		baseUrl: 'http://localhost:8000/api/',
		prepareHeaders(headers) {
			return headers
		},
	}),
	tagTypes: ['Lists', 'Issues', 'Project', 'Members', 'AuthUser', 'Comments'],
	endpoints: ({}) => ({}),
})

export const {} = api
