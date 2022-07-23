
export type SensorData = {
    controller: number,
    controllerName: string,
    area: number,
    areaName: string,
    humidity: number,
    temperature: number,
    raining: boolean,
    date: string,
}


export type SensorDataSearch = {
    start: string,
    end: string,
}
