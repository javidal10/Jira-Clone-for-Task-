import { createSlice } from "@reduxjs/toolkit";
import { endpoints }  from "../../../api/endpoints/auth.endpoint";
import { jwtAuthUser } from "../../../api/apiTypes";



const initialState: jwtAuthUser = {
    refresh: null,
    access: null,
    user: undefined,
};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {},
    extraReducers(builder) {
        builder.addMatcher(endpoints.login.matchFulfilled, (state, action) => {
            const payload  = action.payload;
            return {
                ...state,
                refreshToken: payload.refresh,
                accessToken: payload.access,
                user: payload.user || undefined,
            };
        });
    },
});


export const actions = authSlice.actions;

export default authSlice;