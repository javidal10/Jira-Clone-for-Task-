import { combineReducers, configureStore } from '@reduxjs/toolkit';
import { api } from '../api/api';
import queryReducer, { querySlice } from './slices/querySlice';
import storageSession from 'redux-persist/lib/storage/session';
import {
  FLUSH,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
  REHYDRATE,
  persistReducer,
  persistStore,
} from 'redux-persist';
import authSlice from './slices/authSlice';

const persistConfig = {
  key: 'root',
  storage: storageSession,
  whitelist: [
    querySlice.name,
    authSlice.name,
  ],
};

const rootReducer = combineReducers({
  [api.reducerPath]: api.reducer,
  [authSlice.name]: authSlice.reducer,
  query: queryReducer,
});

const persistReducers = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistReducers,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, PAUSE, PERSIST, PURGE, REGISTER, REHYDRATE],
      },
    }).concat(api.middleware),
});

export const persistor = persistStore(store);
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
