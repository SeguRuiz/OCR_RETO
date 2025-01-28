import axios from "axios";

export const post = async ( url = "", datos = {}) => {
  try {
    const respuesta = await axios.post(url, datos);
    const data = await respuesta.data;

    return [respuesta.status, data];
  } catch (error) {
    return [500, error];
  }
};
