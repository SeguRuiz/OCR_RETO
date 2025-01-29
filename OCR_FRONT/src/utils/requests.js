import axios from "axios";

export const post = async (url = "", datos = {}) => {
  try {
    const respuesta = await axios.post(url, datos, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    const data = await respuesta.data;

    return [respuesta.status, data];
  } catch (error) {
    return [500, error];
  }
};

export const postDrive = async (url = "", datos = {}) => {
  try {
    const respuesta = await axios.post(url, datos);
    const data = await respuesta.data;

    return [respuesta.status, data];
  } catch (error) {
    return [500, error];
  }
};
