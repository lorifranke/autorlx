import {v4 as uuid} from 'uuid';

export const capitalize = (word) => {
    return word ?
        word.charAt(0).toUpperCase() + word.slice(1) :
        null;
};

export const unique = (array) => {
    return array.filter((value, index, _array) => _array.indexOf(value) === index);
}

export const displayUuid = (uuid) => {
    return uuid.substring(uuid.length - 10, uuid.length);
}

export const averageLastK = (array, lastK) => {
    let elements = array.slice(-lastK);
    return elements.reduce((a, b) => a + b, 0) / elements.length;
}

export const argMax = (arr) => {
    if (arr.length === 0) {
        return -1;
    }
    let max = arr[0];
    let maxIndex = 0;
    for (let i = 1; i < arr.length; i++) {
        if (arr[i] > max) {
            maxIndex = i;
            max = arr[i];
        }
    }
    return maxIndex;
};

export const cloneGym = (gym, new_id) => {
    let clone = {
        id: new_id,
        name: gym.name + " (copy)",
        spaces: structuredClone(gym.spaces),
        reset: gym.reset,
        step: gym.step,
        custom: gym.custom,
        code: gym.code,
        params: structuredClone(gym.params).map(param => {
            param.id = uuid();
            param.gym_id = new_id;
            return param;
        }),
        modules: structuredClone(gym.modules).map(module => {
            module.id = uuid();
            module.gym_id = new_id;
            return module;
        }),
        visualization: gym.visualization,
        created_on: new Date()
    };
    return clone;
}