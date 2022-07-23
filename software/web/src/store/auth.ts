import {
    ACTION_FETCH_STATIONS_DATA,
    ACTION_UPDATE_STATION_DATA,
    MUTATION_UPDATE_STATION_DATA,
} from "../../variables";
import { Station } from "../../../types/stations";
import { getStations } from "../../../api/getStations";

export interface StationsState {
    stations: Record<string, Station>;
}

const initialState = {
    stations: {},
} as StationsState;

const auth = {
    namespaced: true,
    state: initialState,

    getters: {
        stations: (state: StationsState): unknown => {
            return state.stations;
        },
    },

    mutations: {
        [MUTATION_UPDATE_STATION_DATA](state: StationsState, data: Station): void {
            state.stations[data.id] = data;
        },
    },

    actions: {
        /**
         * Function to check if station not exists and updates station info
         */
        async [ACTION_UPDATE_STATION_DATA](
            {
                commit,
                state,
            }: {
                commit: <T extends unknown[]>(...args: T) => void;
                state: StationsState;
            },
            station: Station
        ): Promise<void> {
            if (station.id != 0 && station.id !== undefined) {
                if (
                    !Object.keys(state.stations).includes((station.id.toString()).toString()) ||
                    !(JSON.stringify(state.stations[station.id.toString()]) !== JSON.stringify(station))
                ) {
                    commit(MUTATION_UPDATE_STATION_DATA, station);
                }
            }
        },

        /**
         * Function to get all stations
         */
        async [ACTION_FETCH_STATIONS_DATA]({
            commit,
            dispatch,
            state,
        }: {
            commit: <T extends unknown[]>(...args: T) => void;
            dispatch: <T extends unknown[]>(...args: T) => void;
            state: StationsState;
        }): Promise<void> {
            const stations = await getStations()

            stations.forEach(station => {
                dispatch(ACTION_UPDATE_STATION_DATA, station);
            });
        },
    },
};

export default auth;
