import axios from "axios";
import { useState } from "react";

const api = axios.create({
    baseURL: "https://ocr-reto.onrender.com/api",
  });

export const post = async (url = "", datos = {}) => {
  try {
    const respuesta = await api.post(url, datos, {
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
    const respuesta = await api.post(url, datos);
    const data = await respuesta.data;

    return [respuesta.status, data];
  } catch (error) {
    return [500, error];
  }
};


const useAxiosProgress = () => {
  const [uploadProgress, setUploadProgress] = useState(0);

  const subirArchivo = async (url, file, config = {}) => {
    try {
      const respuesta = await axios.post(url, file, {
        ...config,
        onUploadProgress: (progressEvent) => {
          const percent = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setUploadProgress(percent);
        },
      });
      const datos = await respuesta.data;

      return [respuesta.status, datos];
    } catch (error) {
      return [500, error];
    }
  };

  return { uploadProgress, subirArchivo };
};

export default useAxiosProgress;
