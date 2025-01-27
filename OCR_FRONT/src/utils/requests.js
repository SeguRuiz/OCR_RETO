import axios from "axios";

export const subirArhivo = async () => {
  try {
    const holaMundoRespuesta = await axios.get(
      "http://localhost:8000/api/hola-mundo"
    );
    const data = await holaMundoRespuesta.data;

    console.log(data);
  } catch (error) {
    console.log(error);
  }
};
